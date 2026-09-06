# ==========================================
# 这个文件是项目的“数据清洗工”
# 它的唯一职责就是：把抓回来的“生肉”（原始数据），
# 加工成可以直接下锅的“净菜”（标准化数据）。
# ==========================================

#导包
import pandas as pd

#定义一个类
class DataCleaner:
    """
    数据清洗类。
    专门负责把乱七八糟的数据变得整整齐齐。
    """

    # ======================== 内部通用质检方法 =========================
    @staticmethod
    def _quality_check(df, asset_name=""):
        """
        内部通用方法：执行数据质检三板斧。
        所有清洗方法在格式化完成后，都会调用这个方法。
        """
        # 1. 删除包含空值的行
        initial_rows = len(df)
        df = df.dropna()
        dropped_rows = initial_rows - len(df)
        if dropped_rows > 0:
            print(f"🗑️ [{asset_name}] 发现并删除了 {dropped_rows} 条空值数据。")

        # 2. 删除重复日期
        df = df.drop_duplicates(subset=['date']).reset_index(drop=True)

        # 3. 检查 OHLC 逻辑（最高价 >= 收盘价，最低价 <= 收盘价）
        logic_errors = df[(df['high'] < df['close']) | (df['low'] > df['close'])]
        if not logic_errors.empty:
            print(f"⚠️ [{asset_name}] 发现 {len(logic_errors)} 条 OHLC 逻辑错误，已自动剔除。")
            df = df.drop(logic_errors.index).reset_index(drop=True)

        return df

#========================获取股票数据的方法=========================
    @staticmethod
    def clean_stock_data(df):
        """
        清洗股票数据。
        :param df: 从akshare获取的原始数据
        """

        #先判断一下，如果传入的数据是空的，就直接返回
        if df is None or df.empty:
            return None

        # 1. 统一列名（把中文列名改成英文，方便后续写代码和存数据库）
        # 建立一个“中英文对照字典”，然后用 rename 方法批量改名
        column_map = {
            '日期': 'date',
            '开盘': 'open',
            '收盘': 'close',
            '最高': 'high',
            '最低': 'low',
            '成交量': 'volume',
            '成交额': 'amount',
            '振幅': 'amplitude',
            '涨跌幅': 'pct_change',
            '涨跌额': 'change',
            '换手率': 'turnover'
        }
        df = df.rename(columns=column_map)

        # 2. 转换日期格式
        # 把 'date' 这一列从普通的“字符串”变成真正的“日期时间对象”
        # 这样以后我们就能按天、按月来筛选数据了
        df['date'] = pd.to_datetime(df['date'])

        #3.把日期排序
        df = df.sort_values(by='date').reset_index(drop=True)
        # 4. 质量检查
        df = DataCleaner._quality_check(df, asset_name="股票")
        print('📊数据清洗完成！')
        return df

#========================获取黄金数据的方法=========================
    @staticmethod
    def clean_gold_data(df):
        """
        清洗黄金历史数据。
        """
        if df is None or df.empty:
            return None

        # 大白话：黄金数据的列名映射（根据 akshare 返回的实际列名来定）
        column_map = {
            '交易日期': 'date',
            '开盘价': 'open',
            '收盘价': 'close',
            '最高价': 'high',
            '最低价': 'low',
            '成交量': 'volume',
            '成交额': 'amount'
        }
        df = df.rename(columns=column_map)

        # 转换日期格式并排序
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values(by='date').reset_index(drop=True)
        # 4. 质量检查
        df = DataCleaner._quality_check(df, asset_name="黄金")
        print("🧼 黄金数据清洗完成！")
        return df

#========================获取期货数据的方法=========================
    @staticmethod
    def clean_futures_data(df):
        """
        清洗期货历史数据（带诊断功能）。
        """
        if df is None or df.empty:
            return None

        # 【诊断代码】：打印出原始列名，看看 AkShare 到底返回了什么
        print(f"🔍 期货原始列名: {df.columns.tolist()}")

        # 大白话：尝试进行列名映射（如果列名不匹配，就不会报错，只是跳过）
        column_map = {
            '日期': 'date',
            '开盘价': 'open',
            '最高价': 'high',
            '最低价': 'low',
            '收盘价': 'close',
            '成交量': 'volume',
            '持仓量': 'open_interest'
        }

        # 只映射存在的列
        existing_map = {k: v for k, v in column_map.items() if k in df.columns}
        df = df.rename(columns=existing_map)

        # 【诊断代码】：打印出映射后的列名
        print(f"🔍 映射后的列名: {df.columns.tolist()}")

        # 确保日期是 datetime 类型，且按时间正序排列
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values(by='date').reset_index(drop=True)
        # 4. 质量检查
        df = DataCleaner._quality_check(df, asset_name="期货")

        print("🧼 期货数据清洗完成！\n")
        return df

#========================获取原油数据的方法=========================
    @staticmethod
    def clean_crude_data(df):
        """
        清洗原油数据。
        :param df: 从akshare获取的原始数据
        :return: 清洗后的数据
        """
        if df is None or df.empty:
            return None

        #【诊断代码】:打印原始列名，看看AkShare到底返回了什么
        print(f'🔍原油原始列名：{df.columns.tolist()}')

        column_map = {
            '日期': 'date',
            '开盘': 'open',
            '收盘': 'close',
            '最高': 'high',
            '最低': 'low',
            '成交量': 'volume',
            '持仓量': 'open_interest'
        }

        df = df.rename(columns=column_map)

        #转换日期
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values(by='date').reset_index(drop=True)
        # 4. 质量检查
        df = DataCleaner._quality_check(df, asset_name="原油")
        print('🧼原油数据清洗完成！')
        return df

#========================获取伦敦金的方法=========================
    @staticmethod
    def clean_london_gold_data(df):
        """
        清洗伦敦金（XAUUSD）数据。
        大白话：处理国际黄金的英文列名、时区以及周末缺口。
        """
        if df is None or df.empty:
            return None

        # 【诊断代码】：打印原始列名，看看 AkShare 返回了什么
        print(f'🔍 伦敦金原始列名：{df.columns.tolist()}')

        # 1. 统一列名（兼容中英文数据源）
        column_map = {
            '交易日期': 'date',
            '日期': 'date',
            '开盘价': 'open',
            '开盘': 'open',
            '最高价': 'high',
            '最高': 'high',
            '最低价': 'low',
            '最低': 'low',
            '收盘价': 'close',
            '收盘': 'close',
            '成交量': 'volume',
            '成交额': 'amount'
        }
        # 只映射存在的列，防止报错
        existing_map = {k: v for k, v in column_map.items() if k in df.columns}
        df = df.rename(columns=existing_map)

        # 2. 转换日期格式并排序
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values(by='date').reset_index(drop=True)

        # 3. 伦敦金特殊处理：周末无数据缺口
        # 伦敦金周末休市，如果直接算均线会导致数据断层。
        # 这里我们用前一个有效价格（ffill）填充周末的空缺，保证时间序列连续。
        price_cols = ['open', 'high', 'low', 'close']
        for col in price_cols:
            if col in df.columns:
                df[col] = df[col].ffill()
        if 'volume' in df.columns:
            df['volume'] = df['volume'].fillna(0)

        # 4. 质量检查（复用你的通用质检方法）
        df = DataCleaner._quality_check(df, asset_name="伦敦金")
        print('🧼 伦敦金数据清洗完成！')
        return df

