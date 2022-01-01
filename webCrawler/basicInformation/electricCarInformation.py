import requests
from bs4 import BeautifulSoup
import csv
import os
import re

PATH = '../基本信息相关/electricCarInformation.csv'

def getHTML(url):
    try:
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)',
            'Host': 'auto.16888.com'
        }
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        r.encoding = 'utf-8'
        print(r.status_code)
        return r.text
    except:
        return 'Spider failed！'

def save_columns_to_csv(columns, encoding='utf-8'):

    with open(PATH, 'a', encoding=encoding) as csvfile:
        csv_write = csv.writer(csvfile)
        csv_write.writerow(columns)

def spider():
    url = 'http://auto.16888.com/ev.html#3'
    data = getHTML(url)
    soup = BeautifulSoup(data, 'lxml')

    try:
        pattern1 = '<span class="name">\s+<a target="_blank" href="https://www.16888.com/.*?/">(.*?)</a>'
        nameList = re.findall(pattern1, data, re.S)
        print(nameList)

        lowPricePattern = '<p><a target="_blank" href="https://price.16888.com/sr-.*?.html">(.*?)&nbsp;-&nbsp;.*?万</a></p>'


    except Exception as err:
        print(err)

if __name__ == '__main__':
    titleList = ['车型', '最低价', '最高价']
    if os.path.exists(PATH):
        os.remove(PATH)
    save_columns_to_csv(titleList)

    spider()
