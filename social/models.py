from django.db import models, IntegrityError

# Create your models here.
from common import errors


class Swiped(models.Model):
    '''滑动记录表'''
    STYPES = (
        ('like', '喜欢'),
        ('superlike', '超级喜欢'),
        ('dislike', '不喜欢')
    )

    uid = models.IntegerField(verbose_name='滑动者的 ID')
    sid = models.IntegerField(verbose_name='被滑动者的 ID')
    stype = models.CharField(max_length=10, choices=STYPES, verbose_name='滑动类型')
    stime = models.DateTimeField(auto_now_add=True, verbose_name='滑动时间')

    class Meta:
        unique_together = ['uid', 'sid']

    @classmethod
    def swipe(cls, uid, sid, stype):
        try:
            cls.objects.create(uid=uid, sid=sid, stype=stype)
        except IntegrityError:
            # 跑出重复滑动异常
            raise errors.RepeatSwipeErr

    @classmethod
    def is_liked(cls, uid, sid):
        # 检查是否喜欢过某人
        swiped = Swiped.objects.filter(uid=uid, sid=sid).first()
        if not swiped:
            return None  # 用户尚未滑到 sid
        elif swiped.stype in ['like', 'superlike']:
            return True  # 喜欢过
        else:
            return False  # 不喜欢


class Friend(models.Model):
    uid1 = models.IntegerField(verbose_name='UID 1')
    uid2 = models.IntegerField(verbose_name='UID 2')

    class Meta:
        unique_together = ['uid1', 'uid2']

    @classmethod
    def make_friends(cls, uid1, uid2):
        '''创建好友关系'''
        uid1, uid2 = (uid2, uid1) if uid1 > uid2 else (uid1, uid2)  # 调整两者位置
        cls.objects.create(uid1=uid1, uid2=uid2)
