import time
import requests
import os

"""
注意在 cookie 的 180 天过期时间之前更新 cookie

export cookie="*********" && python bili_heartbeat.py
"""

cookie = os.environ.get('cookie')


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

    def __init__(self, cookie):
        self.cookie = self.parse_cookie(cookie)
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

    def get_video_list(self):
        videoList = [
            {
                'aid': 383108156,
                'cid': 571184507,
                'bvid': 'BV1iZ4y127pW',
                'start_ts': 1649768312,
                'duration': 87,
            },
            {
                'aid': 425498094,
                'cid': 569888447,
                'bvid': 'BV1v3411J7AW',
                'start_ts': 1649768525,
                'duration': 208,
            },
            {
                'aid': 637946697,
                'cid': 567234798,
                'bvid': 'BV1NY4y1i7fb',
                'start_ts': 1649768734,
                'duration': 85,
            },
            {
                'aid': 382851517,
                'cid': 564702726,
                'bvid': 'BV1ZZ4y1m7Lj',
                'start_ts': 1649768820,
                'duration': 252,
            }, {
                'aid': 682688049,
                'cid': 560110539,
                'bvid': 'BV1bS4y1N7yn',
                'start_ts': 1649769073,
                'duration': 158,
            }, {
                'aid': 383070378,
                'cid': 574094574,
                'bvid': 'BV1vZ4y127xW',
                'start_ts': 1649769379,
                'duration': 148,
            }]
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
            'playlist_id': 164598376,
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

    def run(self):
        q = Queue()

        # 添加队列
        videoList = self.get_video_list()
        for video in videoList:
            # 登录队列
            q.enqueue({
                'param': {
                    'video': video
                },
                'task': 'h5',
                'sleep': 3,
            })

            step = 15

            # 播放进度队列
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

        # print(q.items)

        # 循环q.items
        while q.size() > 0:
            # 取出一个
            item = q.dequeue()

            print(item['task'] + ':', item['param']['video']['bvid'])

            # 执行
            self.__getattribute__(item['task'])(item['param'])

            # 等待
            time.sleep(item['sleep'])

        # 循环
        self.run()


if __name__ == '__main__':
    PlayBiliVideo(cookie).run()
