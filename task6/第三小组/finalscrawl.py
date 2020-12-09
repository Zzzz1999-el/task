'''
大众点评爬虫+svg反加密
Version: 1.0.0
Author: Lynn
'''

from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import re
import pandas as pd
import time
from random import randint
import xlwt
from multiprocessing import Process


#抓取指定区域和菜系下所有商户的评论
'''
Input: 
    (dict)shop_codes:指定区域和菜系下的所有商户的代码
    (int)start:开始爬取的序号
    (int)end:结束爬取的序号
Output:

'''

def review_get(shop_codes,start = 0,end = None):
    # 登录模块
    browser = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')

    browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
    Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
    })
    """
    })

    url = 'https://account.dianping.com/login'
    browser.get(url)
    time.sleep(30)
    #shop_codes = get_shop_codes(init_url, browser)
    if end == None:
        end = len(shop_codes)
    count = 0
    for shop_name in shop_codes:
        count += 1
        if count <= start:
            continue
        get_shop_review(shop_codes[shop_name], shop_name, browser)
        if count == end:
            print(f'{start}-{end}DONE!')
            break

        


#抓取指定区域和菜系下所有商户的代码
'''
Input: 
    (str)init_url:指定区域和菜系的url
    browser:webdriver所控制的浏览器
Output:
    (dict)shop_codes:指定区域和菜系下的所有商户的代码
'''
def get_shop_codes(init_url, browser):
    shop_codes = {}
    url = init_url
    while True:
        time.sleep(randint(1,3))
        browser.get(url)
        soup = BeautifulSoup(browser.page_source, "html.parser")
        shop_codes_init = soup.find_all('a', {'data-click-name':{'shop_title_click'}})
        for code in shop_codes_init:
            shop_name = code['title']
            shop_code = code['data-shopid']
            shop_codes[shop_name] = shop_code

        next_url = soup.find_all('a', class_ = 'next')
        if next_url == []:
            break
        url = next_url[0]['href']
    
    return shop_codes


#抓取指定商户下的所有评论(解密后)
'''
Input:
    (str)shop_code:指定商户的代码
    (str)shop_name:指定商户的名称
    browser:webdriver所控制的浏览器
Output:
    (data.frame)reviews:商户下所有用户名称、评分及评论
'''
def get_shop_review(shop_code,shop_name, browser):
    url = 'http://www.dianping.com/shop/' + shop_code + '/review_all'
    browser.get(url)
    class_word = decrypt_dict(browser)
    dic = {'shop_name':[],'user_name':[], 'review_time':[], 'user_scores':[], 'user_review':[]}
    while True:
        #print(url)
        soup = BeautifulSoup(browser.page_source,'lxml')
        get_comments(soup, dic, class_word)
        #count += 1
        #if count == 50:
        #    break
        if soup.find('a',class_ = 'NextPage') == None:
            break
        nextpage = soup.find('a',class_ = 'NextPage')['href']
        url = 'http://www.dianping.com' + nextpage
        time.sleep(1)
        browser.get(url)
    dic['shop_name'] = [shop_name]*len(dic['user_name'])
    reviews = pd.DataFrame(dic)
    reviews.to_excel('~/Downloads/dianpingData/Beijing_Japanese_Review/'+shop_name+'_new.xls')
    #return reviews

#抓取商户指定页面的所有评论并解密
'''
Input:
    (bs4)soup:解析的html
    (dict)dic:用来储存抓取下来的用户名称、评分和评论
    (dict)class-word:class-字体的字典
'''
def get_comments(soup,dic,class_word):
    items = soup.find_all('div', class_ = 'main-review')
    length = len(items)
    for i in items:
        dic['user_name'].append(i.find('a',class_ = 'name').contents[0].strip())
        dic['review_time'].append(i.find('span', class_ = 'time').text.strip())
        if i.find('span',class_ = 'score') == None:
            dic['user_scores'].append('N/A')
        elif len(i.find('span',class_ = 'score').contents) == 5:
            dic['user_scores'].append('\n'.join([i.find('span',class_ = 'score').contents[j].contents[0].strip() for j in [1,3]]))
        elif len(i.find('span',class_ = 'score').contents) == 3:
            dic['user_scores'].append('\n'.join([i.find('span',class_ = 'score').contents[1].contents[0].strip()]))
        else:
            dic['user_scores'].append('\n'.join([i.find('span',class_ = 'score').contents[j].contents[0].strip() for j in [1,3,5]]))
        comment_ls = []
        
        if i.find('div', class_ = 'review-words Hide') == None:
            comment = i.find('div', class_ = 'review-words').contents
        else:
            comment = i.find('div', class_ = 'review-words Hide').contents
        
        for j in comment:
            if j.name == 'svgmtsi':
                comment_ls.append(class_word[j['class'][0]])
            elif str(type(j)) == "<class 'bs4.element.NavigableString'>":
                comment_ls.append(str(j))

        #comment_ls.pop(-2)
        dic['user_review'].append(''.join(comment_ls).strip())
        #dic['user_comment'].append(comment_ls)

#构建svg字体加密字典
'''
Input:
    browser:webdriver所控制的浏览器
Output:
    (dict)class_word:class_name到字体的字典
'''
def decrypt_dict(browser):
    #抓取页面中svg的width和height
    js_script_wh = '''
    var a = document.querySelector('svgmtsi')
    var b = a.getBoundingClientRect()
    return [b.width, b.height]
    '''
    svg = browser.execute_script(js_script_wh)
    svg_width = int(svg[0])
    svg_height = int(svg[1])
    soup = BeautifulSoup(browser.page_source, 'html.parser')

    #抓取页面中的css文件的url
    css_url = 'http:' + soup.select('link[href*="svgtextcss"]')[0]['href']
    #print(css_url)
    #抓取页面中的svg文件的url
    js_script_svg = '''
    var a = document.querySelector('svgmtsi')
    var url = window.getComputedStyle(a).backgroundImage
    return url
    '''
    svg_url = browser.execute_script(js_script_svg)[5:-2]

    #构建class_name到字体的映射词典

    class_word = {}
    web_data_css = requests.get(css_url).text
    soup_css = BeautifulSoup(web_data_css, 'html.parser')
    souptext = re.sub(r'\.0px', '', soup_css.text)
    class_name = re.findall(r'\.\w+\{', souptext)
    coordinate = re.findall(r'[+-]\d+.[+-]\d+', souptext)

    web_data_svg = requests.get(svg_url).text
    soup_svg = BeautifulSoup(web_data_svg, 'html.parser')
    

    #将css中的坐标映射到svg中的字体
    for i in range(len(coordinate)):
        x = -int(coordinate[i].split(' ')[0])/svg_width
        y = -int(coordinate[i].split(' ')[1])+svg_height-1
        #y_svg = soup_svg.find('path', d = 'M0 ' +str(y)+' H600')
        #if y_svg == None:
        #    continue
        #word = soup_svg.find('textpath', {'xlink:href':{'#' + y_svg['id']}}).text[int(x)]
        word_init = soup_svg.find('text', y=str(y))
        if word_init == None:
            continue
        word = soup_svg.find('text', y = str(y)).text[int(x)]
        class_word[class_name[i][1:-1]] = word

    return class_word

if __name__  == '__main__':
    #评论抓取并储存
    ############################################################################
    browser = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')

    browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
    Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
    })
    """
    })

    url = 'https://account.dianping.com/login'
    browser.get(url)
    time.sleep(30)
    shop_codes = get_shop_codes('http://www.dianping.com/beijing/ch10/g113', browser)
    p1 = Process(target = review_get, args = (shop_codes,0,200))
    p2 = Process(target = review_get, args=(shop_codes, 200, 400))
    p3 = Process(target = review_get, args=(shop_codes, 400, 600))

