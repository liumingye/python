import time
import requests
import json

requests.packages.urllib3.disable_warnings()


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


class CommitAnswer(object):
    def __init__(self):
        self.ModuleId = '594655d3-846b-4cf9-aaa3-02d902b3d618'
        self.UserCode = '1000'
        self.headers = {'Accept': 'application/json, text/plain, */*', 'Origin': 'https://wx.gzcentaline.com.cn', 'Accept-Encoding': 'gzip, deflate, br', 'Content-Type': 'application/json; charset=UTF-8', 'Connection': 'keep-alive', 'Host': 'wx.gzcentaline.com.cn', 'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko)  Mobile/15E148 wxwork/4.0.6 MicroMessenger/7.0.1 Language/zh ColorScheme/Dark miniprogram', 'Authorization': 'null', 'Accept-Language': 'zh-CN,zh-Hans;q=0.9', 'Referer': 'https://wx.gzcentaline.com.cn/WebApp/TrainingCentreVideoWeb/'}

    def GetCourseList(self):
        url = 'https://wx.gzcentaline.com.cn/WebApi/TrainingCentreApi/Course/GetCourseList?ModuleId=' + self.ModuleId + '&UserCode=' + self.UserCode + '&PageNum=1&PageSize=20&SearchText='
        res = requests.get(url, headers=self.headers, verify=False).json()

        Result = res['Result']

        CourseList = []

        for Course in Result:
            CourseList.append({'KeyId': Course['KeyId']})

        return CourseList

    def GetCourseDetail(self, CourseId):
        url = 'https://wx.gzcentaline.com.cn/WebApi/TrainingCentreApi/Course/CourseDetail?UserCode=' + self.UserCode + '&CourseId=' + CourseId
        res = requests.get(url, headers=self.headers, verify=False).json()

        Result = res['Result']['VideoList']

        CourseDetail = []

        for Course in Result:
            CourseDetail.append({'KeyId': Course['KeyId']})

        return CourseDetail

    def GetVideoDetail(self, VideoId):
        url = 'https://wx.gzcentaline.com.cn/WebApi/TrainingCentreApi/Video/detail?UserCode=' + self.UserCode + '&VideoId=' + VideoId
        res = requests.get(url, headers=self.headers, verify=False).json()

        requests.get('https://wx.gzcentaline.com.cn/WebApi/TrainingCentreApi/Video/markVideoLeastTime?UserCode=' + self.UserCode + '&VideoId=' + VideoId, headers=self.headers, verify=False).json()

        Result = res['Result']

        return Result

    def CommitAnswer(self, KeyId, Question):
        url = 'https://wx.gzcentaline.com.cn/WebApi/TrainingCentreApi/Video/commitAnswer'
        OptionValues = []
        for Option in Question['OptionList']:
            if Option['IsAnswer'] == True:
                OptionValues.append(Option['OptionValue'])
        data = {"empCode": self.UserCode, "optionValues": OptionValues, "questionId": Question['KeyId'], "videoId": KeyId}
        print(data)
        res = requests.post(url, headers=self.headers, data=json.dumps(data), verify=False).json()

        Result = res['Result']

        print(res)

        return Result

    def run(self):

        q = Queue()

        CourseList = self.GetCourseList()

        VideoList = []
        for Course in CourseList:
            print(Course['KeyId'])
            Video = self.GetCourseDetail(Course['KeyId'])
            VideoList.append(Video)
            time.sleep(0.05)

        for Video in VideoList:
            for v in Video:
                Detail = self.GetVideoDetail(v['KeyId'])
                q.enqueue(Detail)
                print(Detail)
                time.sleep(0.05)

        print(q.items)

        # 循环q.items
        while q.size() > 0:
            # 取出一个
            item = q.dequeue()

            print(item['QuestionList'])

            if (len(item['QuestionList']) > 0):
                for Question in item['QuestionList']:
                    self.CommitAnswer(item['KeyId'], Question)

            # # 等待
            time.sleep(0.1)


if __name__ == '__main__':
    CommitAnswer().run()
