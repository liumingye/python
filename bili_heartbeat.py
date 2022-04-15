import time
import requests
import os

"""
注意在 cookie 的 180 天过期时间之前更新 cookie
export cookie="*********" && export biz=164598376 && python bili_heartbeat.py
"""

cookie = os.environ.get('cookie')
biz = os.environ.get('biz')


class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0, item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

    def peek(self):
        return self.items[-1]

    def front(self):
        return self.items[0]


class PlayBiliVideo(object):

    def __init__(self, cookie, biz):
        self.cookie = self.parse_cookie(cookie)
        self.biz = biz
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15',
            'origin': 'https://www.bilibili.com',
            'referer': 'https://www.bilibili.com',
            'cookie': cookie
        }

    # 解析cookie
    def parse_cookie(self, cookie):
        cookie_list = cookie.split(';')
        cookie_dict = {}
        for i in cookie_list:
            k, v = i.split('=')
            cookie_dict[k.strip()] = v.strip()
        return cookie_dict

    def prt_err_msg(self, res, expectation):
        if res['code'] != expectation:
            print('ERROR:', res['message'])
        else:
            print('SUCCESS')

    def get_video_list(self, biz_id):
        print('获取视频列表')
        # 获取b站视频列表
        url = 'https://api.bilibili.com/x/v2/medialist/resource/list'
        data = {
            'type': '1',
            'oid': '',
            'otype': '2',
            'biz_id': biz_id,
            'bvid': '',
            'with_current': 'true',
            'mobi_app': 'web',
            'ps': '100',
            'direction': 'false',
            'sort_field': '1',
            'tid': '0',
            'desc': 'false'
        }
        res = requests.get(url, params=data, headers=self.headers).json()

        media_list = res['data']['media_list']

        videoList = []

        # 循环media_list
        for media in media_list:
            videoList.append({
                'aid': media['id'],
                'cid': media['pages'][0]['id'],
                'bvid': media['bv_id'],
                'duration':  media['duration'],
                'playlist_id': biz_id,
            })
            print(media['index'] + 1, media['title'])

        return videoList

    def h5(self, param):
        """登录"""

        # 取当前时间戳
        ts = int(time.time())

        data = {
            'mid': self.cookie['DedeUserID'],
            'part': 1,
            'lv': 6,
            'ftime': ts,
            'stime': ts + 1,
            'type': 3,
            'sub_type': 0,
            'refer_url': 'https://www.bilibili.com/',
            'spmid': '333.788.0.0',
            'from_spmid': '',
            'csrf': self.cookie['bili_jct'],
        }

        # 数组合并
        data.update(param['video'])

        h5 = 'https://api.bilibili.com/x/click-interface/click/web/h5'

        res = requests.post(h5, data=data, headers=self.headers).json()
        self.prt_err_msg(res, 0)

    def heartbeat(self, param):
        """观看视频"""

        data = {
            'mid': self.cookie['DedeUserID'],
            'played_time': param['time'],
            'real_played_time': param['time'],
            'realtime': param['time'],
            'type': 3,
            'dt': 2,
            'play_type': 0,
            'from_spmid': '333.824.playlist_within_video.0',
            'spmid': '333.788.0.0',
            'auto_continued_play': 1,
            'refer_url': 'https://space.bilibili.com/164598376',
            'bsource': '',
            'playlist_type': 1,
            'csrf': self.cookie['bili_jct'],
        }

        # 数组合并
        data.update(param['video'])

        # 观看视频的参数限制貌似较小
        heartbeat = 'https://api.bilibili.com/x/click-interface/web/heartbeat'

        res = requests.post(heartbeat, data=data, headers=self.headers).json()
        self.prt_err_msg(res, 0)

    def start(self, videoList):
        q = Queue()

        start_ts = int(time.time())

        print('添加队列')
        # 添加队列
        for video in videoList:
            # 登录队列
            q.enqueue({
                'param': {
                    'video': video.copy()
                },
                'task': 'h5',
                'sleep': 3,
            })

            video['start_ts'] = start_ts
            # 播放进度队列
            step = 15
            start = video['duration'] // step
            for i in range(start + 1):
                _sleep = step
                _time = i * step

                # 倒数第一个
                if _time + step >= video['duration']:
                    _sleep = video['duration'] - _time

                q.enqueue({
                    'param': {
                        'video': video,
                        'time': _time,
                    },
                    'task': 'heartbeat',
                    'sleep': _sleep,
                })

            # 播放完成
            if q.isEmpty() is False and q.front()['task'] == 'heartbeat' and q.front()['param']['time'] < video['duration']:
                q.enqueue({
                    'param': {
                        'video': video,
                        'time': video['duration'],
                    },
                    'task': 'heartbeat',
                    'sleep': 3,
                })

            start_ts += video['duration'] + 3 + 3

        print('开始队列')
        # 循环q.items
        while q.size() > 0:
            # 取出一个
            item = q.dequeue()

            print(item['task'] + ':', item['param'])

            # 执行
            self.__getattribute__(item['task'])(item['param'])

            # 等待
            time.sleep(item['sleep'])

        # 循环
        self.start(videoList)

    def run(self):
        videoList = self.get_video_list(self.biz)
        self.start(videoList)


if __name__ == '__main__':
    PlayBiliVideo(cookie, biz).run()
