from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.businfo.models import Businfo, StandardResultSetPagination
from apps.businfo.serializers import BusinfoSerializer, ListSerialize


# Create your views here.


@api_view(['GET', 'POST'])
def getlist(request, format=None):
    if request.method == 'GET':
        businfo = Businfo.objects.all()
        serializer = BusinfoSerializer(businfo, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = BusinfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# @api_view(['GET', 'POST'])
# def getlist(request, format=None):
#     if request.method == 'GET':
#         businfo = Businfo.objects.values('id', 'bname').distinct()
#         serializer = BusinfoSerializer(businfo, many=True)
#
#         # http: // 127.0.0.1:8000 / getlist?limit = 20
#         # http: // 127.0.0.1:8000 / getlist?limit = 20 & offset = 20
#         # http: // 127.0.0.1:8000 / getlist?limit = 20 & offset = 40
#
#         # 根据url参数 获取分页数据
#         obj = StandardResultSetPagination()
#         page_list = obj.paginate_queryset(businfo, request)
#
#         # 对数据序列化 普通序列化 显示的只是数据
#         ser = ListSerialize(instance=page_list, many=True)
#         response = obj.get_paginated_response(ser.data)
#         return response
#
#
# @api_view(['GET', 'POST'])
# def getlisinfo(request, format=None):
#     if request.method == 'GET':
#         id = request.GET['id']
#         if id is not None:
#             businfo = Businfo.objects.filter(id=id)
#             obj = StandardResultSetPagination()
#             page_list = obj.paginate_queryset(businfo, request)
#             ser = ListSerialize(instance=page_list, many=True)
#             response = obj.get_paginated_response(ser.data)
#             return response
