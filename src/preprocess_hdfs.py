import re

input_file = "../hdfs_logs/HDFS_2k.log"
output_file = "../processed/hdfs_clean.txt"

def clean_hdfs(line):
    # remove numeric timestamp block
    line = re.sub(r'^\d+\s+\d+\s+\d+\s+', '', line)

    # remove IP addresses
    line = re.sub(r'\d+\.\d+\.\d+\.\d+', '<IP>', line)

    # replace block IDs
    line = re.sub(r'blk_-?\d+', '<BLOCK>', line)

    # replace numbers
    line = re.sub(r'\d+', '<NUM>', line)

    return line.lower().strip()

with open(input_file, "r", errors="ignore") as f, \
     open(output_file, "w") as out:
    for line in f:
        out.write(clean_hdfs(line) + "\n")

print("HDFS preprocessing complete.")
