'''程序中的错误码'''

OK = 0  # 正常
# VCODE_FAILD = 1000  # 验证码发送失败
# VCODE_ERR = 1001  # 验证码错误
# LOGIN_REQUIRED = 1002  # 需要用户登陆
# PROFILE_ERR = 1003  # 用户资料表单数据错误


class LogicErr(Exception):
    code = OK

    def __init__(self, data=None):
        self.data = data or self.__class__.__name__


def gen_logic_err(name, code):
    '''生成一个逻辑异常类'''
    attr = {'code': code}
    return type(name, (LogicErr,), attr)


VcodeFaild = gen_logic_err('VcodeFaild', 1000)          # 验证码发送失败
VcodeErr = gen_logic_err('VcodeErr', 1001)              # 验证码错误
LoginRequired = gen_logic_err('LoginRequired', 1002)    # 需要用户登陆
ProfileErr = gen_logic_err('ProfileErr', 1003)          # 用户资料表单数据错误
SidErr = gen_logic_err('SidErr', 1004)                  # SID 错误
SwipeErr = gen_logic_err('SwipeErr', 1005)              # 滑动类型错误
RepeatSwipeErr = gen_logic_err('RepeatSwipeErr', 1006)  # 重复滑动
RewindLimit = gen_logic_err('RewindLimit', 1007)        # 反悔次数达到限制
RewindTimeout = gen_logic_err('RewindTimeout', 1008)    # 反悔超时
NoSwiped = gen_logic_err('NoSwiped', 1009)              # 当前还没有滑动记录
PermissionErr = gen_logic_err('PermissionErr', 1010)    # 用户不具有某权限

 