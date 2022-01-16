# Generated by Django 2.2.20 on 2021-11-15 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20210606_1546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.TextField(default='QTechCode是一个基于izone搭建的专业Python技能分享平台，分享包含Python基础知识、机器学习、神经网络算法、Web技术、信息安全技术、爬虫技术、图像处理技术等诸多内容。', help_text='用来作为SEO中description,长度参考SEO标准', max_length=240, verbose_name='描述'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='description',
            field=models.TextField(default='QTechCode是一个基于izone搭建的专业Python技能分享平台，分享包含Python基础知识、机器学习、神经网络算法、Web技术、信息安全技术、爬虫技术、图像处理技术等诸多内容。', help_text='用来作为SEO中description,长度参考SEO标准', max_length=240, verbose_name='描述'),
        ),
    ]
