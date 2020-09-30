from common.errors import PermissionErr
from user.models import User


def perm_required(perm_name):
    '''检查当前用户购买的 VIP 是否具有某权限'''
    def deco(view_func):
        def wrapper(request, *args, **kwargs):
            # 获取当前用户
            user = User.objects.get(id=request.uid)

            # 进行权限检查
            if user.vip.has_perm(perm_name):
                return view_func(request, *args, **kwargs)
            else:
                raise PermissionErr
        return wrapper
    return deco