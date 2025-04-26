from injector import Injector

from config import Config
from internal.router import Router
from internal.server import Http
import dotenv

# 将env加载到环境变量中
dotenv.load_dotenv()

# 配置文件
conf = Config()

# 初始化依赖注入器
injector = Injector()

app = Http(__name__, conf=conf, router=injector.get(Router))

if __name__ == '__main__':
    app.run(debug=True)
