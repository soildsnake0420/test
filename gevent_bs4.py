from gevent import monkey
monkey.patch_all()
from bs4 import BeautifulSoup
import gevent, requests
from gevent.queue import Queue

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

class gevent_movies():

    def __init__(self, url_list):

        # 任务列表
        self.tasks_list = []

        # 把网址列表遍历
        for url in url_list:
            # 创建一个任务，执行 上面的方法
            task = gevent.spawn(self.crawler(url))

            # 把创建好的任务放进任务列表
            self.tasks_list.append(task)

        # 开始执行任务
        gevent.joinall(self.tasks_list)


    #执行方法
    def crawler(self, urls):

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

        work = Queue()
        for url in url_list:
            work.put_nowait(url)

        #当队列不为空则执行
        while not work.empty():

            #取出网址
            url = work.get_nowait()

            #开始抓取数据
            r = requests.get(urls, headers = headers)

            bs = BeautifulSoup(r.text, 'html.parser')

            #电影内容
            bingcenters = bs.find_all(class_='mov_con')


            for bingcenter in bingcenters:


                try:
                    #电影标题
                    title = bingcenter.find('h2')
                    #电影导演
                    dirctor = bingcenter.find_all('p')[0]
                    #电影主演
                    actor = bingcenter.find_all('p')[1]
                    #电影简介
                    content = bingcenter.find(class_='mt3')

                    #打印出这些信息
                    print(title.text)
                    print(dirctor.text)
                    print(actor.text)
                    print(content.text)
                except:
                    #如果缺失信息，则打印下面
                    print('暂无信息') 

                print('---------------')

news = gevent_movies(url_list)
