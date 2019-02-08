from __future__ import unicode_literals
import pymysql
from django.db import models
from rest_framework.pagination import LimitOffsetPagination


# Create your models here.
class Businfo(models.Model):
    id = models.IntegerField(primary_key=True)
    bname = models.CharField(max_length=50)
    uptime = models.CharField(max_length=50, blank=True, null=True)
    dwtime = models.CharField(max_length=50, blank=True, null=True)
    price = models.CharField(max_length=50, blank=True, null=True)
    company = models.CharField(max_length=50, blank=True, null=True)
    updata = models.CharField(max_length=32, blank=True, null=True)
    upcount = models.CharField(max_length=32, blank=True, null=True)
    upsite = models.CharField(max_length=500, blank=True, null=True)
    dwcount = models.CharField(max_length=32, blank=True, null=True)
    dwsite = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'businfo'


class StandardResultSetPagination(LimitOffsetPagination):
    default_limit = 20              # 默认每页显示的条数
    limit_query_param = 'limit'     # url 中传入的显示数据条数的参数
    offset_query_param = 'offset'   # url中传入的数据位置的参数
    max_limit = None                # 最大每页显示条数