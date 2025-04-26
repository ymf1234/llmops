from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class CompletionRequest(FlaskForm):
    """基础聊天接口请求验证"""

    # 1. 定义字段
    query = StringField("query", validators=[
        DataRequired(message="用户的提问必填"),
        Length(max=2000, message="用户的提问最大长度是2000"),
    ])
