import requests
from bs4 import BeautifulSoup
import pymysql


# 1.获取网站信息返回soup
def getHtmlText(url):
    try:
        # hd = {
        #     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
        #     # "Cookie":'SECKEY_ABVK=W7NmvxNqaC5httO4f3UHWbA+iE4G7iTtl5CoAMxPPT0=; BMAP_SECKEY=rYW6jU47njF9Kz7OBzSCMtpSP8kEDc67WoATlUQCTi-zuOB02gHiAVwmYJb3_l29ghQA0g7SecGcOvOQmh2NnVOXMPzXeFM7YuwDVa4Eb_8XHiZCw3q39Rae7rN59l-miWQsiJ19ESSFHK-ifDVz6zLpEQkRSi69wwIMTmYsvVL10zJHlo3xocAoMEC1YeAo; lianjia_uuid=c95919fa-5dba-4fa7-a1e0-4dc0112b55f9; _smt_uid=635924f4.25c68b33; sensorsdata2015jssdkcross={"distinct_id":"18414385b9513a1-0971dc40fe05af-26021f51-1638720-18414385b9615b3","$device_id":"18414385b9513a1-0971dc40fe05af-26021f51-1638720-18414385b9615b3","props":{"$latest_traffic_source_type":"直接流量","$latest_referrer":"","$latest_referrer_host":"","$latest_search_keyword":"未取到值_直接打开"}}; _ga=GA1.2.1520885693.1666786550; select_city=330600; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1666786549,1666920635; _gid=GA1.2.1692001318.1666920636; lianjia_ssid=70da1fed-e4d1-49f6-8c1e-74c852216ad2; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1666933914; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiYmVkYzM3YmY5NGFkZjRlOWJlY2MwNWEzYmI0OWQ0YTRkYmNhMDQxZTgwNjg2MmYwMDFmMTQ0M2FjZjYxY2YxNjU4ZTE4NmVmYTljZjhkYjhjYjJhMTU4NDliYWExYzY4MTA1MWNjYTEzZjM5ZmExMWM0OThmOTM1YjU3ZmE5NDE0YmRhOTY1Njc5M2I5MzYyYWM2ZDhhMzNlMDQyOGZjMDQ5YmRlN2QzNWRiZDcyMzg5MzkxYjQ3NjcxZWI5MDc4MTY0OGUyYTE3NWZiNDNmODIzYjRlNjcwNTI4OTEyYzUwODljZWUzZGU4MzE2N2Y2OGFhZDhhNzRkOGIyMTcwZVwiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCJiYTQ0NjhhN1wifSIsInIiOiJodHRwczovL3N4LmxpYW5qaWEuY29tL2Vyc2hvdWZhbmcvc2hhbmd5dXF1LyIsIm9zIjoid2ViIiwidiI6IjAuMSJ9',
        #     # "host":'sx.lianjia.com'
        # }

        hd = header = {
            'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding':
            'gzip, deflate, br',
            'Accept-Language':
            'zh-CN,zh;q=0.9',
            'Connection':
            'keep-alive',
            'Cookie':
            'lianjia_uuid=07e69a53-d612-4caa-9145-b31c2e9410f4; _smt_uid=5c2b6394.297c1ea9; UM_distinctid=168097cfb8db98-058790b6b3796c-10306653-13c680-168097cfb8e3fa; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1546347413; _ga=GA1.2.1249021892.1546347415; _gid=GA1.2.1056168444.1546347415; all-lj=c60bf575348a3bc08fb27ee73be8c666; TY_SESSION_ID=d35d074b-f4ff-47fd-9e7e-8b9500e15a82; CNZZDATA1254525948=1386572736-1546352609-https%253A%252F%252Fbj.lianjia.com%252F%7C1546363071; CNZZDATA1255633284=2122128546-1546353480-https%253A%252F%252Fbj.lianjia.com%252F%7C1546364280; CNZZDATA1255604082=1577754458-1546353327-https%253A%252F%252Fbj.lianjia.com%252F%7C1546366122; lianjia_ssid=087352e7-de3c-4505-937e-8827e808c2ee; select_city=440700; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1546391853',
            'DNT':
            '1',
            'Host':
            'sx.lianjia.com',
            'Referer':
            'https://sx.lianjia.com/',
            'Upgrade-Insecure-Requests':
            '1',
            'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
        }
        r = requests.get(url, headers=hd)
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, "html.parser")
        soup.prettify()
        return soup
    except:
        return "错误"


def getRegion(burl):
    baseUrl = 'https://sx.lianjia.com'
    htmlText = getHtmlText(burl)
    ReginUrl = []
    ReginName = []

    Regin = (htmlText.select('div[data-role="ershoufang"]')
             )[0].find('div').find_all('a')
    for i in Regin:
        ReginUrl.append(baseUrl + i.get('href'))
        ReginName.append((i.text).strip())

    return ReginUrl, ReginName


