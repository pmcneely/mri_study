import os
import pandas as pd

TARGET_DIR = "./stats_data/"

BASE_TARGET_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), TARGET_DIR)
)

FILES = {
    "aseg.stats",
    "lh.aparc.stats",
    "lh.BA.stats",
    "lh.BA.thresh.stats",
    "lh.entorhinal_exvivo.stats",
    "rh.aparc.stats",
    "rh.BA.stats",
    "rh.BA.thresh.stats",
    "rh.entorhinal_exvivo.stats",
    "wmparc.stats",
}

FIELDS = (
    "StructName",
    "Volume_mm3",
    "SurfArea",
    "GreyVol",
    "ThickAvg",
    "ThickStd",
    "FoldInd",
    "CurvInd",
)

eTIV = "EstimatedTotalIntraCranialVol,"

counter = 0

for basename, directories, files in os.walk(BASE_TARGET_DIR):
    if basename.split('/')[-1] == 'stats_data':
        continue

    counter += 1
    # if counter > 1:
    #     break
    
    # print(f"--> {basename} - found {len(directories)} directories and {len(files)} files")

    results = { k: [] for k in FIELDS }
    results["Source"] = []
    subject_meta_info = {
        "ID": "Unknown",
        "eTIV": -1,
    }

    for f in sorted(files):

        if f not in FILES:
            continue
        # print(f"Processing file {f}")

        lookup_index = { k: -1 for k in FIELDS }

        subject_id = basename.split("/")[-1]
        subject_meta_info["ID"] = subject_id

        with open(os.path.join(basename, f), "r") as fp:
            lines = fp.readlines()
        fp.close()
        for line in lines:
            line = line.split()
            if len(line) == 1:
                continue
            if line[0] == "#" and line[1] != "ColHeaders":
                if f == "aseg.stats":
                    if line[2] == eTIV:
                        subject_meta_info['eTIV'] = float(line[-2].rstrip(','))
                continue
            if line[0] == "#" and line[1] == "ColHeaders":
                for idx, item in enumerate(line[2:]):
                    if item in FIELDS:
                        lookup_index[item] = idx
                continue

            for field, index in lookup_index.items():
                if index == -1:
                    results[field].append("NaN")
                    continue
                results[field].append(line[index])
            results["Source"].append(f)

    df = pd.DataFrame().from_dict(results)
    df.to_excel(os.path.join(basename, "data.xlsx"))

    meta_df = pd.DataFrame().from_dict(subject_meta_info, orient="index").T
    meta_df.to_excel(os.path.join(basename, "meta_data.xlsx"))


print(f"---> Routine complete. {counter - 1} subjects processed")
# print(f"{subject_meta_info}:\n{results}")
