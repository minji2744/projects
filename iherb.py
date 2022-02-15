from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import requests
import urllib.request
import os
import json
from collections import OrderedDict


def get_product_url(array):
    for x in array:
        url = f'https://kr.iherb.com/c/{x}'
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "lxml")
        product_lists = soup.find_all('div', attrs={'class':'absolute-link-wrapper'})
        urls = []
        for t in product_lists:
            try:
                urls.append(t.find('a').attrs['href'])
            except:
                pass
    return urls


def product_info(url):
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    name = soup.select('h1#name')[0].get_text().strip()
    category = soup.select('div#breadCrumbs')[0].get_text().strip()
    category = category.replace("\n", "/")
    info = soup.find('ul', attrs={'id':'product-specs-list'})
    info = info.find_all('li')
    for i in info:
        text = i.get_text()
        if 'UPC' in text:
            upc_code = text.split(":")[1].strip()
    return name, category, upc_code


if __name__ == "__main__":
    headers = {"User-Agent":""}

    options = webdriver.ChromeOptions()
    # options.headless=True
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars --disable-extensions --no-sandbox --disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36")
    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "none"
    driver = webdriver.Chrome(desired_capabilities=caps, options=options)

    cats = []
    brands = ['21st-century-health-care']
    urls = get_product_url(brands)

    dict = {}
    for url in urls:
        name, category, upc_code = product_info(url)
        dict[name] = {
            'category':category,
            'upc_code':upc_code,
            'reviews':[]
        }
        cut_url = '/'.join(url.split('/')[4:])
        review_url = 'https://kr.iherb.com/r/' + cut_url + '?p='

        for i in range(1, 4):
            url = review_url + str(i)
            driver.get(url)
            time.sleep(5)

            reviews = driver.find_elements_by_css_selector('div.review-text')
            for review in reviews:
                dict[name]['reviews'].append(review.text)
        print(dict)
        break
    with open('./iherb_review.json', 'w') as f:
        json.dump(dict, f, ensure_ascii=False, indent=4)
    
    driver.close()