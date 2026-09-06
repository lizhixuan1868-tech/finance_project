# ==========================================
# 【期货数据搬运工】AkShare 版
# 特点：专门拉取国内期货的主力连续合约日线数据
# ==========================================

#导包
import pandas as pd
import time
import akshare as ak
from config.settings import FETCH_DELAY,MAX_RETRIES

#创建类
class FuturesFetcher():
    """
    期货数据抓取类。
    大白话：专门负责去网上抓期货价格的老实人。
    """

    def fetch_futures_history(self, symbol='', start_date='20230101', end_date='20231231'):
        """
        安全地获取期货主力连续历史日线数据。
        参数说明：
        symbol: 期货主力合约代码，例如 'rb0' (螺纹钢主力), 'au0' (沪金主力)
        """
        for attempt in range(MAX_RETRIES):
            try:
                print(f'🚀正在尝试获取{symbol}期货数据，第{attempt+1}次尝试')
                df = ak.futures_main_sina(symbol=symbol)
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
                start_date_fmt = pd.to_datetime(start_date)
                end_date_fmt = pd.to_datetime(end_date)
                df = df[(df['date'] >= start_date_fmt) & (df['date'] <= end_date_fmt)]

                #重置索引
                df = df.reset_index(drop=True)

                print(f'🚀成功获取{symbol}期货数据,一共{len(df)}行记录\n')
                return df

            except Exception as e:
                print(f'🚀获取{symbol}期货数据失败，第{attempt+1}次尝试\n')
                print(e)
                if attempt < MAX_RETRIES - 1:
                    wait_time = FETCH_DELAY * (2 ** attempt)
                    print(f"💤 触发指数退避，休息 {wait_time} 秒后重试...")
                    time.sleep(wait_time)

        print(f'🚀所有尝试失败，放弃获取{symbol}期货数据\n')
        return None
