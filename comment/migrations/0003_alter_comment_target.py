# Generated by Django 3.2.7 on 2021-09-25 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0002_rename_targrt_comment_target'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='target',
            field=models.CharField(max_length=100, verbose_name='评论目标'),
        ),
    ]