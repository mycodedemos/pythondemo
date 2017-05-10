#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''加密工具'''
__author__ = "wenxiaoning(wenxiaoning@gochinatv.com)"
__copyright__ = "Copyright of GoChinaTV (2017)."

import hashlib
import time

from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex


class AESecurity():
    @classmethod
    def generate_key(cls):
        return Md5.encrypt('{}'.format(time.time()))[0:16]

    def __init__(self, key):
        self.key = key
        self.mode = AES.MODE_CBC

    # 加密函数，如果text不是16的倍数【加密文本text必须为16的倍数！】，那就补足为16的倍数
    def encrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.key)
        # 这里密钥key 长度必须为16（AES-128）、24（AES-192）、或32（AES-256）Bytes 长度.目前AES-128足够用
        length = 16
        count = len(text)
        add = length - (count % length)
        text = text + ('\0' * add)
        self.ciphertext = cryptor.encrypt(text)
        # 因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        # 所以这里统一把加密后的字符串转化为16进制字符串
        return b2a_hex(self.ciphertext).decode("utf-8")

    # 解密后，去掉补足的空格用strip() 去掉
    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.key)
        plain_text = cryptor.decrypt(a2b_hex(text)).decode("utf-8")
        return plain_text.rstrip('\x00')


class Md5():
    @classmethod
    def encrypt(cls, text):
        """
        计算字符的md5摘要
        :param str:
        :return:
        """
        return hashlib.md5(text.encode("utf-8")).hexdigest()


if __name__ == '__main__':
    key = AESecurity.generate_key()
    print(key)

    aes = AESecurity(key)
    id = Md5.encrypt('1')

    res = aes.encrypt('{};{}'.format(id, time.time()))
    print(res)