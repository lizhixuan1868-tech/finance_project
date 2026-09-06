# core/london_gold_fetcher.py
import akshare as ak
import pandas as pd


class LondonGoldFetcher:
    """
    伦敦金/现货黄金 专属数据抓取器 (基于 AKShare)
    """

    def __init__(self):
        pass

    def fetch_5min_data(self):
        """
        获取现货黄金 5 分钟级别的 K 线数据。
        """
        print("🌍 正在从 AKShare 获取现货黄金数据...")
        try:
            # 获取现货黄金历史数据（Au99.99 走势与 XAUUSD 高度一致）
            # 这个接口不需要传日期，直接返回近期数据
            df = ak.spot_hist_sge(symbol='Au99.99')

            if df is None or df.empty:
                print("⚠️ spot_hist_sge 返回空数据。")
                return None

            # 打印原始数据检查
            print("=== 原始数据检查 ===")
            print(df.head())
            print(f"列名: {df.columns.tolist()}")
            print("==================")

            # 统一列名
            column_map = {
                "时间": "date", "日期": "date",
                "开盘": "open", "开盘价": "open",
                "最高": "high", "最高价": "high",
                "最低": "low", "最低价": "low",
                "收盘": "close", "收盘价": "close",
                "成交量": "volume"
            }
            df = df.rename(columns=column_map)

            # 确保时间格式正确
            df['date'] = pd.to_datetime(df['date'])

            # 动态保留核心列
            required_cols = ['date', 'open', 'high', 'low', 'close']
            optional_cols = ['volume']

            if not all(col in df.columns for col in required_cols):
                print(f"❌ 抓取到的数据缺少核心列，当前列名为: {df.columns.tolist()}")
                return None

            final_cols = required_cols + [col for col in optional_cols if col in df.columns]
            df = df[final_cols]

            # 强制转为浮点数并保留两位小数
            price_cols = ['open', 'high', 'low', 'close']
            for col in price_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce').astype(float).round(2)

            return df

        except Exception as e:
            print(f"❌ AKShare 抓取失败: {e}")
            return None