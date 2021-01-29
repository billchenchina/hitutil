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
    return s
