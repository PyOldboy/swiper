'''缓存中出现的所有 Key'''


VCODE_K = 'Vcode-%s'  # 验证码缓存，拼接用户的手机号
FIRST_RCMD_Q = 'FirstRcmdQ-%s'  # 优先推荐队列, 拼接用户 uid
REWIND_TIMES_K = 'RewindTimes-%s-%s'  # 每日反悔次数，拼接日期和uid

PROFILE_K = 'Profile-%s'  # 用户交友资料的 Key，拼接 Profile.id
MODEL_K = 'Model-%s-%s'  # 模型缓存的 Key，拼接 Model 名 和 对象的主键