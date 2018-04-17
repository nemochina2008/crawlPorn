<<<<<<< HEAD
from bs4 import BeautifulSoup
import requests
import re
import time
import os
from mainIndex import pornData, pornImg, torrent


def trueTorrentUrl():
    pattern = 'http://vipthz.com/.+'
    for trueUrl in torrent.find():
        print('一个神奇的种子正在发芽..哈哈')
        # print(trueUrl['torrent'])
        page = requests.get(trueUrl['torrent'])
        torrent_page = BeautifulSoup(page.text, 'lxml')
        # print(torrent_page)
        time.sleep(2)
        torrentUrls = torrent_page.find_all(href = re.compile(pattern))
        for t_url in torrentUrls:
            data = {
                'torrent_url' : t_url.get('href')
            }
            torrent.insert(data)
'''
<a href="http://vipthz.com/forum.php?mod=attachment&amp;aid=NDA2MTEwfGQ0MzVhZDM3fDE1MjIyOTM5Njd8MHwxNzk0MDk5" 
onclick="hideWindow('imc_attachad')">
<img src="source/plugin/imc_attachad/images/download.gif"> 
<font color="#008000">立即下载附件1</font> </a>
#wp > div > div:nth-child(3) > div:nth-child(2) > a
http://vipthz.com/imc_attachad-ad.html?aid=NDA2MTE4fDIxNTFiNjhifDE1MjIyOTQwMTh8MHwxNzk0MTA2
http://tu.thzimg.com/images/2018/03/26/9dad40d6940cdbfdec560314b3190f90.jpg
http://vipthz.com/forum.php?mod=attachment&aid=NDA2MzU1fGI3ZjEyNTdjfDE1MjIzMDI3Mzh8MHwxNzk1MDA0

'''

robot = "D:/pornfiles/"

def downloadImg(url):
    path = robot + url.split('/')[-1]
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    if not os.path.exists(robot):
        os.makedirs(robot)
    if not os.path.exists(path):
        with open(path, 'wb') as f:
            f.write(r.content)
            f.close()
            print(path + '\t\t\tSaved!')
    else:
        print('\t\t\tIt Had Exist! Foolish!!!!')



if __name__ == '__main__':
    # trueTorrentUrl()
    num = 0
    d_time = 0
    for d_img in pornImg.find():
        num += 1
        d_time +=2
        print('正在下载第{0}张图\t大吉大利,今晚吃鸡!\t耗费时间: {1}min\t总时间:{2}s'.format(num, int(d_time/60), d_time))
        time.sleep(2)
        # print(d_img['pornImgUrl'])
        downloadImg(d_img['pornImgUrl'])
        
=======
from spider import details
import requests
import os
import time


def downloadspider():
    list_num = [1, 2, 3, 4, 5]
    count = 0
    mount = 0
    # for item in details.find(no_cursor_timeout=True):
    #     robot = "E:/img/"
    #     for item_img, n in zip(item['picture'], list_num):
    #         path_img = robot + str(item['title']) + '-' + str(n) + '.jpg'
    #         html = requests.get(item_img)
    #         time.sleep(1)
    #         html.raise_for_status()
    #         html.encoding = html.apparent_encoding
    #         if not os.path.exists(robot):
    #             os.makedirs(robot)
    #         if not os.path.exists(path_img):
    #             count += 1
    #             print('正在下载{0}张图片:\t{1}'.format(count, item['title']))
    #             with open(path_img, 'wb') as i:
    #                 i.write(html.content)

    for item in details.find(no_cursor_timeout=True):
        robot = "E:/img/"
        for item_file in item['file']:
            path_file = robot + str(item['title']) + '.torrent'
            html = requests.get(item_file)
            time.sleep(1)
            html.raise_for_status()
            html.encoding = html.apparent_encoding
            if not os.path.exists(path_file):
                mount += 1
                print('正在下载{0}个种子:\t{1}'.format(mount, item['title']))
                with open(path_file, 'wb') as f:
                    f.write(html.content)


if __name__ == '__main__':
    downloadspider()
>>>>>>> porn website
