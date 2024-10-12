""" 使用说明
from rest_framework import viewsets

class ExampleViewSet(viewsets.ModelViewSet, BaseGenericAPIView):
    # 示例视图集，继承自 BaseGenericAPIView。
    # - queryset: 数据集
    # - serializer_class: 序列化器类

    queryset = ExampleModel.objects.all()
    serializer_class = ExampleSerializer

"""


from rest_framework import mixins, generics, status
from rest_framework.response import Response
from rest_framework import viewsets

class BaseGenericAPIView(viewsets.ModelViewSet):
    def get_queryset(self):
        """这里设置了排序"""
        return self.queryset.order_by('id')

    def http_OK_response(self, message, data):
        """
        返回一个 HTTP 200 OK 响应。

        :param message: 响应消息
        :param data: 响应数据
        :return: Response 对象
        """
        return Response({'code':0,'message': message, 'data': data}, status=status.HTTP_200_OK)

    def http_BAD_response(self, message, data):
        """
        返回一个 HTTP 400 BAD REQUEST 响应。

        :param message: 响应消息
        :param data: 响应数据
        :return: Response 对象
        """
        return Response({'code':1,'message': message, 'data': data}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        """
        新建记录。

        1. 验证请求数据。
        2. 检查记录是否已存在。
        3. 如果记录不存在，创建新记录。
        4. 返回创建结果。
        """
        # 获取请求数据
        serializer = self.get_serializer(data=request.data)
        # 检查数据有效性
        if serializer.is_valid():
            # 在这里检查记录是否已经存在
            model_class = self.get_queryset().model
            existing_instance = model_class.objects.filter(**serializer.validated_data).first()
            if existing_instance:
                # 如果存在相同的记录，则返回错误响应
                return self.http_BAD_response(message='记录已存在', data={})

            # 如果不存在，则继续创建
            self.perform_create(serializer)
            return self.http_OK_response(message='创建成功', data={})

        # 如果数据无效，返回错误信息
        return self.http_BAD_response(message=serializer.errors, data={})

    def perform_create(self, serializer):
        """
        实际创建记录的方法。

        :param serializer: 序列化器对象
        """
        serializer.save()

    def update(self, request, *args, **kwargs):
        """
        更新记录。

        1. 获取要更新的实例。
        2. 验证请求数据。
        3. 更新实例。
        4. 返回更新结果。
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()  # 这里已经检查了实例是否存在
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return self.http_OK_response(message='更新成功', data={})

    def perform_update(self, serializer):
        """
        实际更新记录的方法。

        :param serializer: 序列化器对象
        """
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        """
        部分更新记录。

        1. 设置 partial 参数为 True。
        2. 调用 update 方法。
        """
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)



    def destroy(self, request, *args, **kwargs):
        """
        删除记录。

        1. 获取要删除的实例。
        2. 删除实例。
        3. 返回删除成功的结果。
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return self.http_OK_response(message='删除成功', data={})

    def perform_destroy(self, instance):
        """
        实际删除记录的方法。

        :param instance: 要删除的实例
        """
        instance.delete()

    def retrieve(self, request, *args, **kwargs):
        """
        查询单个记录。

        1. 获取要查询的实例。
        2. 序列化实例。
        3. 返回查询结果。
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return self.http_OK_response(message='查询成功', data=serializer.data)

    def list(self, request, *args, **kwargs):
        """
        获取数据列表。

        1. 获取查询集并过滤。
        2. 处理分页。
        3. 序列化查询集。
        4. 返回查询结果。
        """
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        # 处理分页
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = self.get_paginated_response(serializer.data).data
            return self.http_OK_response(message='成功', data=data)

        # 不分页时
        serializer = self.get_serializer(queryset, many=True)
        return self.http_OK_response(message='查询成功', data=serializer.data)