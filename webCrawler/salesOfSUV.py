import requests
from bs4 import BeautifulSoup
import csv
import os
import re

PATH = '../SUV销量/SUV销量(2019.01-2019.12).csv'

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
    j = i+1
    url1 = 'https://xl.16888.com/body-5-201901-201912-'
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

        List1 = soup.find_all('td', attrs={'class': 'xl-td-t1'})
        for each in List1:
            # print(each)
            patName = '<td class="xl-td-t1">(.*?)</td>'
            pat = re.compile(patName)
            number = pat.findall(str(each))[0]
            numberList.append(number)

        List2 = soup.find_all('td', attrs={'class': 'xl-td-t2'})
        for each in List2:
            patName2 = 'target="_blank">(.*?)</a></td>'
            pat2 = re.compile(patName2)
            name = pat2.findall(str(each))[0]
            nameList.append(name)

        List3 = soup.find_all('td', attrs={'class': 'xl-td-t3'})
        for each in List3:
            patName3 = '<td class="xl-td-t3">(.*?)</td>'
            pat3 = re.compile(patName3)
            sale = pat3.findall(str(each))[0]
            saleList.append(sale)

        List4 = soup.find_all('td', attrs={'class': 'xl-td-t5'})
        for each in List4:
            patName4 = 'target="_blank">(.*?)</a>'
            pat4 = re.compile(patName4)
            price = pat4.findall(str(each))[0]
            priceList.append(price)

        for i in range(int(len(List1))):
            newList = []
            newList.append(numberList[i])
            newList.append(nameList[2 * i])
            newList.append(saleList[i])
            newList.append(nameList[2 * i + 1])
            newList.append(priceList[i])

            save_columns_to_csv(newList)

    except Exception as err:
        print(err)


if __name__ == '__main__':
    titleList = ['排名', '车型', '销量', '厂商', '售价(万元)']
    if os.path.exists(PATH):
        os.remove(PATH)
    save_columns_to_csv(titleList)
    carSaleList = []

    for i in range(8):
        spider(i)
