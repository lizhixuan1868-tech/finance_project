"""
这个文件是整个项目的“控制面板”
以后想改数据库位置、或者改抓取数据的规则，
只需要在这里修改，不用去动那些复杂的代码。
"""
#======================================

#导包
import os

#1.获取当前项目的根目录路径
#因为settings.py在config文件夹里，要往上退一层，找到finance_project文件夹
BASE_DIR = os.path.dirname(
    os.path.dirname(
        (os.path.abspath(__file__)
         )
    )
)

#2.数据库配置
#以后的数据都存在data文件夹下的finance.db文件夹里
#sqlite:///是告诉python使用sqlite数据库
# DATABASE_URL = f'sqlite:///{os.path.join(BASE_DIR,'data','finance.db')}'
DATABASE_URL = f'sqlite:///{os.path.join(BASE_DIR, "data", "finance.db")}'

#3.数据抓取配置
#为了防止被网站封IP,这里规定每抓取数据后，必须强制休息1秒
FETCH_DELAY = 2.0

#抓取失败，最多允许重复3次
MAX_RETRIES = 5