def getTargetPage(qurl):
    htmlText = getHtmlText(qurl)
    targetDiv = htmlText.select(
        'div[class="page-box house-lst-page-box"]')  # 定位到targetPage的div
    # totoalpage = eval(targetDiv[0].get('page-data'))['totalPage']  # 获取targetPage
    targetDict = eval(targetDiv[0].get('page-data'))
    totoalpage = targetDict['totalPage']
    return totoalpage


# 2.筛选出需要的数据，放在数组中返回
def getInfo(htmlText, regin):
    houseInfoList = []
    # lianjiaHtml = open('./lianjia.html', 'r', encoding='utf-8')
    # lianjiaHtmlText = lianjiaHtml.read()
    # soup = BeautifulSoup(lianjiaHtmlText, "html.parser")
    liEl = htmlText.select('li[class="clear LOGVIEWDATA LOGCLICKDATA"]')

    for item in liEl:
        ''' 
        houseInfo = {}
        title = item.find_all("div",attrs={'class':'title'})
        positionInfo = item.find_all("div",attrs={'class':'positionInfo'})
        baseInfo = item.find_all("div",attrs={'class':'houseInfo'})
        priceInfo = item.find_all("div",attrs={'class':'priceInfo'})

        houseInfo['url']=title[0].find('a').get('href')
        houseInfo['houseName'] = (positionInfo[0].text).split('-')[0].strip()
        houseInfo['houseAddress'] = (positionInfo[0].text).split('-')[1].strip()
        houseInfo['houseType'] = (baseInfo[0].text).split('|')[0].strip()
        houseInfo['houseArea'] = (baseInfo[0].text).split('|')[1].strip()
        houseInfo['houseDirection'] = (baseInfo[0].text).split('|')[2].strip()
        houseInfo['houseDecoration'] = (baseInfo[0].text).split('|')[3].strip()
        houseInfo['houseTotal'] = (priceInfo[0].text).split('万')[0].strip()+'万'
        houseInfo['housePrice'] = (priceInfo[0].text).split('万')[1].strip()

        houseInfoList.append(houseInfo)
        '''
        houseInfo = []
        title = item.find_all("div", attrs={'class': 'title'})
        positionInfo = item.find_all("div", attrs={'class': 'positionInfo'})
        baseInfo = item.find_all("div", attrs={'class': 'houseInfo'})
        priceInfo = item.find_all("div", attrs={'class': 'priceInfo'})

        houseInfo.append(regin)
        houseInfo.append(title[0].find('a').get('href'))
        houseInfo.append((positionInfo[0].text).split('-')[0].strip())
        houseInfo.append((positionInfo[0].text).split('-')[1].strip())
        houseInfo.append((baseInfo[0].text).split('|')[0].strip())
        houseInfo.append((baseInfo[0].text).split('|')[1].strip())
        houseInfo.append((baseInfo[0].text).split('|')[2].strip())
        houseInfo.append((baseInfo[0].text).split('|')[3].strip())
        houseInfo.append((priceInfo[0].text).split('万')[0].strip() + '万')
        houseInfo.append((priceInfo[0].text).split('万')[1].strip())
        houseInfo = tuple(houseInfo)
        houseInfoList.append(houseInfo)
        # print(title[0].find('a').get('href'))     # 链接
        # print((positionInfo[0].text).split('-')[0])   # 小区名称
        # print((positionInfo[0].text).split('-')[1].strip())   #小区位置
        # print((baseInfo[0].text).split('|')[0]) #户型
        # print((baseInfo[0].text).split('|')[1].strip()) #面积
        # print((baseInfo[0].text).split('|')[2].strip()) #朝向
        # print((baseInfo[0].text).split('|')[3].strip()) #装修
        # print((priceInfo[0].text).split('万')[0].strip()+'万')  #总价
        # print((priceInfo[0].text).split('万')[1].strip())    #单价

    print(houseInfoList)
    return houseInfoList


# 3.对数组中的数据进行存储
def saveinfo(houseInfoList):
    con = pymysql.connect(host='localhost',
                          user='root',
                          password='1111',
                          db='链家数据',
                          charset='utf8')

    cur = con.cursor()
    insert_sal = 'insert into houseinfo values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    cur.executemany(insert_sal, houseInfoList)
    con.commit()
    cur.close()
    con.close()

    # with open('./houseInfoList1.txt','wb') as f:
    #     f.write('666')


def main():
    # baseUrl = 'https://sx.lianjia.com/'
    qurl = 'https://sx.lianjia.com/ershoufang/shangyuqu/'
    # qurl = 'https://nb.lianjia.com/ershoufang/haishuqu1/'
    # qurl = 'https://hz.lianjia.com/ershoufang/xihu/'
    ReginUrl, ReginName = getRegion(qurl)
    print(ReginName)
    print(ReginUrl)
    for j in range(len(ReginUrl)):
        targetPage = getTargetPage(ReginUrl[j])
        print(targetPage)
        for i in range(1, targetPage + 1):
            url = ReginUrl[j] + 'pg' + str(i)
            htmlText = getHtmlText(url)
            houseInfoList = getInfo(htmlText, ReginName[j])
            saveinfo(houseInfoList)

    # saveinfo('555')


main()
