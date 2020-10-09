from django.test import TestCase
from unittest.mock import Mock

from common.errors import PermissionErr
from user.models import User
from vip.models import Vip, Permission, VipPermRelation
from social.apis import superlike

class UserTest(TestCase):

    @staticmethod
    def init_permission():
        """创建权限模型"""
        permissions = (
            ('vipflag', '会员身份标识'),
            ('superlike', '超级喜欢'),
            ('rewind', '反悔功能'),
            ('anylocation', '任意更改定位'),
            ('unlimit_like', '无限喜欢次数'),
            ('show_fans', '查看喜欢过我的人'),
        )
        for name, desc in permissions:
            perm, _ = Permission.objects.get_or_create(name=name, description=desc)
            print('create permission %s' % perm.name)

    @staticmethod
    def init_vip():
        vip_data = (
            ('非会员', 0, 100000, 0),

            ('青铜会员(月卡)', 1, 30, 10),
            ('青铜会员(半年卡)', 1, 180, 50),
            ('青铜会员(年卡)', 1, 365, 90),

            ('白银会员(月卡)', 2, 30, 20),
            ('白银会员(半年卡)', 2, 180, 100),
            ('白银会员(年卡)', 2, 365, 180),

            ('黄金会员(月卡)', 3, 30, 40),
            ('黄金会员(半年卡)', 3, 180, 220),
            ('黄金会员(年卡)', 3, 365, 360),
        )
        for name, level, dur, price in vip_data:
            vip, _ = Vip.objects.get_or_create(
                name=name,
                level=level,
                duration=dur,
                price=price
            )
            print('create %s' % vip.name)

    @staticmethod
    def create_vip_perm_relations():
        """创建 Vip 和 Permission 的关系"""
        # 获取权限
        vipflag = Permission.objects.get(name='vipflag')
        superlike = Permission.objects.get(name='superlike')
        rewind = Permission.objects.get(name='rewind')
        anylocation = Permission.objects.get(name='anylocation')
        unlimit_like = Permission.objects.get(name='unlimit_like')
        show_fans = Permission.objects.get(name='show_fans')

        # 给 VIP 1 分配权限
        VipPermRelation.objects.get_or_create(vip_level=1, perm_id=vipflag.id)
        VipPermRelation.objects.get_or_create(vip_level=1, perm_id=superlike.id)

        # 给 VIP 2 分配权限
        VipPermRelation.objects.get_or_create(vip_level=2, perm_id=vipflag.id)
        VipPermRelation.objects.get_or_create(vip_level=2, perm_id=superlike.id)
        VipPermRelation.objects.get_or_create(vip_level=2, perm_id=rewind.id)

        # 给 VIP 3 分配权限
        VipPermRelation.objects.get_or_create(vip_level=3, perm_id=vipflag.id)
        VipPermRelation.objects.get_or_create(vip_level=3, perm_id=superlike.id)
        VipPermRelation.objects.get_or_create(vip_level=3, perm_id=rewind.id)
        VipPermRelation.objects.get_or_create(vip_level=3, perm_id=anylocation.id)
        VipPermRelation.objects.get_or_create(vip_level=3, perm_id=unlimit_like.id)
        VipPermRelation.objects.get_or_create(vip_level=3, perm_id=show_fans.id)

    def create_vip_data(self):
        self.init_permission()
        self.init_vip()
        self.create_vip_perm_relations()

    def setUp(self):
        """准备测试数据"""
        self.create_vip_data()
        User.objects.create(
            phonenum='15601185621',
            nickname='Seamile',
            gender='male',
            birthday='1990-01-01',
            location='北京'
        )
        self.user1 = User.objects.get(phonenum='15601185621')

        User.objects.create(
            phonenum='15612345678',
            nickname='Kitty',
            gender='female',
            birthday='1990-01-01',
            location='上海'
        )
        self.user2 = User.objects.get(phonenum='15612345678')


    def test_superlike(self):
        # 伪造 request
        request = Mock()
        request.uid = self.user1.id
        request.POST = {'sid': self.user2.id}

        # 测试非会员的情况
        with self.assertRaises(PermissionErr):
            superlike(request)

        # 测试会员的情况
        self.user1.set_vip(7)
        response = superlike(request)
        self.assertEqual(response.status_code, 200)