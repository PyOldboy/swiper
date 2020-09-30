import logging

from common import errors, keys
from libs.http import render_json
from libs.cache import rds
from libs.qn_cloud import gen_token, get_res_url
from user.forms import UserForm, ProfileForm
from user.logics import send_vcode
from user.models import User, Profile
from user.serializers import ASerializer

inf_log = logging.getLogger('inf')

def fetch_vcode(request):
    '''给用户发送验证码'''
    phonenum = request.GET.get('phonenum')

    send_vcode.delay(phonenum)  # 异步发送短信验证码
    return render_json()


def submit_vcode(request):
    phonenum = request.POST.get('phonenum')
    vcode = request.POST.get('vcode')

    key = keys.VCODE_K % phonenum
    cached_vcode = rds.get(key)

    if vcode and vcode == cached_vcode:
        try:
            user = User.objects.get(phonenum=phonenum)
            inf_log.info(f'User Login: {user.id} / {user.phonenum}')
        except User.DoesNotExist:
            user = User.objects.create(phonenum=phonenum, nickname=phonenum)
            inf_log.info(f'User Register: {user.id} / {user.phonenum}')

        request.session['uid'] = user.id
        return render_json(user.to_dict())

    else:
        raise errors.VcodeErr('验证码错误')


def show_profile(request):
    uid = request.session['uid']
    profile, _ = Profile.objects.get_or_create(id=uid)

    # profile_serializer = ASerializer(social)

    return render_json(ASerializer(profile).data)


def update_profile(request):
    user_form = UserForm(request.POST)
    profile_form = ProfileForm(request.POST)

    if user_form.is_valid() and profile_form.is_valid():
        uid = request.session['uid']

        User.objects.filter(id=uid).update(**user_form.cleaned_data)
        Profile.objects.update_or_create(id=uid, defaults=profile_form.cleaned_data)
        return render_json()
    else:
        err = {}
        err.update(user_form.errors)
        err.update(profile_form.errors)
        raise errors.ProfileErr(data=err)

def qn_token(request):
    uid = request.session['uid']
    filename = f'Avatar-{uid}'
    token = gen_token(uid, filename)
    return render_json({'token': token, 'key': filename})


def qn_callback(request):
    uid = request.POST.get('uid')
    key = request.POST.get('key')
    avatar_url = get_res_url(key)
    User.objects.filter(id=uid).update(avatar=avatar_url)
    return render_json(avatar_url)
