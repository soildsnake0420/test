
#gevent 学习

from gevent import monkey
monkey.patch_all()
from bs4 import BeautifulSoup
import gevent
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
}

url_list = [
            'http://www.mtime.com/top/tv/top100/',
            'http://www.mtime.com/top/tv/top100/index-1.html',
            'http://www.mtime.com/top/tv/top100/index-2.html',
            'http://www.mtime.com/top/tv/top100/index-3.html',
            'http://www.mtime.com/top/tv/top100/index-4.html',
            'http://www.mtime.com/top/tv/top100/index-5.html',
            'http://www.mtime.com/top/tv/top100/index-6.html',
            'http://www.mtime.com/top/tv/top100/index-7.html',
            'http://www.mtime.com/top/tv/top100/index-8.html',
            'http://www.mtime.com/top/tv/top100/index-9.html',
            'http://www.mtime.com/top/tv/top100/index-10.html'
            ]

#执行方法
def crawler(url):

    r = requests.get(url, headers= headers)

    bs = BeautifulSoup(r.text, 'html.parser')

    #电影内容
    bingcenters = bs.find_all(class_='mov_con')


    for bingcenter in bingcenters:

        try:
            title = bingcenter.find('h2')
            dirctor = bingcenter.find_all('p')[0]
            actor = bingcenter.find_all('p')[1]
            content = bingcenter.find(class_='mt3')

            print(title.text)
            print(dirctor.text)
            print(actor.text)
            print(content.text)
        except:
            print('暂无信息')

        print('---------------')


#任务列表
tasks_list = []

#把网址列表遍历
for url in url_list:

    #创建一个任务，执行 上面的方法
    task = gevent.spawn(crawler(url))

    #把创建好的任务放进任务列表
    tasks_list.append(task)

#开始执行任务
gevent.joinall(tasks_list)



