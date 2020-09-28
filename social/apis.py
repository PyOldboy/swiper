from libs.http import render_json
from social import logics
from social.models import Friend
from user.models import User


def rcmd_users(request):
    '''获取推荐用户'''
    users = logics.rcmd(request.uid)
    users_data = [user.to_dict() for user in users]
    return render_json(users_data)


def like(request):
    '''喜欢 (右滑)'''
    sid = int(request.POST.get('sid'))
    matched = logics.like_someone(request.uid, sid)
    return render_json({'is_matched': matched})


def superlike(request):
    '''超级喜欢 (上滑)'''
    sid = int(request.POST.get('sid'))
    matched = logics.superlike_someone(request.uid, sid)
    return render_json({'is_matched': matched})


def dislike(request):
    '''不喜欢 (左滑)'''
    sid = int(request.POST.get('sid'))
    logics.dislike_someone(request.uid, sid)
    return render_json()


def rewind(request):
    '''反悔'''
    logics.rewind_last_swipe(request.uid)
    return render_json()


def show_fans(request):
    '''查看喜欢过我的人'''
    fans = logics.find_my_fans(request.uid)
    user_data = [u.to_dict for u in fans]
    return render_json(user_data)


def show_friends(request):
    '''查看好友'''
    fid_list = Friend.friend_ids(request.uid)
    friends = User.objects.filter(id__in=fid_list)
    user_data = [u.to_dict for u in friends]
    return render_json(user_data)
