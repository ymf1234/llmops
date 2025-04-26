from enum import Enum


class HttpCode(str, Enum):
    SUCCESS = 'SUCCESS'
    FAIL = 'FAIL'
    NOT_FOUND = 'NOT_FOUND'
    UNAUTHORIZED = 'UNAUTHORIZED'
    FORBIDDEN = 'FORBIDDEN'
    VALIDATE_ERROR = 'VALIDATE_ERROR'
