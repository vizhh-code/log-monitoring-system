import re

input_file = "../linux_logs/Linux_2k.log"
output_file = "../processed/linux_clean.txt"

def clean_linux(line):
    # remove month timestamp
    line = re.sub(r'^[A-Z][a-z]{2}\s+\d+\s+\d+:\d+:\d+\s+', '', line)

    # remove hostname
    line = re.sub(r'^\S+\s+', '', line)

    # remove pid like [12345]
    line = re.sub(r'\[\d+\]', '', line)

    # replace numbers
    line = re.sub(r'\d+', '<NUM>', line)

    return line.lower().strip()

with open(input_file, "r", errors="ignore") as f, \
     open(output_file, "w") as out:
    for line in f:
        out.write(clean_linux(line) + "\n")

print("Linux preprocessing complete.")
