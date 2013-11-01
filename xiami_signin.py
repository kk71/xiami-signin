#!/usr/bin/env python3
#coding=utf-8

script_info='''====================================
多账户虾米自动签到器
请在http://python.org/getit/ 下载python3.

作者：kK(fkfkbill@gmail.com)
http://kkblog.org

reversion:
2013.10：xiami.com改版
====================================
'''

from urllib import request
from http.cookiejar import CookieJar
from urllib.parse import urlencode
import re
import gzip
import pdb


#在此填写账户名（可多账户）
user_info=[
	{"email":"","password":""},
]


#xiami uris
site_urls={
	"index":"http://www.xiami.com",
	"login":"https://login.xiami.com/member/login",
    "check-if-logged-in":"http://www.xiami.com/index/indexright",
	"signin":"http://www.xiami.com/task/signin",
}

#login form
login_form={
    "_xiamitoken":"",#fetch the token in js code from the index page
    "done":"http%3A%2F%2Fwww.xiami.com%2F",
    "type":"",
    "submit":"登 录",
}

#flags
site_flags={
    "logged-in":"今日任务",#note:这个标志在""
	"login-failed":"密码错误",
    "not-logged-in":"忘记密码",
    "captcha-required":"验证码",
}

#fetch xiami token
fetch_re={
    "get-token":re.compile(r"_xiamitoken = '(.+?)';",re.S)
}

#headers for opener
headers=[
    ("Accept","text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"),
    ("Accept-Encoding","gzip,deflate,sdch"),
    ("Accept-Language","en-US,en;q=0.8"),
    ("Cache-Control","max-age=0"),
    ("Connection","keep-alive"),
    ("DNT","1"),
    ("Host","www.xiami.com"),
    ("Referer","http://www.xiami.com/home"),
    ("User-Agent","Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36"),
]


#=========================
def login(n):
    '''
login xiami.
arugments:
	n:登录的账户编号。
return:
	url opener:when succeeded
	None:when failed or have signed in
'''
    cookie_support=request.HTTPCookieProcessor(CookieJar())
    opener=request.build_opener(cookie_support,
                                request.HTTPHandler,
                                request.HTTPRedirectHandler,
                                request.HTTPSHandler)
    opener.addheaders=headers

    content=gzip.decompress(opener.open(site_urls["index"]).read()).decode("utf-8")
    token=fetch_re["get-token"].findall(content)[0]
    lf=login_form
    lf.update(user_info[n])
    lf.update({"_xiamitoken":token})
    print("%s：获得token：%s。"%(user_info[n]["email"],token))

    req=request.Request(url=site_urls["login"],data=urlencode(lf).encode("utf-8"))
    content=gzip.decompress(opener.open(req).read()).decode("utf-8")
    check_content=gzip.decompress(opener.open(site_urls["check-if-logged-in"]).read()).decode("utf-8")
	
    if site_flags["login-failed"] in content:
        print("%s：邮箱或密钥错误。"%user_info[n]["email"])
    elif site_flags["captcha-required"] in content:
        print("%s：虾米要求输入验证码，请断网后重新尝试。\r\n"%user_info[n]["email"])
    elif site_flags["not-logged-in"] in content:
        print("%s：登录失败（用户密码看上去正确），请联系作者报bug。"%user_info[n]["email"])
    elif site_flags["logged-in"] in check_content: 
        print("%s：登录成功。"%user_info[n]["email"])
        return opener
    else:
        print("出现未知标志，以下是调试过程，请联系作者～")
        pdb.set_trace()



#=========================
def signin(opener):
    '''
sign in xiami.com to get daily coins:P
arugments:
	opener:a urllib opener that is logged in xiami.com
'''
    if opener==None:return
    opener.addheaders+=[("X-Requested-With","XMLHttpRequest"),]
    days=gzip.decompress(opener.open(site_urls["signin"],data=b'').read()).decode("utf-8")
    try:
        days=int(days)
    except:
        print("失败：返回信息“%s”，请联系作者报bug。\r\n"%days)
        return
    print("成功：已签到%s天。\r\n"%days)



#=========================
if __name__=="__main__":
	print(script_info)
	for i in range(len(user_info)):
		signin(login(i))
	input("谢谢使用嘻嘻:P")
