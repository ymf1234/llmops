import dotenv
from flask_migrate import Migrate
from injector import Injector

from config import Config
from internal.router import Router
from internal.server import Http
from pkg.sqlalchemy import SQLAlchemy
from .module import ExtexsionModule

# 将env加载到环境变量中
dotenv.load_dotenv()

# 配置文件
conf = Config()

# 初始化依赖注入器
injector = Injector([ExtexsionModule])

app = Http(
    __name__,
    conf=conf,
    db=injector.get(SQLAlchemy),
    migrate=injector.get(Migrate),
    router=injector.get(Router)
)

if __name__ == '__main__':
    app.run(debug=True)
