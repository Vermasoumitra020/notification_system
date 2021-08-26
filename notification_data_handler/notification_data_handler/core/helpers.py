from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


API_RESPONSE_MSG = dict(
    DONE='Done',
    ERROR='Error',
    SERIALIZER_DATA_NOT_FOUND='serializer_data_not_found',
    PLEASE_ENTER_DOCUMENTS="Documents data are not available in DB please enter the documents data",
    REQUEST_NOT_FOUND="User request data not found please use your request data",
    DOCUMENT_NOT_DEFINED="This documents id not found in DB please enter correct Document details id"
)

"""
API RESPONSE PARSER
"""
class APIResponseParser:
    """
    ApiResponseParser
    Common api Response Parser for all API Response.
    """

    def __init__(self):
        pass

    @staticmethod
    def response(**api_response_data):
        """
        kwargs: all Kwargs Parameter comes from to APIView Class.
        return: Response
        """
        try:
            if api_response_data['status']:
                return Response(
                    {
                        'status': api_response_data['status'],
                        'message': api_response_data['message'],
                        api_response_data['result']: api_response_data['data'],
                    }
                )
            return Response(
                {
                    'message': api_response_data['message'],
                    'status': False
                }
            )
        except Exception as msg:
            return Response(
                {
                    'message': "APIResponseParser.response.errors",
                    'errors': str(msg),
                    'status': False
                }
            )

    @staticmethod
    def responses(**api_response_data):
        """
        kwargs: all Kwargs Parameter comes from to APIView Class.
        return: Response
        """
        json_response = {}
        try:
            if api_response_data['status']:
                for key, values in api_response_data['data'].items():
                    json_response[key] = values
                json_response['message'] = api_response_data['message']
                json_response['status'] = api_response_data['status']
                return Response(json_response)
            return Response(
                {
                    'message': api_response_data['message'],
                    'status': False
                }
            )
        except Exception as msg:
            return Response(
                {
                    'message': "APIResponseParser.response.errors",
                    'errors': str(msg),
                    'status': False
                }
            )


class PaginationResponse(PageNumberPagination):
    '''get pagination resonse
        of all data'''
    page_size = 20

    @staticmethod
    def get_pagination_response(self, data):
        try:
            return Response(
                {
                    "links": {
                        'next': self.get_next_link(),
                        'previous': self.get_previous_link()
                    },
                    "count": self.page.paginator.count,
                    'pagesize': self.page_size,
                    'result': data
                }
            )
        except Exception as e:
            return Response(
                {
                    'message': "APIResponseParser.response.errors",
                    'errors': str(e),
                    'status': False
                }
            )


class DocumentListPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'limits'


class PaginationHandlerMixin(object):

    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        else:
            pass
        return self._paginator

    def paginate_queryset(self, queryset):

        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset,
                                                self.request, view=self)

    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)


""" Custom Serializers Errors
"""
class SerializerErrorParser:
    """
    SerializerErrorParser : Serializer error Parser Class Used to split the serializer errors in
    two parts key and Values, key define the error of key and value define what is the
    error in this Key.
    # {'email': ['Enter a valid e-mail address.'], 'created': ['This field is required.']}
    """

    def __init__(self, un_error_message):
        self.error_message = un_error_message

    def __call__(self):
        """
        manipulate serializer error
        """
        try:
            return self.serializer_error_parser()
        except Exception as exception_error:
            print("SerializerErrorParser.Exception.message")
            print(exception_error)
            return None, None

    def serializer_error_parser(self):
        """
        manipulate the serializer error for api response
        return: key and error
        """
        if isinstance(self.error_message, dict):
            error_keys = list(self.error_message.keys())
            if len(error_keys) > 0:
                return error_keys[0], self.error_message[error_keys[0]][0]
            return None, None

        if isinstance(self.error_message, list):
            error_list = list(filter(lambda x: list(x.keys()), self.error_message))
            if error_list:
                error_parse = error_list[0]
                error_keys = list(error_parse.keys())
                if len(error_keys) > 0:
                    return error_keys[0], error_parse[error_keys[0]][0]
                return None, None
