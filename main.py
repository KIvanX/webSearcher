import json
import time
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By

caps = ChromeOptions()
caps.page_load_strategy = "eager"
driver = webdriver.Chrome(options=caps)

pages, i = [], 1
while len(pages) < 100:
    driver.get(f'https://habr.com/ru/search/page{i}/?q=андроид&target_type=posts&order=relevance')
    time.sleep(2)
    i += 1

    urls = [e.find_element(By.CLASS_NAME, 'tm-title__link').get_attribute('href') for e in driver.find_elements(By.TAG_NAME, 'article')]
    for page_url in urls[:3]:
        try:
            driver.get(page_url)
            time.sleep(1)

            content = driver.find_element(By.CLASS_NAME, 'tm-article-body').text
            if len(content) > 3000:
                pages.append({'url': page_url, 'content': content})
                print(len(pages))
        except:
            pass


index_text = '\n'.join([f'page_{i}.txt - {page["url"]}' for i, page in enumerate(pages)])
with open('index.txt', 'w', encoding='utf-8') as f:
    f.write(index_text)

for i, page in enumerate(pages):
    with open(f'static/page_{i}.txt', 'w', encoding='utf-8') as f:
        f.write(page['content'])
