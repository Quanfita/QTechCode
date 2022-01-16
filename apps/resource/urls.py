# -*- coding: utf-8 -*-
from django.urls import path
# from .views import goview
from .views import IndexView, DetailView, update_downloads

urlpatterns = [
    path('', IndexView.as_view(), name='index'),  # 主页，自然排序
    path('update_downloads/', update_downloads, name='update_downloads'),
    path('<slug:slug>/', DetailView.as_view(), name='detail'),
]