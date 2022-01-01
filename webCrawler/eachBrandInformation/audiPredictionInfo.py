import requests
from bs4 import BeautifulSoup
import csv
import os
import re

PATH = '../预测相关/吉利.csv'
global count
count = 158

def getHTML(url):
    try:
        headers = {
            'user-agent': 'Mozilla/5.0',
            'Host': 'xl.16888.com'
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

def spider(i):
    global count
    j = i+1
    url1 = 'https://xl.16888.com/b/57604-'
    url2 = '.html'
    url = (f'{url1}{j}{url2}')
    print(url)
    data = getHTML(url)
    soup = BeautifulSoup(data, 'lxml')

    try:
        numberList = []
        nameList = []
        saleList = []
        priceList = []

        patName1 = '<td class="xl-td-t4">(.*?)</td>'
        wholeList = re.findall(patName1, data)

        patName2 = '<td class="xl-td-t4"><a href="/.*?.html" target="_blank">(.*?)</a></td>'
        rankList = re.findall(patName2, data)

        patName3 = '<td class="xl-td-t5">(.*?)%</td>'
        percentList = re.findall(patName3, data)

        for j in range(len(rankList)):
            newList = []
            newList.append(count)
            count-=1
            newList.append(wholeList[3*j+1])
            newList.append(percentList[j])
            newList.append(rankList[j])
            print(newList)

            save_columns_to_csv(newList)

    except Exception as err:
        print(err)


if __name__ == '__main__':
    titleList = ['time', 'saleNumber', 'percent', 'rank']
    if os.path.exists(PATH):
        os.remove(PATH)
    save_columns_to_csv(titleList)
    carSaleList = []

    for i in range(8):
        spider(i)
