#!/user/bin/env python3
# _*_ coding:utf-8 _*_

import urllib.request
import urllib.parse
import re
import http.cookiejar
import socket


def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


url = "http://211.138.1.156:8888/showLogin.do?wlanuserip="+get_host_ip()+"&wlanacname=0004.0313.311.00"
url_post = "http://211.138.1.156:8888/login.do"

#用户名及密码
username = 
password = 


header_login = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0",
        "Host": "211.138.1.156:8888",
        "Referer": "http://211.138.1.156:8888/showLogin.do?wlanuserip=100.122.193.111&wlanacname=0004.0313.311.00",
        "Content-Type": "application/x-www-form-urlencoded",
        "Upgrade-Insecure-Requests": "1"
}

# 提交的表单
data_login= {
    "bpssBUSPWD": password,
    "bpssUSERNAME": username,
    "bpssVERIFY": "",
    "cookieAge": 7,
    # "CSRFToken_HW": "af3bcf7d2708881946b4ff3bc4d6ff63",
    "dynVerifyCode": "",
    "loginType": 1,
    "showVerify": "false"
}

# cookie管理
cookie = http.cookiejar.LWPCookieJar(filename='cookie.txt')
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))


# 查询 CSRFToken_HW
pattern = 'CSRFToken_HW" value=(.*)'
request = urllib.request.Request(url, headers=header_login)
with opener.open(request) as res:
    html = res.read()
html = html.decode('UTF-8', 'ignore')
data_login["CSRFToken_HW"] = re.match(pattern,html)


# 登陆
data_l = urllib.parse.urlencode(data_login).encode('utf-8')
request_login = urllib.request.Request(url_post, data=data_l, headers=header_login)
print("IP地址为："+get_host_ip())
with opener.open(request_login) as res:
    html = res.read()
html = html.decode('UTF-8', 'ignore')
pattern = '取消自动登录</span>'
a = re.search(pattern, html)
if a:
    print("登陆成功")
else:
    print("登陆失败")
