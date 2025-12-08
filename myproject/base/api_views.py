from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class MultiSerializerViewSetMixin:
    serializer_action_classes = {}

    def get_serializer_class(self):
        serializer = self.serializer_action_classes.get(self.action)
        if not serializer:
            serializer = super().get_serializer_class()
        return serializer


class DefaultPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'

    def paginate_queryset(self, queryset, request, view=None):
        paginate = bool(request.query_params.get('page', None))
        if paginate:
            return super().paginate_queryset(queryset, request, view)
        return None

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('total_pages', self.page.paginator.num_pages),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))
