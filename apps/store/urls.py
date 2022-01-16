# -*- coding: utf-8 -*-
from django.urls import path
# from .views import goview
from .views import IndexView, DetailView, PayView, CallbackView, DeliverView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),  # 主页，自然排序
    path('goods/<slug:slug>/', DetailView.as_view(), name='detail'),
    path('pay/', PayView, name='pay'),
    path('callback/', CallbackView, name='callback'),
    path('deliver/', DeliverView, name='deliver'),
]