import re,urllib,requests
s = requests.session()
url="http://m.quanmama.com/mzdm/2111914.html"
user_agent = 'User-Agent: Mozilla/5.0 (Linux; Android 7.1.1; MI 6 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/59.0.3071.125 Mobile Safari/537.36 MicroMessenger/6.5.13.1081 NetType/WIFI Language/zh_CN'
headers = {'User-Agent':user_agent}
s1=r"group_sn=\w{32}"
s2=re.findall(s1,s.get(url,headers=headers).text)
headers = {'User-Agent':user_agent,
           'Accept':'*/*',
           'Accept-Encoding':'gzip, deflate, br',
           'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
           'Cache-Control':'no-cache',
           'Connection':'keep-alive',
           'Content-Type':'text/plain;charset=UTF-8',
           "Host":"restapi.ele.me",
           "Origin":"https://h5.ele.me",
           "Pragma":"no-cache",
           "Referer":"https://h5.ele.me/baida/"
}
phone=input("请输入电话号码")
for url in s2:
    value={
        "group_sn":url[9:],
        "phone":phone,
        "weixin_uid":'468015ki5tulqs9mbjmjvr6w83o45kh9'
    }
    s3=s.post("https://restapi.ele.me/marketing/hongbao/h5/grab",json=value,headers=headers)
    s4=s3.text
    if not(re.findall("普通红包",s4)==[]):
        amount=re.search("amount\":(.*?),",s4)
        sum_condition=re.search("sum_condition\":(.*?),",s4)
        validity_periods=re.search("validity_periods\":\"(.*?)\"",s4)
        print("满{}减{},有效期{}".format(sum_condition.group(1),amount.group(1),validity_periods.group(1)))