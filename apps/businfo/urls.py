# -*- coding: utf-8 -*-
""" 
 @Author   : hawk
 @Email    : a8926764@163.com
 @Time     : 2019/2/3 16:35
 @Version  : 1.0
 @Function : 
"""
from django.urls import path
from . import views

app_name = 'businfo'
urlpatterns = [
    path('getlist/', views.getlist, name='index'),

]