import os

dataset = []
data_dir = "data"

if os.path.exists(data_dir):
    for filename in os.listdir(data_dir):
        if filename.endswith(".txt"):
            filepath = os.path.join(data_dir, filename)
            with open(filepath, "r", encoding="utf-8") as file:
                lines = [line.strip() for line in file if line.strip()]
                dataset.extend(lines)
                print(f"Loaded {len(lines)} entries from {filename}")
else:
    print(f"Directory '{data_dir}' not found.")