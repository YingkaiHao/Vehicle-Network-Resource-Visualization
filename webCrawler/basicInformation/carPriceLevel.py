import requests
from bs4 import BeautifulSoup
import operator
import csv
import os
import re

PATH = '../carPriceLevel.csv'

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
    url = 'http://auto.16888.com/price.html'
    data = getHTML(url)
    soup = BeautifulSoup(data, 'lxml')

    try:
        levelList = []
        patName1 = '<a href="#.*?">(.*?)</a>'
        pat1 = re.compile(patName1)
        level = pat1.findall(data)

        for i in range(12):
            levelList.append(level[i])
        print(levelList)

        patName2 = '<div class="brand_box">(.*?)</div>'
        content = re.findall(patName2, data, re.S)

        allModelList = []
        allPriceList = []
        for each in range(len(content)):
            patName3 = '<a target="_blank" href="https://www.16888.com/.*?/" title=".*?">(.*?)</a>'
            model = re.findall(patName3, content[each])
            allModelList.append(model)

            patName4 = '<p.*?>(.*?)</p>'
            price = re.findall(patName4, content[each])
            eachPriceList = []
            for j in range(len(price)):
                if operator.eq(price[j], "暂无报价"):
                    eachPriceList.append(price[j])
                else:
                    patName5 = '<a href="https://price.16888.com/.*?.html" target="_blank">(.*?)&nbsp;-&nbsp;(.*?)万</a>'
                    havePrice = re.findall(patName5, price[j])
                    eachPriceList.append(havePrice[0])
            allPriceList.append(eachPriceList)
        print(allModelList)
        print(allPriceList)

        for i in range(len(levelList)):
            newModelList = allModelList[i]
            newPriceList = allPriceList[i]
            for j in range(len(newModelList)):
                newList = []
                newList.append(levelList[i])
                newList.append(newModelList[j])
                newList.append(newPriceList[j])

                print(newList)
                save_columns_to_csv(newList)
    except Exception as err:
        print(err)

if __name__ == '__main__':
    titleList = ['价格区间', '车型', '报价(单位：万)']
    if os.path.exists(PATH):
        os.remove(PATH)
    save_columns_to_csv(titleList)

    spider()
