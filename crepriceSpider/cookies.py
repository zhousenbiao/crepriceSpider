# -*- coding:utf-8 -*-
import requests
import json
import redis
import logging
from .settings import REDIS_URL

logger = logging.getLogger(__name__)

# 使用REDIS_URL链接Redis数据库,deconde_response=True这个参数必须要,数据会变成byte形式,完全没法用
reds = redis.Redis.from_url(REDIS_URL, db=2, decode_responses=True)
login_url = 'http://www.creprice.cn/user/login.html?matchrand=a0b92382'

##获取Cookie
def get_cookie(account, password):
    s = requests.Session()
    payload = {
        'login_uid1': account,
        'login_pwd1': password,
        'agreeRule': "1",
        'loginsubmit': "登录",
        # 'redirect_to': "http://www.creprice.cn",
        # 'testcookie': "1"
    }
    response = s.post(login_url, data=payload, allow_redirects=False)
    cookies = response.cookies.get_dict()
    logger.warning("get cookie success!!!(account is:%s)" % account)
    return json.dumps(cookies)

# 将Cookies写入Redis数据库
def init_cookie(red, spidername):
    redkeys = reds.keys()
    for user in redkeys:
        password = reds.get(user)
        if red.get("%s:Cookies:%s--%s" % (spidername, user, password)) is None:
            cookie = get_cookie(user, password)
            red.set("%s:Cookies:%s--%s"% (spidername, user, password), cookie)

# if __name__ == '__main__':
#     get_cookie("13790395689","qwe123")