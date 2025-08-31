import pytest

from app.http.app import app


@pytest.fixture
def client():
    """创建一个简单的 Flask 应用用于测试"""
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client
