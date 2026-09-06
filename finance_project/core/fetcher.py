# ==========================================
# 这个文件是项目的“数据搬运工”
# 它的唯一职责就是：安全、稳定地从网上把股票数据抓回来。
# ==========================================

#导包
from config.settings import FETCH_DELAY,MAX_RETRIES
from core.storage import DataStorage
import akshare as ak
import time
import pandas as pd

#定义一个类
class DataFetcher:
    """
    这个类是项目的“数据搬运工”
    它的唯一职责就是：安全、稳定地从网上把股票数据抓回来。
    """
    def __init__(self):
        self.storage = DataStorage()

    def fetch_stock_history(self,symbol,start_date,end_date):
        """
        这个方法用于从网上抓取股票历史数据
        :param symbol: 股票代码，比如'600519(贵州茅台)'
        :param start_date: 开始日期，比如 '20230101'
        :param end_date: 结束日期，比如 '20230101'
        """
        # ================= 第一道防线：本地缓存检查 =================
        # 大白话：去数据库看看，如果之前已经抓过这段数据了，就直接从本地读，不浪费网络请求！
        print(f"🔍 正在检查本地缓存：{symbol} ({start_date} 到 {end_date})...")
        # if self.storage.check_if_data_exists("stock_daily", symbol, start_date, end_date):
        if self.storage.check_if_data_exists("stock_daily_with_code", symbol, start_date, end_date):
            print(f"🎉 本地已有数据，直接从数据库秒读！跳过网络请求。")
            # query = f"SELECT * FROM stock_daily WHERE code = '{symbol}' AND date BETWEEN '{start_date}' AND '{end_date}'"
            query = f"SELECT * FROM stock_daily_with_code WHERE code = '{symbol}' AND date BETWEEN '{start_date}' AND '{end_date}'"
            return pd.read_sql(query, self.storage.engine)

        # ================= 第二道防线：指数退避抓取 =================
        # 大白话：如果本地没有，才去网上抓。如果失败了，等待时间会翻倍！
        print(f"🌐 本地无数据，准备从网络获取...")
        #用for循环来实现“失败重试机制”
        #range(MAX_RETRIES) 会生成 0, 1, 2（如果 MAX_RETRIES 是 3）
        for attempt in range(MAX_RETRIES):
            try:
                # 调用 akshare 的接口获取 A 股历史行情
                # adjust="qfq" 表示“前复权”（这是金融常识，消除分红送股带来的价格断层）

                print(f'🚀正在获取{symbol}的历史数据...')
                df = ak.stock_zh_a_hist(
                    symbol=symbol,
                    period="daily",
                    start_date=start_date,
                    end_date=end_date,
                    adjust="qfq"
                )

                #如果成功拿到了数据，打印成功信息并返回数据
                print(f'🚀成功获取{symbol}的历史数据,共{len(df)}条')
                return df

            except Exception as e:
                #如果失败了，打印错误信息并等待一段时间后重试
                print(f'🚀获取{symbol}的历史数据失败，第{attempt+1}次，错误信息：{e}')

                #等待一段时间后重试，如果不行就直接放弃，返回空
                if attempt < MAX_RETRIES -1:
                    wait_time = FETCH_DELAY * (2 ** attempt)
                    #等待一段时间后重试
                    print(f'🚀等待{wait_time}秒后重试...')
                    time.sleep(wait_time)

        #如果重试了 MAX_RETRIES 次还是失败，返回 None
        print(f'⚠️ 获取{symbol}的历史数据失败，已达到最大重试次数')
        return None

