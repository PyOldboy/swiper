import random
import re

from django.core.cache import cache

from lib.sms import send_sms


def is_phonenum(phonenum):
    '''验证是否是一个正确的手机号'''
    if re.match(r'1[3-9]\d{9}$', phonenum):
        return True
    else:
        return False

def random_code(length=6):
    nums = [str(random.randint(0,9)) for i in range(length)]
    return ''.join(nums)

def send_vcode(phonenum):
    if not is_phonenum(phonenum):
        return False

    key = 'Vcode-%s' % phonenum
    if cache.get(key):
        return True

    # 产生验证码
    vcode = random_code()
    print('随机码：', vcode)
    cache.set(key, vcode, 600)

    # return send_sms(phonenum, vcode)