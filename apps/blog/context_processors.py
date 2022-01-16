# -*- coding: utf-8 -*-

from django.conf import settings
from .utils import site_full_url


# 自定义上下文管理器
def settings_info(request):
    return {
        'site_logo_name': settings.SITE_LOGO_NAME,
        'site_end_title': settings.SITE_END_TITLE,
        'site_description': settings.SITE_DESCRIPTION,
        'site_keywords': settings.SITE_KEYWORDS,
        'tool_flag': settings.TOOL_FLAG,
        'api_flag': settings.API_FLAG,
        'store_flag': settings.STORE_FLAG,
        'resource_flag': settings.RESOURCE_FLAG,
        'cnzz_protocol': settings.CNZZ_PROTOCOL,
        'beian': settings.BEIAN,
        'my_github': settings.MY_GITHUB,
        'my_csdn': settings.MY_CSDN,
        'site_verification': settings.MY_SITE_VERIFICATION,
        'site_url': site_full_url(),
        'hao_console': settings.HAO_CONSOLE,
        'notice_flag': settings.NOTICE_FLAG,
        'notice_content': settings.NOTICE_CONTENT
    }
