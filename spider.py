import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import pymongo
from multiprocessing.pool import Pool
import time

# chrome configs
prefs = {
    'profile.default_content_setting_values': {
        'images': 2,
        # 'javascript': 2
        # 'User-Agent': ua
    }
}
options = webdriver.ChromeOptions()
options.add_experimental_option('prefs', prefs)
# options.add_argument('--headless')

# databse config
client = pymongo.MongoClient('localhost', 27017)
porn = client['porn']
details = porn['details']
details.create_index('url')

def get_links(min_, max_):
    links = []
    for i in range(min_, max_):
        link = 'http://thz2.com/forum-220-{0}.html'.format(i)
        links.append(link)
    return links 


def page_next(d_url):
    browsers = webdriver.Chrome(chrome_options=options)
    browsers.get(d_url)
    pagecontents = browsers.page_source
    htmls = requests.get(d_url)
    if htmls.status_code == 200:
        pic = []
        files = []
        responses = BeautifulSoup(pagecontents, 'lxml')
        titles = responses.findAll('title')[0].get_text()
        torrents = responses.select('p.attnm > a')
        pattern_img = '^aimg_.*'
        for search_img in responses.find_all(id = re.compile(pattern_img)):
            if search_img.get('file'):
                pic_url = search_img.get('file')
                pic.append(pic_url)
        for to_url in torrents:
            t_url = 'http://thz2.com' + '/' + str(to_url.get('href'))
            t_file = page_next_torrent(t_url)
            files.append(t_file)
        if pic:
            time_p = pic[1].split('/')[4:7]
            time_img = time_p[0] + time_p[1] + time_p[2]    
            data = {
                'num': str(titles).split(']')[0].replace('[', ''),
                'title': str(titles).split(']')[1].replace('Taohuazu_桃花族 -  thz.la', ''),
                'file': files,
                'picture': pic,
                'time': time_img,
                'url': d_url
            }
            updatedata(data)
    browsers.close()


def page_next_torrent(url):
    requests.adapters.DEFAULT_RETRIES = 10
    files = requests.get(url)
    contents = BeautifulSoup(files.text, 'lxml')
    pattern_torrent =re.compile('http:\/\/thz2\.com\/forum\.php.*') 
    all_links = contents.findAll('a')
    for item in all_links:
        if re.search(pattern_torrent, str(item.get('href'))):
            result = re.search(pattern_torrent, str(item.get('href')))
            results = result.group(0)
    return results


def updatedata(data):
    if data:
        if porn['details'].update({'url': data['url']}, {'$set': data}, True):
            print('=======================================================================================\n')
            print('更新存储到数据库成功,目前文档数:{}\t\n'.format(porn['details'].find().count()))
            print('=======================================================================================\n')
            print('数据展示:\n\n', data)
            return True
        else:
            print('数据不存在,无法存储到数据库,请检查是否匹配成功') 




# 6-n
def spider(start_url):
    browser = webdriver.Chrome(chrome_options=options)
    browser.get(start_url)
    htmlcontents = browser.page_source
    html = requests.get(start_url)
    if html.status_code == 200:
        urls = []
        response = BeautifulSoup(htmlcontents, 'lxml')
        link_next = response.find_all('a')
        pattern = re.compile(r'^thread-\d+-\d-\d\.html')
        for item in link_next:
            if re.search(pattern, str(item.get('href'))):
                results = re.search(pattern, str(item.get('href')))
                result = results.group(0)
                domainNew = 'http://thz2.com' + '/' + result
                urls.append(domainNew)
        pool = Pool(2)
        pool.map(page_next, set(urls))
        # for item_ in set(urls):
        #     page_next(item_)
        browser.close()
   

if __name__ == '__main__':
    links = get_links(6,10)
    for item in links:
        spider(item)
