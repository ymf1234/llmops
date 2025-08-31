from dataclasses import field
from typing import Any

from pkg.response import HttpCode


# 客户异常类
class CustomException(Exception):
    """基础自定义异常信息"""

    code: HttpCode = HttpCode.FAIL
    message: str = ""
    data: Any = field(default_factory=dict)

    def __init__(self, message: str, data: Any = None):
        super().__init__()
        self.message = message
        self.data = data


# 通用失败异常
class FailException(CustomException):
    """通用失败异常"""
    pass


# 未找到数据异常
class NotFoundException(CustomException):
    """未找到数据异常"""
    code = HttpCode.NOT_FOUND


# 未授权异常
class UnauthorizedException(CustomException):
    """未授权异常"""
    code = HttpCode.UNAUTHORIZED


# 权限异常
class ForbiddenException(CustomException):
    """权限异常"""
    code = HttpCode.FORBIDDEN


class ValidateException(CustomException):
    """参数验证异常"""
    code = HttpCode.VALIDATE_ERROR
