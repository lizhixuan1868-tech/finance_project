"""


"""

# test_london_gold.py
import pandas as pd
from core.london_gold_fetcher import LondonGoldFetcher
from core.cleaner import DataCleaner
from datetime import datetime, timedelta


def validate_data():
    print("🔍 正在启动伦敦金数据准确性校验...\n")

    fetcher = LondonGoldFetcher(symbol="GC=F")
    cleaner = DataCleaner()

    # 1. 获取最近5天的5分钟K线数据
    # Yahoo Finance 的 days=5 通常能覆盖完整的本周交易日
    print(f"📅 正在请求过去 5 天的 5分钟 K线数据...")
    raw_df = fetcher.fetch_5min_data(days=5)

    if raw_df is None or raw_df.empty:
        print("❌ 抓取失败或无数据，请检查网络或稍后重试（Yahoo可能有频率限制）。")
        return

    print(f"✅ 原始数据获取成功，共 {len(raw_df)} 条记录。\n")

    # 2. 打印原始数据的前3条和后3条（查看首尾时间是否对齐）
    print("--- 原始数据前3条 (Head) ---")
    print(raw_df.head(3).to_string())
    print("\n--- 原始数据后3条 (Tail) ---")
    print(raw_df.tail(3).to_string())

    # 3. 执行清洗逻辑
    print("\n🧼 正在执行数据清洗...")
    clean_df = cleaner.clean_london_gold_data(raw_df)

    # 4. 核心校验逻辑
    print("\n--- 📊 数据质量报告 ---")
    print(f"清洗后剩余条数: {len(clean_df)}")

    # 检查是否有空值
    null_counts = clean_df.isnull().sum().sum()
    print(f"缺失值总数: {null_counts}")

    # 检查是否有0值（异常数据）
    zero_counts = (clean_df[['open', 'high', 'low', 'close']] == 0).sum().sum()
    print(f"价格为0的异常单元格数: {zero_counts}")

    # 检查价格逻辑 (High >= Low)
    logic_error = (clean_df['high'] < clean_df['low']).sum()
    print(f"最高价<最低价的逻辑错误数: {logic_error}")

    # 5. 打印清洗后的样本供人工核对
    print("\n--- ✅ 清洗后数据预览 (随机5条) ---")
    print(clean_df.sample(5).to_string())

    print("\n💡 提示：请核对上述打印出的价格是否在合理区间（如 2500-2600 美元）。")


if __name__ == '__main__':
    validate_data()