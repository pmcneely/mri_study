import os
import shutil
import zipfile

INPUT_DIR = os.path.abspath("./preproc/")
OUTPUT_DIR = os.path.abspath("./stats_data/")

counter = 0

for filename in os.listdir(INPUT_DIR):
    # print(f"Checking file {filename}")
    if os.path.isdir(filename):
        print(f"Found directory {filename} - Aborting")
        continue
    # if counter > 2:
    #     break
    # print(f"Basename: {basename}\nDirectories: {directories}\nFiles: {files}")
    f_base = filename.split(".")[-1]
    if f_base != "zip":
        continue
    counter += 1
    # print(f"Found a target! --> {f_base}")
    print(f"Processing sample {counter}")
    archive = zipfile.ZipFile(
        os.path.abspath(
            os.path.join(INPUT_DIR, filename)
            )
        )
    subject_id = filename.split("_")[0]
    # print(f"Got subject ID {subject_id}")
    stats_path = "{0}/T1w/{0}/stats".format(subject_id)
    destination_path = os.path.join(OUTPUT_DIR, f"{subject_id}")
    tmp_path = os.path.join(OUTPUT_DIR, stats_path)

    # print(f"Searching stats path {stats_path}")
    # Collect the stats files
    for file in archive.namelist():
        # print(f"Found archive file {file}")
        if file.startswith(stats_path):
            archive.extract(file, OUTPUT_DIR)
    # Move the stats files to the top-level subject directory
    to_move = []
    for file in os.listdir(tmp_path):
        if os.path.isdir(file):
            continue
        to_move.append(
            (os.path.join(tmp_path, file), os.path.join(destination_path, file))
        )
    for pair in to_move:
        # print(f"Moving!\n{pair[0]} to\n{pair[1]}")
        os.rename(pair[0], pair[1])

    # Remove trailing directories
    shutil.rmtree(os.path.join(destination_path, "T1w"))

print(f"---> Processing {counter} samples complete <---")

