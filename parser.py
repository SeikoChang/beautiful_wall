# -*- coding: UTF-8 -*-

import requests #各種引入
import re, os, sys
import urllib
from hashlib import md5
from multiprocessing import Pool


PY3K = sys.version_info >= (3, 0)
if PY3K:
    import urllib.request as urllib2
    import urllib.parse as urlparse
else:
    import urllib2 
    import urlparse


def get_html(url):
    r = requests.get(url)
    if r.status_code == 200:
        return r.text

    return None


def save_image(img_url):
    ir = requests.get(img_url)
    if ir.status_code == 200:
        content = ir.content
        file_path = '{path}/{name}.{ext}'.format(path=os.getcwd(), name=md5(content).hexdigest(), ext='jpg')
        print(file_path)
        if not os.path.exists(file_path):
            with open(file_path, 'wb') as f:
                f.write(content)
        else:
            print('file exists!!!')

        print('download completed! [%s] to [%s]' % (img_url, file_path))

'''
if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    print('INFO : It spend [%s] to download img' % end-start)
'''

def download_image(imgs=[], out=os.getcwd(), replace=False ,retry=2):
    for i in imgs:
        for j in range(1, 1+retry):
            path, name = os.path.split(i)
            tofile = '{path}{sep}{name}'.format(path=out, sep=os.sep, name=name)
            print(tofile)
            if not os.path.exists(tofile) or (os.path.exists(tofile) and replace):
                print('downloading .... = [%s]' % tofile)
                try:
                    urllib2.urlretrieve(i, tofile)
                    break
                except:
                    print('fail to download from = [%s]' % i)
            else:
                print('file exists!!!')
                break

def findSubUrlWin4000(url, pattern, retry=2):
    urls = []
    root_url = url
    headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    }

    for i in range(1, 1+retry):
        req = html =None
        try:
            req = requests.get(url=root_url, headers=headers)
            html = req.text
            pattern = re.compile(pattern)
            urls = re.findall(pattern, html)
        except:
            if html:
                print ('\r\n')
                print (html)

    #print ('\r\n')
    #print (url)
    #print ('\r\n')
    #print (urls)
    #print ('\r\n')

    return urls


def getImg(url, out=os.getcwd(), replace=False):
    imglist = []

    root_url = url
    urls = findSubUrlWin4000(url=root_url, pattern=r'<a href="(http://www.win4000.com/meinv.+?.html)">')

    for url in urls:
        print('url = [%s]' % url)
        sub_urls = findSubUrlWin4000(url=url, pattern=r'<a href="(http://www.win4000.com/meinv.+?.html)"><img src=')
        #print('sub_urls = [%s]' % sub_urls)
        for sub_url in sub_urls:
            print('sub_url = [%s]' % sub_url)
            imgurl = findSubUrlWin4000(url=sub_url, pattern=r'<img class="pic-large" src=.* data-original=".+?" url="(.+?)"')
            download_image(imgs=imgurl, out=out, replace=replace)

            for j in imgurl:
                imglist.append(j)

        imgurl = findSubUrlWin4000(url=url, pattern=r'<img class="pic-large" src=.* data-original=".+?" url="(.+?)"')
        download_image(imgs=imgurl, out=out, replace=False)
        for j in imgurl:
            imglist.append(j)

    print(imglist)
    print('total image # = [%s] downloaded' % len(imglist))


if __name__ == '__main__':
    getImg(url=sys.argv[1], out=sys.argv[2])

