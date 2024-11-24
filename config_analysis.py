import pandas as pd

file_path_is = "result_configs/is_results_small.txt"
file_path_ds = "result_configs/ds_results_small.txt"
with open(file_path_is, "r") as file:
    is_lines = file.readlines()

with open(file_path_ds, "r") as file:
    ds_lines = file.readlines()

def parse_lines(lines):
    data = []
    current_entry = {}
    for line in lines:
        line = line.strip()
        print(f"line: {line}")
        if not line:
            if current_entry:
                data.append(current_entry)
                current_entry = {}
        else:
            if line.startwith("prompts:"):
                print(line.replace("prompts:", "").strip())
                prompts = line.replace("prompts:", "").strip().split("' '")
                current_entry["prompts"] = [p.strip("'") for p in prompts]
            elif line.startwith("style:"):
                style = line.replace("style:", "").strip().strip("'")
                current_entry["style"] = style
            elif line.startwith("views:"):
                views = line.replace("views:", "").strip().split("' '")
                current_entry["views"] = [v.strip("'") for v in views]
    if current_entry:
        data.append(current_entry)
    return data

data_is = parse_lines(is_lines)
data_ds = parse_lines(ds_lines)

is_df = pd.DataFrame(data_is)
ds_df = pd.DataFrame(data_ds)

print(is_df)
print(ds_df)



    
