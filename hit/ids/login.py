"""Implementation of hit.ids.login"""

import random
import re

from bs4 import BeautifulSoup
from hit.exceptions import CaptchaNeeded, LoginFailed
from requests import Session

from .utils import encrypt, rds


def idslogin(username: str, password: str, **kwargs) -> Session:
    """Handle ids.hit.edu.cn login
    Arguments:
        username (str): ID
        password (str): password
        **kwargs (dict): See below
    Keyword Arguments:
        s (requests.Session)
        captchaResponse (str)
        need_check_resp (boolen)
        check_resp_hook (function(requests.Response, *args, **kwargs))
    Returns:
        s (requests.Session): Session
    Raises:
        hit.exceptions.CaptchaNeeded: Captcha needed
        hit.exceptions.LoginFailed: Login Failed
    """
    if 's' in kwargs:
        s = kwargs['s']
    else:
        s = Session()
    # get pwdDefaultEncryptSalt
    r1 = s.get('http://ids.hit.edu.cn/authserver/login')
    pwd_default_encrypt_salt = re.compile(
        'pwdDefaultEncryptSalt = "(.*)"').search(r1.text).groups()[0]
    passwordEncrypt = encrypt(
        rds(64).encode()+password.encode(), pwd_default_encrypt_salt.encode())
    # Detect Captcha
    r2 = s.get('http://ids.hit.edu.cn/authserver/needCaptcha.html',
               params={
                   'username': username,
                   'pwdEncrypt2': 'pwdEncryptSalt'
               })
    if r2.text == 'true':
        if 'captchaResponse' in kwargs:
            captchaResponse = kwargs['captchaResponse']
        else:
            r = s.get('http://ids.hit.edu.cn/authserver/captcha.html', params={
                'ts': random.randint(0, 999)
            })
            raise CaptchaNeeded(s, r.content)
    else:
        captchaResponse = None
    soup = BeautifulSoup(r1.text, 'html.parser')
    r = s.post(r1.url, data={
        "username": username,
        "password": passwordEncrypt,
        "captchaResponse": captchaResponse,
        "lt": soup.find('input', {'name': 'lt'})['value'],
        "dllt": soup.find('input', {'name': 'dllt'})['value'],
        "execution": soup.find('input', {'name': 'execution'})['value'],
        "_eventId": soup.find('input', {'name': '_eventId'})['value'],
        "rmShown": soup.find('input', {'name': 'rmShown'})['value'],
        "pwdDefaultEncryptSalt": pwd_default_encrypt_salt
    })
    if r.url != 'http://ids.hit.edu.cn/authserver/index.do':
        raise LoginFailed()

    if kwargs.get('need_check_resp', False):
        s.hooks['response'].append(
            kwargs.get('check_resp_hook', _check_resp_hook_default_impl))
    
    return s

def _check_resp_hook_default_impl(r, *args, **kwargs):
    """
    Response hook for checking the error msg returned by ids
    another way: override Requests.Resopnse.ok()
    """
    soup = BeautifulSoup(r.text, 'html.parser')
    found_err_msg = soup.find('div', {'id': 'msg', 'class': 'errors'})
    assert not found_err_msg, \
        (f'found error msg: {found_err_msg.h2.text}, '
         f'reason: {found_err_msg.p.text}')
    return r
