import re
import requests


def zdaye():
    # https://www.zdaye.com/dayProxy/2022/6/1.html
    url = "https://www.zdaye.com/dayProxy.html"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        data = r.text
        url_res = re.findall(r"/dayProxy/ip/[0-9]{5,11}.html", data)
        get_proxy_ip(url_res[0])

    else:
        print('error')


def get_proxy_ip(url):
    ip_port_set = set()
    url = "https://www.zdaye.com%s" % url
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    data = response.text
    data_line_list = data.split('\n')

    for data_line in data_line_list:
        if "立即检测该代理IP_" in data_line:
            key_seg = data_line.split("立即检测该代理IP_")[1]
            ip_port = key_seg.split("是否可用")[0]
            check_ip_port_result = check_proxy(ip_port)
            print(ip_port)
            if check_ip_port_result:
                ip_port_set.add(ip_port)

    print(ip_port_set)


def check_proxy(ip_port):
    result = False
    proxy = {"http": "http://" + ip_port}
    url = "http://pd.musicapp.migu.cn/MIGUM3.0/v1.0/content/search_all.do?text=zhoujielun&pageNo=1&pageSize=20&searchSwitch={'song':1}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.55 Safari/537.36',
    }
    exe_time = 0
    retyr_time = 1
    while result == False:
        try:
            response = requests.get(url, headers=headers, proxies=proxy, timeout=5)
            response.encoding = 'utf-8'
            # print(response.text)
            if "000000" in response.text:
                result = True
                print(response.text)
                break
        except Exception as e:
            print("check_ip_port error")

        exe_time += 1
        if exe_time > retyr_time:
            break

    return result


if __name__ == "__main__":
    zdaye()
    # check_proxy('106.14.255.124:80');
