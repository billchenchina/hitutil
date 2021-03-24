"""Utils of hit.ids"""

import base64
import random

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
BLOCK_SIZE = 16


def rds(length: int) -> str:
    """Implementation of _rds function in encrypt.js"""
    chars = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678'
    return ''.join([random.choice(chars) for i in range(length)])


def encrypt(message: bytes, passphrase: bytes) -> bytes:
    """Implementation of encryptAES function in encrypt.js"""
    aes = AES.new(passphrase, AES.MODE_CBC, rds(16).encode())
    return base64.b64encode(aes.encrypt(pad(message, BLOCK_SIZE)))
