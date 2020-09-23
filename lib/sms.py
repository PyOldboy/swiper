import json
import time
from hashlib import md5

import requests

from tantan import config as cfg

def send_sms(phonenum, vcode):
    args = {
        'appid': cfg.SD_APPID,  # APPID
        'to': phonenum,  # 手机号
        'project': cfg.SD_PROJECT,  # 短信模板的 ID
        'vars': json.dumps({'code': vcode, 'time': '5分钟'}),
        'timestamp': int(time.time()),
        'sign_type': cfg.SD_SIGN_TYPE,
    }
    # 计算参数的签名
    sorted_args = sorted(args.items())  # 提取每一项
    args_str = '&'.join([f'{key}={value}' for key, value in sorted_args])  # 对参数排序、组合
    sign_str = f'{cfg.SD_APPID}{cfg.SD_APPKEY}{args_str}{cfg.SD_APPID}{cfg.SD_APPKEY}'
    sign_bytes = sign_str.encode('utf8')  # 拼接成待签名字符串
    signature = md5(sign_bytes).hexdigest()  # 计算签名
    args['signature'] = signature

    response = requests.post(cfg.SD_API, data=args)
    if response.status_code == 200:
        result = response.json()
        print('短信结果：', result)
        if result.get('status') == 'success':
            return True
    return False