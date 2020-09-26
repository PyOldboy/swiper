'''程序逻辑配置，及第三方平台配置'''

# Redis 配置
REDIS = {
    'host': 'localhost',
    'port': 6379,
    'db': 2,
}


# 云之讯通信设置

YUN_SID = '4e43ef436406a81cc297291b9633029a'
YUN_TOKEN = '6c7fcf77b31128cebf3187ef0b39583d'
YUN_APPID = 'e35c50827a4e45429672b15188076d0a'
YUN_TEMPALTEID = '567790'
YUN_API = 'https://open.ucpaas.com/ol/sms/sendsms'



# 赛迪云通信设置
SD_APPID = '54756'
SD_APPKEY = 'd3ec971d542ca45c229e48d4811b1300'
SD_PROJECT = 'pBS5H'  # 短信模板的 ID
SD_SIGN_TYPE = 'md5'
SD_API = 'https://api.mysubmail.com/message/xsend.json'


# 七牛云配置
QN_DOMAIN = 'qh5o2kg5r.hd-bkt.clouddn.com'
QN_BUCKET = 'chengning'
QN_Access_Key = 'dQw134pAWeHx6fam-cIQ-1whO7H1gTYkKq2X9rng'
QN_Secret_Key = 'J77oP9QYxTun2q4ZLLkdi9HiM4xfDPbZuf80Fux_'
QN_CALLBACK_URL = 'http://106.53.229.53:80/qiniu/callback'
QN_CALLBACK_DOMAIN = '106.53.229.53:80'