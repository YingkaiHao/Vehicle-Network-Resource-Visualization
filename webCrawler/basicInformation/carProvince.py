import json

import requests
from bs4 import BeautifulSoup
import operator
import csv
import os
import re

PATH = '../基本信息相关/品牌4S店/众泰.csv'

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
    url = 'http://dealer.16888.com/?tag=search&extra=getCity&regionId=0&bid=58085&fid=0&sid=0&nature=0'
    data = getHTML(url)
    # soup = BeautifulSoup(data, 'lxml')

    try:
        newData = data.encode('utf-8').decode('unicode_escape')
        print(newData)
        patName1 = '"region_name":"(.*?)",'
        provinceList = re.findall(patName1, str(newData))
        newProvinceList = []
        for i in range(len(provinceList)):
            if provinceList[i] == "中国":
                continue
            elif provinceList[i] == "全国":
                continue
            elif provinceList[i] == provinceList[i-1]:
                continue
            else:
                newProvinceList.append(provinceList[i])
        print(len(newProvinceList))

        patName2 = '"total":"(\d+)"}'
        numberList = re.findall(patName2, newData)
        # numberList.insert(26, "0")
        print(len(numberList))

        for j in range(len(newProvinceList)):
            newList = []
            newList.append(newProvinceList[j])
            newList.append(numberList[j])
            print(newList)

            save_columns_to_csv(newList)
    except Exception as err:
        print(err)

if __name__ == '__main__':
    titleList = ['province', '4SNumber']
    if os.path.exists(PATH):
        os.remove(PATH)
    save_columns_to_csv(titleList)

    spider()
