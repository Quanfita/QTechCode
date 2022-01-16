# -*- coding: utf-8 -*-
from django.urls import path
from .views import profile_view, change_profile_view, history_order_view


urlpatterns = [
    path('profile/',profile_view,name='profile'),
    path('profile/change/',change_profile_view,name='change_profile'),
    path('history_order/',history_order_view,name='history_order'),
]