import datetime

from django.db.transaction import atomic

from common import keys, errors
from libs.cache import rds
from tantan import config
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

    return users


def rcmd(uid):
    '''推荐滑动用户'''
    first_users = rcmd_from_queue(uid)
    remain = 20 - len(first_users)  # 计算需要从数据库获取的个数
    if remain:
        second_users = rcmd_from_db(uid, remain)
        return set(first_users) | set(second_users)
    else:
        return first_users


@atomic
def like_someone(uid, sid):
    '''喜欢某人 (右滑)'''

    # 添加滑动记录
    Swiped.swipe(uid, sid, 'like')

    # 强制删除优先推荐队列中的 sid
    rds.lrem(keys.FIRST_RCMD_Q % uid, count=0, value=sid)

    # 给被滑动者增加滑动积分
    rds.zincrby(keys.HOT_RANK, config.SWIPE_SCORE['like'], sid)

    # 检查对方是否喜欢(右滑或上滑)过自己
    if Swiped.is_liked(sid, uid):
        # 将互相喜欢的两人添加成好友
        Friend.make_friends(uid, sid)
        return True
    else:
        return False


@atomic
def superlike_someone(uid, sid):
    '''超级喜欢某人 (上滑)'''

    # 添加滑动记录
    Swiped.swipe(uid, sid, 'superlike')

    # 强制删除优先推荐队列中的 sid
    rds.lrem(keys.FIRST_RCMD_Q % uid, count=0, value=sid)

    # 给被滑动者增加滑动积分
    rds.zincrby(keys.HOT_RANK, config.SWIPE_SCORE['superlike'], sid)

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


def dislike_someone(uid, sid):
    '''不喜欢某人（左滑）'''
    # 添加滑动记录
    Swiped.swipe(uid, sid, 'dislike')

    # 强制删除优先推荐队列中的 sid
    rds.lrem(keys.FIRST_RCMD_Q % uid, count=0, value=sid)

    # 给被滑动者增加滑动积分
    rds.zincrby(keys.HOT_RANK, config.SWIPE_SCORE['dislike'], sid)


def rewind_last_swipe(uid):
    '''反悔上一次滑动 (每天允许反悔 3 次， 反悔的记录只能是五分钟之内的)'''
    now = datetime.datetime.now()

    # 检查今天是否已经反悔 3 次
    rewind_key = keys.REWIND_TIMES_K % (now.date(), uid)
    rewind_times = rds.get(rewind_key, 0)
    if rewind_times >= config.REWIND_TIMES:
        raise errors.RewindLimit

    # 找到最后一次滑动
    last_swipe = Swiped.objects.filter(uid=uid).latest('stime')

    # 检查最后一次滑动是否在 5 分钟之内
    time_past = (now - last_swipe.stime).total_seconds()
    if time_past >= config.REWIND_TIMEOUT:
        raise errors.RewindTimeout

    with atomic(): # 将多次数据修改在事务中执行
        if last_swipe.stype in ['like', 'superlike']:
            # 如果之前匹配成了好友，则删除好友关系
            Friend.breakoff(uid, last_swipe.sid)
            # 如果上一次是超级喜欢，则删除优先推荐队列中的数据
            if last_swipe.stype == 'superlike':
                rds.lrem(keys.FIRST_RCMD_Q % last_swipe.sid, 0, uid)

        # 撤销被滑动者改变的积分
        score = config.SWIPE_SCORE[last_swipe.stype]
        rds.zincrby(keys.HOT_RANK, -score, last_swipe.sid)

        # 删除最后一次的滑动
        last_swipe.delete()

        # 今日反悔次数加一
        rds.set(rewind_key, rewind_times + 1, 86460) # 缓存过期时间为一天零60秒

def find_my_fans(uid):
    '''查找我的粉丝'''
    # 取出自己滑过的用户
    sid_list = Swiped.objects.filter(uid=uid).values_list('sid', flat=True)

    # 所有喜欢自己的人
    fans_id_list = Swiped.objects.filter(sid=uid, stype__in=['like', 'superlike'])\
                                .exclude(uid__in=sid_list).values_list('uid', flat=True)

    users = User.objects.filter(id__in=fans_id_list)
    return users

def get_top_n(num):
    """获取排行榜前 N 的用户数据"""
    origin_rank = rds.zrevrange(keys.HOT_RANK, 0, num - 1, withscores=True)  # 从 Redis 中取出前 N 的原始数据
    cleaned_rank = [[int(uid), int(score)] for uid, score in origin_rank] # 将原始数据中的每一项强转成int

    # 取出前 N 个用户
    uid_list = [uid for uid, _ in cleaned_rank] # 用户的 ID 列表
    users = User.objects.filter(id__in=uid_list)
    users = sorted(users, key=lambda user: uid_list.index(user.id))

    # 整理用户数据
    rank_data = []
    for index, (uid ,score) in enumerate(cleaned_rank):
        rank = index + 1
        user = users[index]
        user_data = user.to_dict(exclude=['phonenum', 'birthday', 'location',
                                          'vip_id', 'vip_expire'])
        user_data['rank'] = rank
        user_data['score'] = score
        rank_data.append(user_data)

    return rank_data

