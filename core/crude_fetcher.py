# ==========================================
# 【黄金数据搬运工】AkShare 最新稳定版
# 特点：使用官方最新接口，专门拉取原油交易数据
# ==========================================

#导包
import pandas as pd
import akshare as ak
import time
from config.settings import FETCH_DELAY, MAX_RETRIES

#原油交易数据抓取类
class CrudeFetcher:
    """
    原油交易数据抓取类
    """
    def fetch_crude_history(self, symbol="CL", start_date="2020-01-01", end_date="2020-01-02"):
        """
        抓取原油交易数据
        :param symbol: 原油合约代码
        :param start_date: 开始日期
        :param end_date: 结束日期
        :return: 原油交易数据
        """
        for attempt in range(MAX_RETRIES):
            try:
                print(f'🚀正在获取{symbol}的原油交易数据....')
                df = ak.futures_foreign_hist(symbol=symbol)

                df['date'] = pd.to_datetime(df['date'])
                start_date_fmt = pd.to_datetime(start_date)
                end_date_fmt = pd.to_datetime(end_date)
                df = df[(df['date'] >= start_date_fmt) & (df['date'] <= end_date_fmt)]

                df = df.reset_index(drop=True)

                print(f'🚀获取{symbol}的原油交易数据成功,共{len(df)}行数据')
                return df

            except Exception as e:
                print(f'🚀获取{symbol}的原油交易数据失败，正在重试...({attempt+1}/{MAX_RETRIES})')
                if attempt < MAX_RETRIES -1:
                    wait_time = FETCH_DELAY * (2 ** attempt)
                    print(f'💤 触发指数退避，休息 {wait_time} 秒后重试...')
                    time.sleep(wait_time)

        print(f'⚠️ 获取{symbol}的原油交易数据失败，已达到最大重试次数')
        return None
