import random
import re

from common import keys
from libs.cache import rds
from libs.sms import send_sms
from tasks import celery_app


def is_phonenum(phonenum):
    '''验证是否是一个正确的手机号'''
    if re.match(r'1[3-9]\d{9}$', phonenum):
        return True
    else:
        return False

def random_code(length=6):
    nums = [str(random.randint(0,9)) for i in range(length)]
    return ''.join(nums)

@celery_app.task
def send_vcode(phonenum):
    if not is_phonenum(phonenum):
        return False

    key = keys.VCODE_K % phonenum
    if rds.get(key):
        return True

    # 产生验证码
    vcode = random_code()
    print('随机码：', vcode)
    rds.set(key, vcode, 600)

    # return send_sms(phonenum, vcode)