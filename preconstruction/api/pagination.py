from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination


class PreconstructionPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page'
    max_page_size = 1000
    page_size_query_param = 'size'
    max_page_size = 100

# class PreconstrctionOfPage(LimitOffsetPagination):
#     default_limit = 10
    

# class PreconCursorPage(CursorPagination):
#     page_size = 5
#     ordering = 'created'
