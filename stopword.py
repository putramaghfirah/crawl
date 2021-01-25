from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests
from tqdm import tqdm
from string import punctuation

from pathlib import Path

raw_url = 'https://indeks.kompas.com/?site=all&date='
date = datetime.now()

batas_stopword = 50
batas_page = 10
links = list()
data = dict()
i = 1
print("Process...")
# perulangan untuk mendapatkan link
while len(links) < batas_page:
    # mengambil link kompas berdasarkan hari ini
    url = f"{raw_url}{date.strftime('%Y-%m-%d')}"
    while len(links) < batas_page:
        raw_data = BeautifulSoup(requests.get(
            url).text.encode('utf-8'), 'html.parser')
        # mengambil link lalu memasukkan kedalam list
        links += [link['href'] for link in raw_data.select('.article__link')]
        if raw_data.select_one('.paging__link--next'):
            # mengambil page tiap halaman
            url = raw_data.select_one('.paging__link--next')['href']
            continue
        date += timedelta(day=-1)
        continue

# perulangan untuk membangun stopword
for link in tqdm(links[:batas_page]):
    raw_data = BeautifulSoup(requests.get(
        link).text.encode('utf-8'), 'html.parser')
    try:
        for i in raw_data(['script']):
            i.decompose()
        # mengambil content-content pada tiap link
        content = raw_data.select_one('.read__content').get_text()
        judul = raw_data.select_one('.read__title').get_text()
    except AttributeError:
        pass
    # ini untuk teks preprocessing
    term = content.translate(str.maketrans(
        '', '', punctuation)).lower().split()
    # term2 = content.translate(str.maketrans(
    #     '', '', punctuation)).lower()
    directory = Path()/'data'/f'data{i}.txt'
    with open(directory, 'w') as file:
        file.write(f"{link}\n{judul}\n{term}")
    if i is batas_page:
        break
    # kondisi pengecekan unique word
    for word in term:
        if data.get(word):
            data[word] += 1
        else:
            data[word] = 1

# melakukan sorting pada kata berdasarkan frekuensi terbanyak
data_sorted = sorted(data.items(), key=lambda x: x[1], reverse=True)

# memasukkan kata stopword kedalam file txt
with open('stopword.txt', 'w') as file:
    for kata, freq in data_sorted[:batas_stopword]:
        file.write(f"{kata} {freq}\n")

# menampilkan jumlah kata unik
print(f'Total unique word = {len(data_sorted)}')
print("Done...")
