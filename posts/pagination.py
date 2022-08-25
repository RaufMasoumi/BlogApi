from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 20
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_page_size(self, request):
        if request.query_params.get('page_size') == 'max':
            # The query_params is not mutable so making it mutable and again immutable.
            _mutable = request.query_params._mutable
            request.query_params._mutable = True
            request.query_params.update({'page_size': self.max_page_size})
            request.query_params._mutable = _mutable

        return super().get_page_size(request)
