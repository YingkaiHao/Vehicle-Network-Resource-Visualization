import requests
from bs4 import BeautifulSoup
import csv
import os
import re

PATH = '../allBrandsInformation.csv'

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
    url = 'http://auto.16888.com/'
    data = getHTML(url)
    soup = BeautifulSoup(data, 'lxml')

    try:
        numberList = []

        patName1 = '<a name="(.*?)" style="margin-top: -\d*px; display: block; float: right;"></a>'
        pat1 = re.compile(patName1)
        name = pat1.findall(data)
        print(name)

        List1 = soup.find_all('em')
        for each in List1:
            patName2 = '<em>(\d+)</em>'
            pat2 = re.compile(patName2)
            number = pat2.findall(str(each))
            if bool(number) == True:
                numberList.append(number[0])
        print(numberList)

        patName3 = '<a target="_blank" href="https(.*?)"><img src="//i.img16888.com/carlogo/.*?.gif"></a>'
        pat3 = re.compile(patName3)
        webSiteList = pat3.findall(data)
        print(webSiteList)

        for i in range(len(webSiteList)):
            basicUrl = 'http'
            brandUrl = webSiteList[i]
            commonUrl = (f'{basicUrl}{brandUrl}')
            brandData = getHTML(commonUrl)

            patName4 = '<a target="_blank" href="https://www.16888.com/.*?/" title="(.*?)">'
            pat4 = re.compile(patName4)
            brandNameList = pat4.findall(brandData)
            print(brandNameList)

            patName5 = '<!-- 未上市加上class “not”-->\s+<a target="_blank" href="https://price.16888.com/.*?/" class="f_red f_14">(.*?)</a>'
            brandPriceList = re.findall(patName5, brandData, re.S)
            newBrandPriceList = []
            for m in range(len(brandPriceList)):
                str_new = brandPriceList[m].replace(" ", "")
                str_new1 = "".join(str_new.split())
                str_new2 = str_new1.replace("万", "")
                newBrandPriceList.append(str_new2)
            print(newBrandPriceList)

            for n in range(len(brandNameList)):
                newList = []
                newList.append(name[i])
                newList.append(numberList[i])
                newList.append(brandNameList[n])
                newList.append(newBrandPriceList[n])
                print(newList)

                save_columns_to_csv(newList)

    except Exception as err:
        print(err)

if __name__ == '__main__':
    titleList = ['品牌', '4S店数', '车型', '报价(单位：万)']
    if os.path.exists(PATH):
        os.remove(PATH)
    save_columns_to_csv(titleList)

    spider()
