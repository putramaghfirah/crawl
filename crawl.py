from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests
from tqdm import tqdm
from pathlib import Path

raw_url = 'https://indeks.kompas.com/terpopuler/'
date = datetime.now()

i = 0
batas_page = 2000

print("Wait a second...")
while i < batas_page:
    url = f"{raw_url}{date.strftime('%Y-%m-%d')}"
    raw_data = BeautifulSoup(requests.get(
        url).text.encode('utf-8'), 'html.parser')
    link = raw_data.select('.article__title')
    for links in link:
        urls = links.find('a')['href']
        soup = BeautifulSoup(requests.get(
            urls).text.encode('utf-8'), 'html.parser')
        try:
            judul = soup.select_one('.read__title').get_text()
            content = soup.select_one('.read__content')
            for decode in content('script'):
                decode.decompose()
            directory = Path()/'data'/f'data{i+1}.txt'
            with open(directory, 'w') as file:
                file.write(f"{urls}\n{judul}\n{content.getText()}")
            i += 1
        except AttributeError:
            pass
        if i is batas_page:
            break
    date += timedelta(days=-1)
print("done")
