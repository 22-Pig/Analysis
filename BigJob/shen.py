import requests
from bs4 import BeautifulSoup
import pymysql


class LianJiaSpider():

    def __init__(self):
        # hd = {
        #     "user-agent":
        #     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
        # }
        self.headers = {
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

        self.mydb = pymysql.connect(host='localhost',
                                    user='root',
                                    passwd='123123',
                                    db='bigjob',
                                    charset='utf8')
        self.cur = self.mydb.cursor()

    # 1.获取网站信息返回soup
    def getHtmlText(self, url):
        try:
            r = requests.get(
                url,
                headers=self.headers,
            )
            r.encoding = r.apparent_encoding
            soup = BeautifulSoup(r.text, "html.parser")
            soup.prettify()
            return soup
        except:
            return "错误"

    def getRegion(self, burl):
        baseUrl = 'https://sx.lianjia.com'
        htmlText = self.getHtmlText(burl)
        ReginUrl = []
        ReginName = []

        Regin = (htmlText.select('div[data-role="ershoufang"]')
                 )[0].find('div').find_all('a')
        for i in Regin:
            ReginUrl.append(baseUrl + i.get('href'))
            ReginName.append((i.text).strip())

        return ReginUrl, ReginName

    def getTargetPage(self, qurl):
        htmlText = self.getHtmlText(qurl)
        targetDiv = htmlText.select(
            'div[class="page-box house-lst-page-box"]')  # 定位到targetPage的div
        targetDict = eval(targetDiv[0].get('page-data'))
        totoalpage = targetDict['totalPage']
        print(totoalpage)
        return totoalpage

    # 2.筛选出需要的数据，放在数组中返回
    def getInfo(self, htmlText, regin):
        houseInfoList = []
        liEl = htmlText.select('li[class="clear LOGVIEWDATA LOGCLICKDATA"]')

        for item in liEl:
            houseInfo = []
            title = item.find_all("div", attrs={'class': 'title'})
            positionInfo = item.find_all("div",
                                         attrs={'class': 'positionInfo'})
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
        # print(houseInfoList)
        return houseInfoList

    def createTable(self):
        # print('111')
        usedb = "use bigjob;"
        droptable = "DROP TABLE IF EXISTS `houseinfo2`;" 
        createSql = '''CREATE TABLE `houseinfo2`  (
                `Region` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
                `URL` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
                `Name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
                `Location` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
                `Type` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
                `Area` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
                `Orientation` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
                `DecorativeStyle` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
                `TotalPrice` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
                `AveragePrice` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL
                ) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;'''
        try:
            self.cur.execute(usedb)
            self.cur.execute(droptable)
            self.cur.execute(createSql)
            self.mydb.commit()
            # self.cur.close()
            # self.mydb.close()
        except:
            pass

    # 3.对数组中的数据进行存储
    def saveInfo(self, houseInfoList):
        insertSql = 'insert into houseinfo2 values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        self.cur.executemany(insertSql, houseInfoList)
        self.mydb.commit()
        # self.cur.close()
        # self.mydb.close()

    # 对数据库中的数据进行过滤
    def filterInfo(self):
        filterSql = '''DELETE FROM houseinfo2 WHERE Type LIKE '%车位%';'''
        self.cur.execute(filterSql)
        self.mydb.commit()
        self.cur.close()
        self.mydb.close()


if __name__ == '__main__':
    lianjia = LianJiaSpider()

    qurl = 'https://sx.lianjia.com/ershoufang/'
    ReginUrl, ReginName = lianjia.getRegion(qurl)
    print(ReginName)
    print(ReginUrl)
    print("爬取ing……")

    lianjia.createTable()
    for j in range(len(ReginUrl)):
        targetPage = lianjia.getTargetPage(ReginUrl[j])
        # print(targetPage)
        for i in range(1, targetPage + 1):
            url = ReginUrl[j] + 'pg' + str(i)
            htmlText = lianjia.getHtmlText(url)
            houseInfoList = lianjia.getInfo(htmlText, ReginName[j])
            lianjia.saveInfo(houseInfoList)
    print("爬取完成")
    lianjia.filterInfo()
    print("过滤完成")
