import requests
from bs4 import BeautifulSoup
import operator
import csv
import os
import re

PATH = '../基本信息相关/diffCountry.csv'

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
    url = 'http://auto.16888.com/country.html'
    data = getHTML(url)
    soup = BeautifulSoup(data, 'lxml')

    try:
        patName1 = '<a href="#(.*?)"'
        country = re.findall(patName1, data)
        countryList = []
        for each in range(12):
            countryList.append(country[each])
        print(countryList)

        patName2 = '<li  class="clearfix">(.*?)</li>'
        patName3 = '<li style="display: block;" class="clearfix">(.*?)</li>'
        brand1 = re.findall(patName3, data, re.S)
        brand2 = re.findall(patName2, data, re.S)
        brand = []
        brand.append(brand1)
        for each in range(11):
            brand.append(brand2[each])

        brandList = []
        for each in range(len(brand)):
            patName4 = '<a href="#.*?">(.*?)</a>'
            smallBrandList = re.findall(patName4, str(brand[each]), re.S)
            brandList.append(smallBrandList)
        print(brandList)

        patName5 = '<ul class="last">(.*?)</ul>'
        type = re.findall(patName5, data, re.S)
        print(len(type))

        modelList = []
        priceList = []
        for each in type:
            patName6 = 'href="https://www.16888.com/.*?/" title="(.*?)">.*?<'
            model = re.findall(patName6, each)
            modelList.append(model)

            patName7 = '<p.*?>(.*?)</p>'
            price = re.findall(patName7, each)
            eachPriceList = []
            for j in range(len(price)):
                if operator.eq(price[j], "暂无报价"):
                    eachPriceList.append(price[j])
                else:
                    patName5 = '<a target="_blank" href="https://price.16888.com/sr-.*?.html">(.*?)万</a>'
                    havePrice = re.findall(patName5, price[j])
                    eachPriceList.append(havePrice[0])
            priceList.append(eachPriceList)
        print(modelList)
        print(priceList)

        for x in range(len(countryList)):
            index1 = len(brandList[x])
            List1 = brandList[x]
            for i in List1:
                newList = []
                newList.append(countryList[x])
                newList.append(i)
                print(newList)
                save_columns_to_csv(newList)


    except Exception as err:
        print(err)

if __name__ == '__main__':
    titleList = ['国别', '品牌']
    if os.path.exists(PATH):
        os.remove(PATH)
    save_columns_to_csv(titleList)

    spider()
