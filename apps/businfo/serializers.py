# -*- coding: utf-8 -*-
""" 
 @Author   : hawk
 @Email    : a8926764@163.com
 @Time     : 2019/2/3 16:44
 @Version  : 1.0
 @Function : 提供序列化和反序列化的途径，使之可以转化为，某种表现形式如json。
"""
from rest_framework import serializers
from apps.businfo.models import Businfo


class BusinfoSerializer(serializers.ModelSerializer):
    # ModelSerializer和Django中ModelForm功能相似
    # Serializer和Django中Form功能相似
    class Meta:
        model = Businfo
        fields = ('bname', 'uptime', 'dwtime', 'price', 'company', 'updata', 'upcount', 'upsite', 'dwcount', 'dwsite')


class ListSerialize(serializers.ModelSerializer):
    class Meta:
        model = Businfo
        fields = ('id', 'bname')


class ListInfoSerialalize(serializers.ModelSerializer):
    class Meta:
        model = Businfo
        fields = "__all__"
