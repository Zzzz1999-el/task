# Task6 爬虫:豆瓣电影TOP250

## 1.准备工作

## 1.1 导入模块


```python
from bs4 import BeautifulSoup
import re
import urllib.error
from urllib.request import urlopen, Request
import xlwt
import sqlite3
```

## 1.2 设置工作路径


```python
#设置工作路径
import os
os.chdir("C:/Users/kol/Desktop")
print(os.getcwd())
```

## 1.3 用正则表达式进行预编译


```python
#创建正则表达式对象， 表示规则（字符串的格式）
#影片链接
findLink =re.compile(r'<a href="(.*?)">')      
#影片图片
findImgsrc =re.compile(r'<img.*src="(.*?)"',re.S)
#影片片名
findTitle = re.compile(r'<span class="title">(.*)</span>')
#影片评分
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
#评价人数
findJudge =re.compile(r'<span>(\d*)人评价</span>')
#概述
findInq =re.compile(r'<span class="inq">(.*)</span>')
#相关内容
findBd =re.compile(r'<p class="">(.*?)</p>',re.S)
```

## 2.爬取网页


```python
# -*- coding: utf-8 -*-

#爬取网页
def main():
    baseurl = 'https://movie.douban.com/top250?start='
    datalist = getData(baseurl)
    savepath = "豆瓣电影Top250.xls "
    saveData(datalist,savepath)
    askURL('https://movie.douban.com/top250?start=')


def getData(baseurl):
    datalist = []
    for i in range(0,10):   #获取页面信息的函数，调用25次
        url = baseurl + str(i*25)
        html = askURL(url) #保存获取到的网页源码
        soup = BeautifulSoup(html,"html.parser")
        for item in soup.find_all('div',class_="item"):  #查找符合要求的字符串
            #print(item)
            data = [] #保存一部电影的所有信息
            item = str(item)
            #获取影片链接
            link = re.findall(findLink,item)[0]  #re库用来查找指定字符串
            data.append(link)
            #影片图片
            imgsrc =re.findall(findImgsrc,item)[0]
            data.append(imgsrc)
            #片名
            title =re.findall(findTitle,item)
            if(len(title) ==2):
                ctitle = title[0]     #中文名
                data.append(ctitle)     #外文名
                otitle = title[1].replace("/","")  #去掉无关的/
                data.append(otitle)
            else:
                data.append(title[0])
                data.append(' ')  #外国名留空

            #评价分数
            rating = re.findall(findRating,item)[0]
            data.append(rating)
            #评价人数
            judgeNum =re.findall(findJudge,item)[0]
            data.append(judgeNum)
            #概述
            inq =re.findall(findInq,item)
            if len(inq) !=0:
                inq =inq[0].replace("。","")
                data.append(inq)
            else:
                data.append(" ")

            bd =re.findall(findBd,item)[0]
            bd =re.sub('<br(\s+)?/>(\s+)?'," ",bd)  #去掉br
            bd =re.sub('/'," ",bd)  #替换/
            data.append(bd.strip())   #去掉空格
            datalist.append(data)   #把处理好的一部电影信息放回去
    return  datalist

def askURL(url):
    head = {
        'User-Agent': "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Mobile Safari/537.36"}
    request = Request(url, headers=head)
    html = ''
    try:
        respose = urlopen(request)
        html = respose.read().decode("utf-8")
        #print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html

#保存数据为xls
def saveData(datalist, savepath):
    book = xlwt.Workbook(encoding="utf-8",style_compression=0)  # 创建workbook对象
    sheet = book.add_sheet('豆瓣电影Top 250 ',cell_overwrite_ok=True)
    col =("电影详情链接","图片链接","影片中文名","影片外国名 ","评分","评价数","概况","相关信息")
    for i in range(0,8):
        sheet.write(0,i,col[i])
    for i in range(0,250):
        print("第%d条" %(i+1))
        data = datalist[i]
        for j in range(0,8):
            sheet.write(i+1,j,data[j])
    book.save('豆瓣电影Top 250.xls')  #保存
    print(" ")

#运行主程序
if __name__ == '__main__':
    main()
```
