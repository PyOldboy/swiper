from django.db.models import query
from django.db import models

from libs.cache import rds
from common.keys import MODEL_K


def get(self, *args, **kwargs):
    """
    Perform the query and return a single object matching the given
    keyword arguments.
    """
    cls_name = self.model.__name__
    pk = kwargs.get('pk') or kwargs.get('id')
    if pk is not None:
        # 先从缓存获取数据
        key = MODEL_K % (cls_name, pk)
        model_obj = rds.get(key)
        if isinstance(model_obj, self.model):
            return model_obj

    # 缓存中没有数据，从数据库取出数据
    model_obj = self._get(*args, **kwargs)

    # 将数据写入到缓存中，方便下次使用
    key = MODEL_K % (cls_name, model_obj.pk)
    rds.set(key, model_obj)
    return model_obj


def save(self, force_insert=False, force_update=False, using=None,
         update_fields=None):
    """
    Save the current instance. Override this in a subclass if you want to
    control the saving process.

    The 'force_insert' and 'force_update' parameters can be used to insist
    that the "save" must be an SQL insert or update (or equivalent for
    non-SQL backends), respectively. Normally, they should not be set.
    """
    # 调用原 save 方法将数据保存到 数据库
    self._save(force_insert, force_update, using, update_fields)

    # 将对象保存到 缓存
    key = MODEL_K % (self.__class__.__name__, self.pk)
    rds.set(key, self)


def path_orm():
    '''通过 Monkey Patch 的方式为 ORM 增加缓存处理'''
    query.QuerySet._get = query.QuerySet.get
    query.QuerySet.get = get

    models.Model._save = models.Model.save
    models.Model.save = save