# # ==========================================
# # 这是整个项目的“总指挥”（启动入口）
# # 以后你每次想运行项目，只需要运行这一个文件。
# # ==========================================
#
# #导包
# import pandas as pd
# import akshare as ak
# import openpyxl
# from config.settings import DATABASE_URL,FETCH_DELAY,MAX_RETRIES
# from core.fetcher import DataFetcher
# from core.cleaner import DataCleaner
# from core.storage import DataStorage
# from factors.engine import FactorEngine
# from core.baostock_fetcher import BaoStockFetcher
# from core.gold_fetcher import GoldFetcher
#
# def try_fetcher():
#     try:
#         df = ak.spot_gold()
#         print("✅ 接口通了！最新数据：")
#         print(df.head())
#     except Exception as e:
#         print(f"❌ 接口挂了：{e}")
#
# def main():
#     """
#     这是项目的总指挥（启动入口）
#     """
#     print('🚀欢迎使用A股量化数据中台！')
#     print('-'*30)
#
#     #打印配置信息
#     print(f'📦数据库将保存在：{DATABASE_URL}')
#     print(f'⏰每次抓取数据后休息：{FETCH_DELAY}秒')
#     print(f'🔁抓取失败最多重试：{MAX_RETRIES}次')
#     print('-'*30)
#     print('☑️配置文件读取成功，项目骨架已就绪！')
#
#     #TODO: 以后我们会在这里写上抓取数据、计算因子的代码
#
# def main_fetcher():
#     print("🚀 开始测试数据抓取模块...")
#
#     # 1. 创建一个搬运工对象
#     fetcher = DataFetcher()
#
#     # 2. 让他去抓“贵州茅台”在 2023 年的数据
#     # 600519 是贵州茅台的代码
#     stock_data = fetcher.fetch_stock_history("600519", "20230101", "20231231")
#
#     # 3. 如果抓到了数据，打印最后 5 行看看
#     if stock_data is not None:
#         print("\n📊 数据预览（最后5行）：")
#         print(stock_data.tail())
#     else:
#         print("\n😢 没抓到数据，请检查网络或稍后再试。")
#
# def main_fetcher_cleaner():
#     print("🚀 开始测试 ETL（提取-转换）流水线...\n")
#
#     # 1. 第一步：去网上抓数据（生肉）
#     fetcher = DataFetcher()
#     raw_data = fetcher.fetch_stock_history("600519", "20230101", "20231231")
#
#     # 2. 第二步：把抓回来的数据洗干净（净菜）
#     if raw_data is not None:
#         cleaner = DataCleaner()
#         clean_data = cleaner.clean_stock_data(raw_data)
#
#         # 3. 看看洗完之后的数据长啥样
#         print("\n📊 清洗后的数据预览（前5行）：")
#         print(clean_data.head())
#         print("\n📋 数据基本信息：")
#         print(clean_data.dtypes)  # 打印每一列的数据类型，看看 date 是不是变成了 datetime
#     else:
#         print("\n😢 第一步抓取数据就失败了，流水线停止。")
#
# def main_fetcher_cleaner_storage():
#     print("🚀 开始测试完整的 ETL 流水线...\n")
#
#     # 1. 第一步：去网上抓数据（生肉）
#     fetcher = DataFetcher()
#     raw_data = fetcher.fetch_stock_history("600519", "20230101", "20231231")
#
#     # 2. 第二步：把抓回来的数据洗干净（净菜）
#     if raw_data is not None:
#         cleaner = DataCleaner()
#         clean_data = cleaner.clean_stock_data(raw_data)
#
#         # 3. 第三步：把洗好的数据存进数据库（入库）
#         storage = DataStorage()
#         storage.save_to_db(clean_data, "stock_daily")
#
#         print("\n🎉 恭喜！完整的 ETL 流水线测试成功！")
#         print(f"📂 数据库文件已保存在: data/finance.db")
#     else:
#         print("\n😢 抓取数据失败，流水线停止。")
#
# def main_factor_engine():
#     print("🚀 开始测试完整的量化数据流水线...\n")
#
#     # 1. 第一步：去网上抓数据（生肉）
#     fetcher = DataFetcher()
#     raw_data = fetcher.fetch_stock_history("600519", "20240101", "20240231")
#
#     # 2. 第二步：把抓回来的数据洗干净（净菜）
#     if raw_data is not None:
#         cleaner = DataCleaner()
#         clean_data = cleaner.clean_stock_data(raw_data)
#
#         # 3. 第三步：把洗好的数据存进数据库（入库）
#         storage = DataStorage()
#         storage.save_to_db(clean_data, "stock_daily")
#
#         # 4. 第四步：计算金融因子（加工成高价值商品）
#         engine = FactorEngine()
#         final_data = engine.add_moving_averages(clean_data)
#         final_data = engine.add_rsi(final_data)
#
#         # 5. 看看加了指标后的数据长啥样
#         print("\n📊 最终数据预览（最后5行）：")
#         print(final_data[['date', 'close', 'MA_5', 'MA_20', 'RSI']].tail())
#
#         print("\n🎉 恭喜！完整的量化数据流水线测试成功！")
#     else:
#         print("\n😢 抓取数据失败，流水线停止。")
#
# def main_baostock_fetcher():
#     print("🚀 开始测试 BaoStock 量化数据流水线...\n")
#
#     # 1. 第一步：使用 BaoStock 抓数据（生肉）
#     fetcher = BaoStockFetcher()
#     raw_data = fetcher.fetch_stock_history("000001", "20260101", "20260531")
#
#     # 2. 第二步：把抓回来的数据洗干净（净菜）
#     if raw_data is not None and not raw_data.empty:
#         cleaner = DataCleaner()
#         clean_data = cleaner.clean_stock_data(raw_data)
#
#         # 3. 第三步：把洗好的数据存进数据库（入库）
#         storage = DataStorage()
#         storage.save_to_db(clean_data, "stock_daily_with_code")
#
#         # 4. 第四步：计算金融因子（加工成高价值商品）
#         engine = FactorEngine()
#         final_data = engine.add_moving_averages(clean_data)
#         final_data = engine.add_rsi(final_data)
#
#         # ================= 新增：把算好指标的数据单独存进新表 =================
#         # 大白话：原始数据存在 stock_daily_with_code 里，
#         # 算好指标的数据，我们给它个新名字，存进 stock_daily_factors 表里！
#         storage.save_to_db(final_data, "stock_daily_factors")
#         print("📊 带有指标的宽表数据已成功写入 stock_daily_factors 表！")
#         #
#
#         # 5. 看看加了指标后的数据长啥样
#         print("\n📊 最终数据预览（最后5行）：")
#         print(final_data[['date', 'close', 'MA_5', 'MA_20', 'RSI']].tail())
#         print("\n💾 正在导出 Excel...")
#         storage.export_to_excel("stock_daily_factors", "贵州茅台_2023年_带指标.xlsx")
#
#         print("\n🎉 恭喜！BaoStock 量化数据流水线测试成功！")
#     else:
#         print("\n😢 抓取数据失败，流水线停止。")
#
# def main_gold_fetcher():
#     print("🚀 开始测试【黄金】量化数据流水线...\n")
#
#     # 1. 第一步：去网上抓黄金数据（生肉）
#     fetcher = GoldFetcher()
#     raw_data = fetcher.fetch_gold_history("Au99.99", "20250101", "20251231")
#
#     # 2. 第二步：把抓回来的黄金数据洗干净（净菜）
#     if raw_data is not None:
#         cleaner = DataCleaner()
#         clean_data = cleaner.clean_gold_data(raw_data)  # 注意：这里用的是 clean_gold_data
#
#         # 3. 第三步：把洗好的数据存进数据库（入库）
#         storage = DataStorage()
#         storage.save_to_db(clean_data, "gold_daily")  # 存进 gold_daily 表
#
#         # 4. 第四步：计算金融因子（黄金也可以算均线和RSI！）
#         engine = FactorEngine()
#         final_data = engine.add_moving_averages(clean_data)
#         final_data = engine.add_rsi(final_data)
#
#         # 5. 看看加了指标后的黄金数据长啥样
#         print("\n📊 黄金最终数据预览（最后5行）：")
#         print(final_data[['date', 'close', 'MA_5', 'MA_20', 'RSI']].tail())
#
#         # 6. 导出 Excel 看看
#         storage.export_to_excel("gold_daily", "黄金_2023年_带指标.xlsx")
#
#         print("\n🎉 恭喜！黄金量化数据流水线测试成功！")
#     else:
#         print("\n😢 抓取黄金数据失败，流水线停止。")
# #
#
# if __name__ == '__main__':
#     # main()
#     # main_fetcher()
#     # main_fetcher_cleaner()
#     # main_fetcher_cleaner_storage()
#     #  main_factor_engine()
#     # main_baostock_fetcher()
#     main_gold_fetcher()
from typing import final

