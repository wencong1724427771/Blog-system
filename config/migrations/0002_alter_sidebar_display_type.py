# Generated by Django 3.2.7 on 2021-09-25 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sidebar',
            name='display_type',
            field=models.PositiveIntegerField(choices=[(1, 'HTML'), (2, '最新文章'), (3, '热门文章'), (4, '最近评论')], default=1, verbose_name='展示类型'),
        ),
    ]