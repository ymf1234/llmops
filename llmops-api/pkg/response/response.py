from dataclasses import dataclass, field
from typing import Any

from flask import jsonify, Response

from .http_code import HttpCode


@dataclass
class Response:
    """基础 HTTP 接口响应格式"""
    code: HttpCode.SUCCESS
    message: str = ""

    data: Any = field(default_factory=dict)


def json(data: Response = None):
    """基础的响应接口"""
    response = jsonify(data)
    # 添加跨域头
    # response.headers.add("Access-Control-Allow-Origin", 'http://localhost:5173')
    # response.headers.add("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS")
    # response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    # response.headers.add("Access-Control-Allow-Credentials", "true")
    return response, 200


def success_json(data: Any = None):
    """成功数据响应"""
    return json(Response(code=HttpCode.SUCCESS, message="成功返回json数据", data=data))


def fail_json(data: Any = None):
    """失败数据响应"""
    return json(Response(code=HttpCode.FAIL, message="", data=data))


def validate_error_json(errors: dict = None):
    """数据验证错误响应"""
    first_key = next(iter(errors))
    if first_key is not None:
        mgs = errors.get(first_key)[0]
    else:
        mgs = "请输入正确的格式"
    return json(Response(code=HttpCode.VALIDATE_ERROR, message=mgs, data=errors))


def message(code: HttpCode = None, msg: str = ""):
    """基础的消息响应,固定返回消息提示,数据固定为空字典"""
    return json(Response(code=code, message=msg, data={}))


def success_message(msg: str = ""):
    """成功的消息响应"""
    return message(code=HttpCode.SUCCESS, msg=msg)


def fail_message(msg: str = ""):
    """失败的消息响应"""
    return message(code=HttpCode.FAIL, msg=msg)


def not_found_message(msg: str = ""):
    """未找到消息响应"""
    return message(code=HttpCode.NOT_FOUND, msg=msg)


def unauthorized_message(msg: str = ""):
    """未授权消息响应"""
    return message(code=HttpCode.UNAUTHORIZED, msg=msg)


def forbidden_message(msg: str = ""):
    """无权限消息响应"""
    return message(code=HttpCode.FORBIDDEN, msg=msg)