# ==========================================
# 【总指挥】使用数据工厂
# ==========================================
from core.data_factory import DataFactory
from core.storage import DataStorage
from apscheduler.schedulers.blocking import BlockingScheduler
import logging
from datetime import datetime

def main(target_date=None):
    """
    总指挥：支持传入指定日期，如果不传则默认抓取今天的数据
    :param target_date:字符串格式，如 '20260902'。默认为 None（代表今天）
    """
    # 【核心逻辑】：如果没有传入日期，就自动获取今天的日期
    if target_date is None:
        target_date = datetime.now().strftime('%Y%m%d')

    print('🚀 欢迎使用 A股量化数据中台（工厂模式）！')
    print(f'📅 正在抓取日期：{target_date}')

    # 创建工厂
    factory = DataFactory()

    # ==========================================
    # 🎯 你只需要在这里“点菜”就行了！
    # ==========================================

    #点菜1：要贵州茅台的股票数据
    factory.process(
        asset_type='stock',
        symbol='600519',
        start_date=target_date,
        end_date=target_date
    )

    #点菜2：要黄金数据
    factory.process(
        asset_type='gold',
        symbol='XAU',
        start_date='20250801',
        end_date='20260823',
        market_type='intl'
    )

    #点菜3：要螺纹钢主力合约的数据
    factory.process(
        asset_type='futures',
        symbol='rb0',         # rb0 代表螺纹钢主力
        start_date=target_date,
        end_date=target_date
    )

    # 点菜4：要原油数据
    factory.process(
        asset_type='crude',
        symbol='CL',
        start_date=target_date,
        end_date=target_date
    )

    # 以后想加平安银行？只需要加一行：
    # factory.process('stock', '000001', '20230101', '20231231')

    # 以后想加白银？只需要在工厂里加一个 elif，然后在这里加一行：
    # factory.process('silver', 'AG9999', '20230101', '20231231')
    #
    # if final_date is not None and not final_date.empty:
    #     storage = DataStorage()
    #     # 大白话：把带有均线和 RSI 的宽表数据，保存为 Excel 文件
    #     storage.export_to_excel("lundon_daily_factors", "伦敦金数据指标.xlsx")
    #     print("📁 数据已成功导出为 Excel！")
    # else:
    #     print("😢 没有拿到最终数据，跳过 Excel 导出。")


if __name__ == '__main__':
     main()
