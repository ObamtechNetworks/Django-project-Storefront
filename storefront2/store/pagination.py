from rest_framework.pagination import PageNumberPagination

class DefaultPagination(PageNumberPagination):
    page_size = 10
    # page_size_query_param = 'page_size'  # Allow client to set the page size using ?page_size=xyz
    # max_page_size = 100  # Maximum limit for page size to prevent excessive data load