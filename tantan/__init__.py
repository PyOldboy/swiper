from libs.orm import path_orm


# 抢在 settings 加载之前，为 Django 的 ORM 执行猴子补丁，增加缓存处理
path_orm()
