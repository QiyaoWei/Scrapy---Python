# -*- coding: utf-8 -*-

"""
Created on Thu Jun 7 17:42:05 2018

@author: Qiyao Wei
"""
import sys
import time
import hashlib
import random

#Returns both the proxy and the header authorization
def change():
    """
    :param: N/A
    :return: (proxy, header) in the form of a tuple
    """
    try:
        #Xundaili verbatim
        _version = sys.version_info
        is_python3 = (_version[0] == 3)

        #What you need is your orderno and secret, use mine for a try!
        #orderno = "ZF201861908708TBWqz"
        #secret  = "6f588ce975f644cbb941cc09ce4364be"
        #Or, you know, buy your own...

        ip = "forward.xdaili.cn"
        port = "80"

        ip_port = ip + ":" + port

        timestamp = str(int(time.time()))                # 计算时间戳
        string = ""
        string = "orderno=" + orderno + "," + "secret=" + secret + "," + "timestamp=" + timestamp

        if is_python3:
            string = string.encode()

        md5_string = hashlib.md5(string).hexdigest()                 # 计算sign
        sign = md5_string.upper()                              # 转换成大写
        auth = "sign=" + sign + "&" + "orderno=" + orderno + "&" + "timestamp=" + timestamp

        proxy = {"http": "http://" + ip_port, "https": "https://" + ip_port}
        header = {"Proxy-Authorization": auth,
                  'accept': '*/*',
                  'accept-encoding': 'gzip, deflate, br',
                  'accept-language': 'en-US,en;q=0.9',
                  'origin': 'https://www.merriam-webster.com',
                  'user-agent': "Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25", #Use your own!
                  'x-client-data': 'CJC2yQEIprbJAQjEtskBCKmdygEIqKPKAQ=='}

    except:
        #Take a break
        time.sleep(random.random())
        proxy  = change()[0]
        header = change()[1]

    return (proxy, header)