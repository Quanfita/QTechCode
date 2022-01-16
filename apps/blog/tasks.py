from __future__ import absolute_import, unicode_literals
from celery import shared_task
from tool.apis.bd_push import get_urls, push_urls

@shared_task
def push_baidu_urls():
    return push_urls('http://data.zz.baidu.com/urls?site=https://quanfita.cn&token=s6TjmYFCEdzfPGru',get_urls('https://quanfita.cn/sitemap.xml'))

