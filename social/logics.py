import datetime

from common import keys
from libs.cache import rds
from user.models import User
from user.models import Profile
from social.models import Swiped, Friend


def rcmd_from_queue(uid):
    '''从优先推荐队列进行推荐'''
    uid_list = rds.lrange(keys.FIRST_RCMD_Q % uid, 0, 19)  # 从优先推荐队列取出 uid 列表
    uid_list = [int(uid) for uid in uid_list]  # 将 uid 强转成 int 类型
    return User.objects.filter(id__in=uid_list)


def rcmd_from_db(uid, num=20):
    '''从数据库中推荐滑动用户'''
    profile = Profile.objects.get(id=uid)

    #   计算出生日期范围
    today = datetime.date.today()
    earliest_birth = today - datetime.timedelta(profile.max_dating_age * 365)  # 最早出生日期
    latest_birth = today - datetime.timedelta(profile.min_dating_age * 365)  # 最晚出生日期

    # 获取已经滑过的用户的 ID
    sid_list = Swiped.objects.filter(uid=uid).values_list('sid', flat=True)

    users = User.objects.filter(
        location=profile.dating_location,
        gender=profile.dating_gender,
        birthday__range=[earliest_birth, latest_birth],
    ).exclude(id__in=sid_list)[:num]  # 懒加载

    # TODO：排除已经滑过的人

    return users


def rcmd(uid):
    '''推荐滑动用户'''
    first_users = rcmd_from_queue(uid)
    remain = 20 - len(first_users) # 计算需要从数据库获取的个数
    if remain:
        second_users = rcmd_from_db(uid,remain)
        return  set(first_users) | set(second_users)
    else:
        return first_users



def like_someone(uid, sid):
    '''喜欢某人 (右滑)'''

    # 添加滑动记录
    Swiped.objects.create(uid=uid, sid=sid, stype='like')

    # 强制删除优先推荐队列中的 sid
    rds.lrem(keys.FIRST_RCMD_Q % uid, count=0, value=sid)

    # 检查对方是否喜欢(右滑或上滑)过自己
    if Swiped.is_liked(sid, uid):
        # 将互相喜欢的两人添加成好友
        Friend.make_friends(uid, sid)
        return True
    else:
        return False


def superlike_someone(uid, sid):
    '''超级喜欢某人 (上滑)'''

    # 添加滑动记录
    Swiped.objects.create(uid=uid, sid=sid, stype='superlike')

    # 强制删除优先推荐队列中的 sid
    rds.lrem(keys.FIRST_RCMD_Q % uid, count=0, value=sid)

    # 检查对方是否喜欢(右滑或上滑)过自己
    liked = Swiped.is_liked(sid, uid)
    if liked is True:
        # 将互相喜欢的两人添加成好友
        Friend.make_friends(uid, sid)
        return True
    elif liked is False:
        return False
    else:
        # 对方尚未滑到过自己，把自己推荐给对方
        rds.rpush(keys.FIRST_RCMD_Q % sid, uid)
        return False
