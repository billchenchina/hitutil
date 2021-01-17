"""Utils of hit.ids"""

import base64
import random

from Crypto.Cipher import AES

BLOCK_SIZE = 16


def rds(length: int) -> str:
    """Implementation of _rds function in encrypt.js"""
    chars = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678'
    return ''.join([random.choice(chars) for i in range(length)])


def pad(data: bytes) -> bytes:
    """Pad bytes"""
    length = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    return data + (chr(length)*length).encode()


def encrypt(message: bytes, passphrase: bytes) -> bytes:
    """Implementation of encryptAES function in encrypt.js"""
    aes = AES.new(passphrase, AES.MODE_CBC, rds(16).encode())
    return base64.b64encode(aes.encrypt(pad(message)))
