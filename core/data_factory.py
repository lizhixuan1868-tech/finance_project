# ==========================================
# 【数据工厂】DataFactory
# 大白话：一个全自动化的中央厨房。
# 你只需要告诉它“我要什么资产”和“什么时间段”，
# 它会自动帮你完成：抓取 -> 清洗 -> 入库 -> 算指标。
# ==========================================

from core.baostock_fetcher import BaoStockFetcher
from core.gold_fetcher import GoldFetcher
from core.cleaner import DataCleaner
from core.storage import DataStorage
from factors.engine import FactorEngine
from core.futures_fetcher import FuturesFetcher
from core.crude_fetcher import CrudeFetcher

class DataFactory:
    """
    数据工厂类。
    大白话：根据传入的资产类型，自动组装对应的流水线。
    """

    def __init__(self):
        self.storage = DataStorage()
        self.cleaner = DataCleaner()
        self.engine = FactorEngine()

    def process(self, asset_type, symbol, start_date, end_date,market_type='sge'):
        """
        工厂的核心方法：一键处理数据流水线。

        参数说明：
        asset_type: 资产类型 ('stock' 或 'gold')
        symbol: 资产代码 (如 '600519' 或 'Au99.99')
        start_date: 开始日期 (如 '20230101')
        end_date: 结束日期 (如 '20231231')
        """
        print(f"\n{'=' * 40}")
        print(f"🏭 工厂开始处理: {asset_type} - {symbol}")
        print(f"{'=' * 40}")
        #===============股票数据调用===============
        # 1. 自动选择对应的“搬运工”
        if asset_type == 'stock':
            fetcher = BaoStockFetcher()
            raw_data = fetcher.fetch_stock_history(symbol, start_date, end_date)
            clean_method = self.cleaner.clean_stock_data
            table_name = "stock_daily_with_code"
        #===============黄金数据调用===============
        elif asset_type == 'gold':
            fetcher = GoldFetcher()
            # 把市场类型传给 Fetcher，让它知道去抓哪个市场的数据
            raw_data = fetcher.fetch_gold_history(symbol, start_date, end_date, market_type=market_type)

            # 【核心逻辑】：根据市场类型决定清洗方法和存哪张表
            if market_type == 'intl':
                clean_method = self.cleaner.clean_london_gold_data
                table_name = "london_gold_daily"
            else:
                clean_method = self.cleaner.clean_gold_data
                table_name = "gold_daily"
        #===============期货数据调用===============
        elif asset_type == 'futures':
            fetcher = FuturesFetcher()
            raw_data = fetcher.fetch_futures_history(symbol, start_date, end_date)
            clean_method = self.cleaner.clean_futures_data
            table_name = "futures_daily"

        # ===============原油数据调用===============
        elif asset_type == 'crude':
            fetcher = CrudeFetcher()
            raw_data = fetcher.fetch_crude_history(symbol, start_date, end_date)
            clean_method = self.cleaner.clean_crude_data
            table_name = "crude_daily"

        # # ===============伦敦金数据调用===============
        # elif asset_type == 'gold':
        #     fetcher = GoldFetcher()
        #     raw_data = fetcher.fetch_gold_history(symbol, start_date, end_date, market_type=market_type)
        #     clean_method = self.cleaner.clean_london_gold_data
        #     # 如果是伦敦金，存到单独的表里
        #     table_name = "london_gold_daily" if market_type == 'intl' else "gold_daily"

        else:
            print(f"❌ 不支持的资产类型: {asset_type}")
            return None

        # 2. 如果抓取失败，直接返回
        if raw_data is None or raw_data.empty:
            print("😢 抓取数据失败，流水线停止。")
            return None

        # 3. 自动清洗
        clean_data = clean_method(raw_data)

        # 4. 存入数据库
        self.storage.save_to_db(clean_data, table_name)

        # 5. 计算因子
        final_data = self.engine.add_moving_averages(clean_data)
        final_data = self.engine.add_rsi(final_data)

        # 6. 把带指标的宽表也存起来
        factors_table = f"{table_name}_factors"
        self.storage.save_to_db(final_data, factors_table)

        print(f"🎉 工厂处理完成！数据已存入 [{table_name}] 和 [{factors_table}]")
        return final_data