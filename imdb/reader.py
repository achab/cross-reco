import pandas as pd

try:
    data = pd.read_json('items.jl')
except:
    with open("items.jl", "rb") as f:
        lines = f.readlines()
    lines = map(lambda x: x.rstrip(), lines)
    data_json_str = "[" + ','.join(lines) + "]"
    data = pd.read_json(data_json_str)

print(data.head())
print(" ")
print(str(len(data)) + " movies scrapped")
