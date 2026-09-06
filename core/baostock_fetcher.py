# ==========================================
# 【备用数据搬运工】BaoStock 官方标准版
# 特点：极其稳定，没有反爬机制，随便拉数据！
# ==========================================

import baostock as bs
import pandas as pd


class BaoStockFetcher:
    """
    BaoStock 数据抓取类。
    大白话：一个永远不嫌烦、不会封你 IP 的老实人搬运工。
    """

    def __init__(self):
        # 大白话：BaoStock 需要“登录”才能用，但它不需要账号密码，
        # 只是告诉服务器“我要开始干活了”。
        print("🔑 正在连接 BaoStock 服务器...")
        lg = bs.login()
        # 大白话：检查登录是否成功
        if lg.error_code != '0':
            print(f"❌ BaoStock 登录失败: {lg.error_msg}")
        else:
            print("✅ BaoStock 连接成功！")

    def fetch_stock_history(self, symbol, start_date, end_date):
        """
        从 BaoStock 获取股票历史日线数据。
        """
        # 大白话：BaoStock 的股票代码格式比较特殊，需要加上前缀。
        # 比如 600519 要变成 sh.600519，000001 要变成 sz.000001
        if symbol.startswith('6'):
            bs_symbol = f"sh.{symbol}"
        else:
            bs_symbol = f"sz.{symbol}"

        # 大白话：BaoStock 的日期格式要求是 YYYY-MM-DD，我们要转换一下
        start_date = f"{start_date[:4]}-{start_date[4:6]}-{start_date[6:]}"
        end_date = f"{end_date[:4]}-{end_date[4:6]}-{end_date[6:]}"

        print(f"🚀 正在通过 BaoStock 获取 {bs_symbol} 的历史数据...")

        # 大白话：调用 BaoStock 的接口，获取日线数据（前复权）
        # 这是官方标准写法，把需要的字段明确传进去
        rs = bs.query_history_k_data_plus(
            bs_symbol,
            "date,code,open,high,low,close,volume,amount",
            start_date=start_date,
            end_date=end_date,
            frequency="d",
            adjustflag="2"  # 2 表示前复权
        )

        # 大白话：检查接口是否报错
        if rs.error_code != '0':
            print(f"❌ BaoStock 查询报错: {rs.error_msg}")
            return pd.DataFrame()

        # 大白话：把返回的数据转换成 Pandas 表格（官方标准循环写法）
        data_list = []
        while (rs.error_code == '0') & rs.next():
            data_list.append(rs.get_row_data())

        # 如果没查到数据，data_list 就是空的
        if not data_list:
            print(f"⚠️ BaoStock 未获取到 {bs_symbol} 的数据（可能非交易时段或代码错误）。")
            return pd.DataFrame()

        df = pd.DataFrame(data_list, columns=rs.fields)

        # 大白话：BaoStock 返回的数据全是字符串，我们要转成数字
        # 否则后面没法算均线！
        numeric_cols = ['open', 'high', 'low', 'close', 'volume', 'amount']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        if not df.empty:
            print(f"✅ BaoStock 成功获取 {bs_symbol} 的数据，共 {len(df)} 条记录！")

        return df