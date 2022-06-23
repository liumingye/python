import requests
import json

# 每日签到
url = "https://user.lfcharge.com/cfs/service.json"

payload = json.dumps({"serviceId": "pointsTask", "data": "{\"userId\":504456,\"typeCode\":\"1001\"}", "signature": "", "token": ""})
headers = {'Content-Type': 'application/json'}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)

# 看视频领积分
url = "https://user.lfcharge.com/cfs/service.json"

payload = json.dumps({"serviceId": "pointsTask", "data": "{\"userId\":504456,\"typeCode\":\"1004\"}", "signature": "", "token": ""})
headers = {'Content-Type': 'application/json'}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)

# 福利送不停
def draw(turntableDetailId):

    url = "https://user.lfcharge.com/cfs/service.json"

    payload = json.dumps({"serviceId": "draw", "data": "{\"userId\":504456,\"turntableDetailId\":\"" + str(turntableDetailId) + "\",\"source\":\"01\"}", "signature": "", "token": ""})
    headers = {'Content-Type': 'application/json'}

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

draw(0)
draw(1)
draw(2)
draw(3)
draw(4)
draw(5)
