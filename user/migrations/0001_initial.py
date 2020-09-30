# Generated by Django 2.2.16 on 2020-09-23 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phonenum', models.CharField(max_length=16, unique=True, verbose_name='手机号')),
                ('nickname', models.CharField(db_index=True, max_length=20, verbose_name='昵称')),
                ('gender', models.CharField(choices=[('male', '男性'), ('female', '女性')], max_length=10, verbose_name='性别')),
                ('birthday', models.DateField(default='2002-01-01', verbose_name='出生日')),
                ('avatar', models.CharField(max_length=256, verbose_name='个人形象')),
                ('location', models.CharField(choices=[('北京', '北京'), ('上海', '上海'), ('深圳', '深圳'), ('成都', '成都'), ('西安', '西安'), ('武汉', '武汉'), ('沈阳', '沈阳')], max_length=10, verbose_name='常居地')),
            ],
        ),
    ]
