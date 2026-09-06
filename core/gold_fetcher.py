# ==========================================
# 【黄金数据搬运工】AkShare 最新稳定版
# 特点：使用官方最新接口，专门拉取上海黄金交易所数据
# ==========================================
import pandas as pd
import akshare as ak
import time
from config.settings import FETCH_DELAY, MAX_RETRIES


class GoldFetcher:
    """
    黄金数据抓取类。
    支持上海金（Au99.99）和伦敦金（XAU）。
    """

    def fetch_gold_history(self, symbol="Au99.99", start_date="20230101", end_date="20231231", market_type="sge"):
        """
        安全地获取黄金历史数据。

        参数说明：
        symbol: 黄金品种代码 (上海金: 'Au99.99', 伦敦金: 'XAU')
        start_date: 开始日期，格式 'YYYYMMDD'
        end_date: 结束日期，格式 'YYYYMMDD'
        market_type: 市场类型 ('sge' 代表上海黄金交易所, 'intl' 代表国际现货伦敦金)
        """
        for attempt in range(MAX_RETRIES):
            try:
                print(f"🚀 正在获取 {symbol} ({market_type}) 的历史数据...")

                # 1. 根据市场类型调用不同的 AkShare 接口
                if market_type == "intl":
                    # 伦敦金（现货黄金）历史数据
                    # 注意：AkShare 中伦敦金通常使用 'XAU' 作为代码
                    df = ak.spot_hist_sge(symbol="XAU")
                else:
                    # 上海金（默认）
                    df = ak.spot_hist_sge(symbol=symbol)

                # 2. 统一处理日期格式
                df['date'] = pd.to_datetime(df['date'])
                start_date_fmt = pd.to_datetime(start_date)
                end_date_fmt = pd.to_datetime(end_date)

                # 3. 按日期范围筛选（包含起止日期当天的所有数据）
                df = df[(df['date'] >= start_date_fmt) & (df['date'] <= end_date_fmt)]

                # 重置索引，让行号从 0 开始
                df = df.reset_index(drop=True)

                print(f"✅ 成功获取 {symbol} 的数据，共 {len(df)} 条记录！")
                return df

            except Exception as e:
                print(f"❌ 获取 {symbol} 失败 (第 {attempt + 1} 次尝试): {e}")
                if attempt < MAX_RETRIES - 1:
                    wait_time = FETCH_DELAY * (2 ** attempt)
                    print(f"💤 触发指数退避，休息 {wait_time} 秒后重试...")
                    time.sleep(wait_time)

        print(f"⚠️ 放弃获取 {symbol}，已达到最大重试次数！")
        return None