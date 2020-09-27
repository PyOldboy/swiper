import datetime

from user.models import User
from user.models import Profile

def rcmd(uid):
    '''推荐滑动用户'''
    profile = Profile.objects.get(id=uid)

    today = datetime.date.today()
    earliest_birth = today - datetime.timedelta(profile.max_dating_age*365) # 最早出生日期
    latest_birth = today - datetime.timedelta(profile.min_dating_age*365)   # 最晚出生日期

    users = User.objects.filter(
        location= profile.dating_location,
        gender=profile.dating_gender,
        birthday__range=[earliest_birth,latest_birth],
    )[:20]  # 懒加载

    # TODO：排除已经滑过的人

    return users