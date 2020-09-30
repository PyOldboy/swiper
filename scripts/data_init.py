import os
import random
import sys
from datetime import date
from user.models import User

import django

# 第一步：将项目的绝对路径加载到 sys.path
from vip.models import VipPermRelation, Permission, Vip

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

# 第二步：设置环境变量 DJANGO_SETTINGS_MODULE
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tantan.settings')

# 第三步：Django 环境初始化
django.setup()

last_names = (
    '赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨'
    '朱秦尤许何吕施张孔曹严华金魏陶姜'
    '戚谢邹喻柏水窦章云苏潘葛奚范彭郎'
    '鲁韦昌马苗凤花方俞任袁柳酆鲍史唐'
    '费廉岑薛雷贺倪汤滕殷罗毕郝邬安常'
    '乐于时傅皮卞齐康伍余元卜顾孟平黄'
)

first_names = {
    'male': [
        '致远', '俊驰', '雨泽', '烨磊', '晟睿',
        '天佑', '文昊', '修洁', '黎昕', '远航',
        '旭尧', '鸿涛', '伟祺', '荣轩', '越泽',
        '浩宇', '瑾瑜', '皓轩', '浦泽', '绍辉',
        '绍祺', '升荣', '圣杰', '晟睿', '思聪'
    ],
    'female': [
        '沛玲', '欣妍', '佳琦', '雅芙', '雨婷',
        '韵寒', '莉姿', '雨婷', '宁馨', '妙菱',
        '心琪', '雯媛', '诗婧', '露洁', '静琪',
        '雅琳', '灵韵', '清菡', '溶月', '素菲',
        '雨嘉', '雅静', '梦洁', '梦璐', '惠茜'
    ]
}


def random_name(gender):
    """随机产生一个名字"""
    last_name = random.choice(last_names)
    first_name = random.choice(first_names[gender])
    return last_name + first_name


def create_robots(n):
    # 创建初始用户
    for i in range(n):
        uid = i + 1
        gender = ['male', 'female'][i % 2]
        name = random_name(gender)
        year = random.randint(1970, 2000)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        try:
            user, _ = User.objects.update_or_create(
                id=uid,
                defaults={
                    'phonenum': '%s' % random.randrange(20000000000, 30000000000),
                    'nickname': name,
                    'gender': gender,
                    'birthday': date(year, month, day),
                    'location': random.choice([item[0] for item in User.LOCATIONS]),
                    'avatar': f'http://disk.swiper.seamile.cn/Avatar-{uid}'
                }
            )
            print(f'created: {user.id} {name} {gender}')
        except django.db.utils.IntegrityError:
            pass


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


def create_vip_data():
    init_permission()
    init_vip()
    create_vip_perm_relations()


if __name__ == '__main__':
    # 解析脚本执行的参数
    if len(sys.argv) >= 2:
        command = sys.argv[1]
        if command == 'create_robots':
            create_robots(1000)
        elif command == 'create_vip':
            create_vip_data()
        else:
            print('未知的命令')
            sys.exit(2)
    else:
        create_robots(1000)
        create_vip_data()
