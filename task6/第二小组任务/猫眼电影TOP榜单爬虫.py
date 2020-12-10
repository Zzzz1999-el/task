import requests
import re
import xlwt

url='https://maoyan.com/board/4?'
headers={
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
        }
        
def get_page(url):
    try:
        response=requests.get(url,headers=headers)
        if response.status_code==200:
            return response.text
        else:
            print('获取网页失败')
    except Exception as e:
        print(e)
        
def get_info(page):
    items=re.findall('board-index .*?>(\d+)</i>.*?class="name"><.*?>(.*?)</a></p>.*?<p class="star">.*?'+
                     '主演：(.*?) .*?</p>.*?<p class="releasetime">(.*?)</p>.*?<p class="score"><i class="integer">'+
                     '(.*?)</i><i class="fraction">(\d+)</i></p>',page,re.S)
    for item in items:
        data={}
        data['rank']=item[0]
        data['title']=item[1]
        actors=re.sub('\n','',item[2])
        data['actors']=actors
        data['date']=item[3]
        data['score']=str(item[4])+str(item[5])
        yield data           

# 获取前3页的电影数据
urls=['https://maoyan.com/board/4?offset={}'.format(i*10) for i in range(3)]
DATA=[]
for url in urls:   
    page=get_page(url)
    datas=get_info(page)
    for data in datas:
        DATA.append(data) #将所有的数据添加到DATA里

f=xlwt.Workbook(encoding='utf-8')
sheet01=f.add_sheet(u'sheet1',cell_overwrite_ok=True)
sheet01.write(0,0,'rank') #第一行第一列
sheet01.write(0,1,'title')
sheet01.write(0,2,'actors')
sheet01.write(0,3,'date')
sheet01.write(0,4,'score')  
#写内容
for i in range(len(DATA)):
    sheet01.write(i+1,0,DATA[i]['rank'])
    sheet01.write(i+1,1,DATA[i]['title'])
    sheet01.write(i+1,2,DATA[i]['actors'])
    sheet01.write(i+1,3,DATA[i]['date'])
    sheet01.write(i+1,4,DATA[i]['score'])
    print('p',end='')
f.save('/Users/sonder/Downloads/猫眼电影.xlsx')

