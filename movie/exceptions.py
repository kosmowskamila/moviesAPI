from rest_framework.exceptions import APIException


class NoDateRangeException(APIException):
    status_code = 400
    default_code = 'no-date-range'
    default_detail = 'Please, provide start and end dates.'


class InvalidDateException(APIException):
    status_code = 400
    default_code = 'invalid-date'
    default_detail = 'Invalid date of format (should be YYYY-MM-DD)'


class InvalidRangeException(APIException):
    status_code = 400
    default_code = 'invalid-range'
    default_detail = 'Start date cannot be bigger than end date!'
