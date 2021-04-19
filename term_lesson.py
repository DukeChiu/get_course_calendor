import requests as req
import json
import logging
import os
import re
from tools import config

logger = config.logger


# load tht information of user

def get_sep_cookies():
    try:
        resp_init_cookies = req.get(config.info['urls']['initUrl'])
        init_cookies = resp_init_cookies.cookies
        resp_final_cookies = req.post(url=config.info['urls']['loginUrl'], data=config.info['userInfos'],
                                      cookies=init_cookies, headers=config.info['headers'], allow_redirects=False)
        cookies = dict(init_cookies)
        cookies.update({'sepuser': re.findall('sepuser="(.+?)"', resp_final_cookies.headers['Set-Cookie'])[0]})
        return cookies
        #
    except Exception as e:
        logger.error(str(e))
        return None


def get_jwxt_cookie(tmp_cookies):
    try:
        resp_url = req.get(config.info['urls']['sepToJwxt'], cookies=tmp_cookies)
        # print(resp_url.text)
        url_to_jwxt = re.findall('url=(.+?)"', resp_url.text)[0]
        # print(url_to_jwxt)
        resp_jwxt_cookies = req.get(url_to_jwxt, headers=config.info['headers'], allow_redirects=False)
        jwxt_cookies = re.findall('JSESSIONID=(.+?);', str(resp_jwxt_cookies.headers.get('Set-Cookie')))[0]
        tmp_cookies['JSESSIONID'] = jwxt_cookies
        return tmp_cookies
    except Exception as e:
        logger.error(str(e))
        return None


def get_lessons(cookies):
    try:
        req.get(config.info['urls']['siteMain'], headers=config.info['headers'], cookies=cookies)
        resp_lesson = req.get(config.info['urls']['lesson'], cookies=cookies, headers=config.info['headers'])
        lessons_href = list(
            map(lambda x: config.info['urls']['jwxtRoot'] + x, re.findall('/course/coursetime.+?"', resp_lesson.text)),
            )
        print(lessons_href)
    except Exception as e:
        logger.error(str(e))


if __name__ == '__main__':
    cookies = get_jwxt_cookie(get_sep_cookies())
    print(cookies)
    get_lessons(cookies)
