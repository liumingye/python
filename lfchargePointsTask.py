import requests
import json

url = "https://user.lfcharge.com/cfs/service.json"

payload = json.dumps({
  "serviceId": "pointsTask",
  "data": "{\"userId\":504456,\"typeCode\":\"1001\"}",
  "signature": "",
  "token": ""
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)


url = "https://user.lfcharge.com/cfs/service.json"

payload = json.dumps({
  "serviceId": "pointsTask",
  "data": "{\"userId\":504456,\"typeCode\":\"1004\"}",
  "signature": "",
  "token": ""
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
