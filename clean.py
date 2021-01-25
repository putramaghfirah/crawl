from pathlib import Path
from string import punctuation

paths = [path for path in Path('data').glob('*.txt')]
data = dict()
print("Reading file process...")
for path in paths:
    with open(path) as file:
        raw = file.read()
        term = raw.translate(str.maketrans(
            '', '', punctuation)).lower().split()
        for item in term:
            if data.get(item):
                data[item] += 1
            else:
                data[item] = 1

data_sorted = sorted(data.items(), key=lambda v: v[1], reverse=True)

with open('stopword.txt', 'w') as file:
    for kata, freq in data_sorted[:20]:
        file.write(f"{kata} {freq}\n")

print(f'Total unique word = {len(data_sorted)}')
print("Done...")
