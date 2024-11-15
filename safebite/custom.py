from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPaginator(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'per_page': self.get_page_size(self.request),
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })