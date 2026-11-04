from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
    """
    Pagination personnalisée avec des informations supplémentaires.
    """
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 50 

    def get_paginated_response(self, data):
        """
        Retourne une réponse paginée personnalisée.
        """
        return Response({
            'total_count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })








    