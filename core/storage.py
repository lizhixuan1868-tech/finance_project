# ==========================================
# 这个文件是项目的“仓库管理员”
# 它的唯一职责就是：把洗好的数据，安全地存进数据库里。
# ==========================================

#导包
from config.settings import DATABASE_URL
from sqlalchemy import create_engine
import pandas as pd

#定义类
class DataStorage:
    """
    数据存储类。
    专门负责和数据库打交道，存数据、读数据都找它。
    """

    def __init__(self):
        """
        初始化方法。
        用于创建数据库连接。
        """

        # create_engine 会创建一个数据库引擎（连接对象）
        # echo=False 表示不在控制台打印底层的 SQL 语句（保持控制台干净）
        #self.engine = create_engine(DATABASE_URL,echo=False)
        #print("数据库连接创建成功！")

        """
        初始化方法。
        用于创建腾讯云数据库连接。
        """
        # 1. 腾讯云数据库配置信息（请替换为你自己的真实信息）
        DB_USER = 'root'    # 数据库用户名
        DB_PASS = 'lzx13695250408'    # 数据库密码
        DB_HOST = 'gz-cdb-8bco4w6f.sql.tencentcdb.com'    # 数据库外网地址
        DB_PORT = 24347  # 【注意】：这是你专属的外网端口，千万别漏了
        DB_NAME = 'use01'

        # 2. 拼接数据库连接字符串（使用 pymysql 驱动）
        DATABASE_URL = f'mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4'

        # 3. 创建云端数据库引擎
        # echo=False 表示不在控制台打印底层的 SQL 语句（保持控制台干净）
        self.engine = create_engine(DATABASE_URL, echo=False)

        print("☁️ 腾讯云数据库连接创建成功！")

    def save_to_db(self,df,table_name):
        """
        智能追加数据到数据库（严谨版）。
        """
        if df is None or df.empty:
            print("😢 传入的数据为空，跳过存储。")
            return

        try:
            from sqlalchemy import inspect
            inspector = inspect(self.engine)
            table_exists = inspector.has_table(table_name)

            # 1. 如果表存在，进行增量过滤
            if table_exists and 'date' in df.columns:
                max_date_in_db = pd.read_sql(
                    f"SELECT MAX(date) as max_date FROM {table_name}",
                    self.engine
                )['max_date'].iloc[0]

                if max_date_in_db is not None:
                    max_date_in_db = pd.to_datetime(max_date_in_db)
                    # 过滤出比数据库里最新日期还要新的数据
                    df = df[df['date'] > max_date_in_db]

                    # 【核心修复点】：如果过滤后没有新数据，直接返回，绝不打印成功！
                    if df.empty:
                        print(f"⏩ 数据库表 [{table_name}] 已是最新，无需重复写入。")
                        return

                        # 2. 只有走到这里，才说明真正有新数据要写入
            df.to_sql(
                name=table_name,
                con=self.engine,
                if_exists='append',
                index=False
            )
            print(f"💾 成功追加 {len(df)} 条新数据到 [{table_name}] 表！")

        except Exception as e:
            print(f"❌ 存入数据库失败: {e}")


    #新增查询功能
    def check_if_data_exists(self, table_name, symbol, start_date, end_date):
        """
        检查本地数据库里是否已经有这段时间的数据了。
        大白话：在去网上抓之前，先问问本地仓库：“兄弟，这批货你有吗？”
        """
        try:
            # 大白话：用 pandas 从数据库里读取数据，看看有没有记录
            # 这里用了一个简单的 SQL 查询：SELECT * FROM 表名 WHERE code = ? AND date BETWEEN ? AND ?
            query = f"SELECT * FROM {table_name} WHERE code = '{symbol}' AND date BETWEEN '{start_date}' AND '{end_date}'"
            df = pd.read_sql(query, self.engine)

            # 如果查出来的行数大于 0，说明本地有数据
            return len(df) > 0
        except Exception as e:
            # 如果表还不存在，或者查询出错，说明本地肯定没数据，返回 False
            return False

    def export_to_excel(self, table_name, file_name):
        """
        把数据库里的某张表导出为 Excel 文件。

        参数说明：
        table_name: 数据库里的表名（比如 'stock_daily_factors'）
        file_name: 导出的 Excel 文件名（比如 '茅台2023年数据.xlsx'）
        """
        try:
            # 大白话：用 pandas 把整张表的数据读出来
            df = pd.read_sql(f"SELECT * FROM {table_name}", self.engine)

            # 大白话：使用 pandas 的 to_excel 方法，一键生成 Excel 文件
            # index=False 表示不把数据库的行号写进 Excel 里
            df.to_excel(file_name, index=False)

            print(f"📁 成功将 [{table_name}] 导出为 Excel 文件：{file_name}")
        except Exception as e:
            print(f"❌ 导出 Excel 失败: {e}")


    #新增查空值与异常的功能
    def basic_health_check(self,df,asset_name=''):
        """
        基本健康检查：检查数据中是否存在空值和异常值。
        :param df:  待检查的数据框
        :param asset_name: 资产名称，用于提示
        """

        #1.检查空值
        null_counts = df.isnull().sum()
        if null_counts.any():
            print(f"⚠️ 发现空值:\n{null_counts[null_counts > 0]}")
        else:
            print(f'☑️无空值')

        #2.检查价格异常（比如收盘价<=0）
        if 'close' in df.columns:
            negative_prices = df[df['close'] <= 0]
            if not negative_prices.empty:
                print(f"❌ 发现异常价格（<=0）: {len(negative_prices)} 条")
            else:
                print("✅ 价格区间正常")

        #3.检查重复日期
        duplicate_dates = df[df.duplicated(subset=['date'])]
        if not duplicate_dates.empty:
            print(f"❌ 发现重复日期: {len(duplicate_dates)} 条")
        else:
            print("✅ 日期无重复")

        #4.检查OHLC逻辑
        #最高价 >= 收盘价，最低价 <= 收盘价。如果数据源抓错了，这个逻辑就会被打破
        logic_errors = df[(df['high'] < df['close']) | (df['low'] > df['close'])]
        if not logic_errors.empty:
            print(f"❌ 发现 OHLC 逻辑错误: {len(logic_errors)} 条")
            print(logic_errors[['date', 'open', 'high', 'low', 'close']].head())
        else:
            print("✅ OHLC 逻辑正确")