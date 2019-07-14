# -*- coding: utf-8 -*-
import hashlib
import random


def md5hex(data):
    data = data.encode('utf-8')
    md5 = hashlib.md5()
    md5.update(data)
    return md5.hexdigest()


def get_random_str(length=4):
    chars = "abcdedfhkmnpqrtuvwxy2346789ABCDEFGHKLMNPQRTUVWXY2346789"
    return ''.join(random.sample(chars, length)).lower()
