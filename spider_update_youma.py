import re
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

from spider import porn, details


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


def get_links_update():
    links = []
    for i in range(1, 5):
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
        torrents = responses.select('p.attnm > a')
        pattern_img = '^aimg_.*'
        for search_img in responses.find_all(id=re.compile(pattern_img)):
            if search_img.get('file'):
                pic_url = search_img.get('file')
                pic.append(pic_url)
        for to_url in torrents:
            t_url = 'http://thz2.com' + '/' + str(to_url.get('href'))
            t_file = page_next_torrent(t_url)
            files.append(t_file)
        data = {
            'download': files,
            'pictures': pic
        }
    browsers.close()
    return data


def page_next_torrent(url):
    requests.adapters.DEFAULT_RETRIES = 5
    files = requests.get(url)
    contents = BeautifulSoup(files.text, 'lxml')
    pattern_torrent = re.compile('http:\/\/thz2\.com\/forum\.php.*')
    all_links = contents.findAll('a')
    for item in all_links:
        if re.search(pattern_torrent, str(item.get('href'))):
            result = re.search(pattern_torrent, str(item.get('href')))
            results = result.group(0)
    return results


def updatedata(data):
    if porn['details'].update({'url': data['url']}, {'$set': data}, True):
        print('=======================================================================================\n')
        print('更新存储到数据库成功,目前文档数:{}\t\n'.format(porn['details'].find().count()))
        print('=======================================================================================\n')
        print('数据展示:\n\n', data)
        return True
    else:
        print('数据不存在,无法存储到数据库,请检查是否匹配成功')


def spider_update(start_url):
    browser = webdriver.Chrome(chrome_options=options)
    browser.get(start_url)
    htmlcontents = browser.page_source
    html = requests.get(start_url)
    if html.status_code == 200:
        response = BeautifulSoup(htmlcontents, 'lxml')
        pattern = '^normalthread_.*'
        for search_id in response.find_all(id = re.compile(pattern)):
            _links = response.select("#{} > tr > th > a.s.xst".format(search_id.get('id')))
            updateTime = response.select('#{} > tr > td > em > span > span'.format(search_id.get('id')))
            clicks = response.select('#{} > tr > td.num > em'.format(search_id.get('id')))
            title = response.select('#{} > tr > th > a.s.xst'.format(search_id.get('id')))
            for p_link, p_updateTime, p_title, p_click in zip(_links, updateTime, title, clicks):
                domainNew = 'http://thz2.com' + '/' + str(p_link.get('href'))
                d_list = page_next(domainNew)
                if d_list:
                    data_ = {
                        'num': p_title.get_text().split(']')[0].replace('[', ''),
                        'title' : p_title.get_text().split(']')[1],
                        'url': domainNew,
                        'file': d_list['download'],
                        'picture': d_list['pictures'],
                        'time': p_updateTime.get('title').replace('-',''),
                        'comemnts': p_click.get_text()
                    }
                    updatedata(data_)
    browser.close()

if __name__ == '__main__':
    urls = get_links_update()
    for i_url in urls:
        spider_update(i_url)
