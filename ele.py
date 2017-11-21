#!/usr/bin/env python3
# -*-coding:utf-8-*-

import json
import re
import time
import random

url_jmm = 'http://m.quanmama.com/mzdm/2111914.html'
url_ele = 'https://restapi.ele.me/marketing/hongbao/h5/grab'
user_agent = 'User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 10_2_1 like Mac OS X) AppleWebKit/602.4.6 (KHTML, like Gecko) Mobile/14D27 QQ/6.7.1.416 V1_IPH_SQ_6.7.1_1_APP_A Pixel/750 Core/UIWebView NetType/4G QBWebViewType/1'

is_urllib = True  # 使用 自带的urllib 还是 requests 库

headers = {'User-Agent': user_agent,
           'Accept': '*/*',
           'Accept-Encoding': 'gzip, deflate, br',
           'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
           'Cache-Control': 'no-cache',
           'Connection': 'keep-alive',
           'Content-Type': 'application/json;charset=UTF-8',
           "Host": "restapi.ele.me",
           "Origin": "https://h5.ele.me",
           "Pragma": "no-cache",
           "Referer": "https://h5.ele.me/baida/"
           }

def revertShortLink(url_jmm):
    res = requests.head(url_jmm)
    return res.headers.get('location')


def get(url, **kwargs):
    if is_urllib:
        from urllib import request

        req = request.Request(url, **kwargs)
        html = request.urlopen(req).read().decode('utf-8')
        return html
    else:
        import requests

        html = requests.get(url, **kwargs).text
        return html


def post(url, **kwargs):
    if is_urllib:
        from urllib import request
        import gzip

        kwargs['data'] = json.dumps(kwargs['data']).encode('utf-8')
        req = request.Request(url, **kwargs)
        content = request.urlopen(req).read()
        try:
            html = gzip.decompress(content).decode("utf-8")
        except:
            html = content.decode("utf-8")
        return html
        pass
    else:
        import requests

        kwargs['data'] = json.dumps(kwargs.pop('data'))
        # kwargs['verify'] = False 不验证证书
        result_text = requests.post(url, **kwargs).text
        print(result_text)
        return result_text


def hongbao():
    jmm_html = get(url_jmm, headers={'User-Agent': user_agent})

    group_sn_list = re.findall(r'group_sn=(\w+)', jmm_html)

    phone = input('请输入领取红包的手机号码:').strip()

    for sn in group_sn_list:
        value = {
            "group_sn": sn,
            "phone": phone,
            "weixin_uid": '468015ki5tulqs9mbjmjvr6w83o45kh9'
        }
        result_text = post(url_ele, data=value, headers=headers)
        hongbao_dict = json.loads(result_text)
        account = hongbao_dict.get('account')
        hongbao_list_json = hongbao_dict.get('hongbao_list')
        if hongbao_list_json:
            for hongbao in hongbao_list_json:
                amount = hongbao.get('amount')
                hongbao_variety = hongbao.get('hongbao_variety')  # 数组
                name = hongbao.get('name')
                sum_condition = hongbao.get('sum_condition')
                validity_periods = hongbao.get('validity_periods')

                print('%s 领取了 满 %-4s减 %-3s的 %s %s %s' % (
                    account, sum_condition, amount, name, validity_periods, ' '.join(hongbao_variety)))
        time.sleep(random.randint(1, 3))

    print('红包领完了')


if __name__ == '__main__':
    hongbao()