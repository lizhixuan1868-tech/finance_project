# london_gold_monitor.py
# ==========================================
# 【伦敦金实时监控模块】
# 职责：每5分钟获取一次伦敦金最新价格，并自动存入专属的高频数据表。
# ==========================================

# london_gold_monitor.py
import time
import schedule
from datetime import datetime
from core.london_gold_fetcher import LondonGoldFetcher
from core.cleaner import DataCleaner
from core.storage import DataStorage


class LondonGoldMonitor:
    """伦敦金5分钟级行情监控器（AKShare 稳定版）"""

    def __init__(self):
        self.fetcher = LondonGoldFetcher()
        self.cleaner = DataCleaner()
        self.storage = DataStorage()
        self.table_name = "london_gold_5min"

    def fetch_and_save(self):
        """核心动作：抓取最新5分钟数据并入库"""
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n⏰ [{now_str}] 正在获取伦敦金最新数据...")

        try:
            # AKShare 会一次性返回近期的所有 5 分钟数据，我们每次只取最新的
            raw_data = self.fetcher.fetch_5min_data()

            if raw_data is None or raw_data.empty:
                print("😴 API返回空数据（可能是休市），跳过本次入库。")
                return

            # 清洗数据
            clean_data = self.cleaner.clean_london_gold_data(raw_data)

            # 强力安检：过滤掉价格为 0 的无效数据
            price_cols = ['close', 'open']
            for col in price_cols:
                if col in clean_data.columns:
                    clean_data = clean_data[clean_data[col] != 0]

            if clean_data.empty:
                print("😴 清洗后无有效数据，跳过入库。")
                return

            # 去重并入库
            clean_data = clean_data.drop_duplicates()
            self.storage.save_to_db(clean_data, self.table_name)
            print(f"✅ 成功更新 {len(clean_data)} 条有效数据到 [{self.table_name}]")

        except Exception as e:
            print(f"❌ 伦敦金监控任务异常: {e}")
            import traceback
            traceback.print_exc()

    def start(self):
        print("🚀 伦敦金 5 分钟独立监控服务已启动！")
        print("💡 提示：按 Ctrl+C 可安全停止服务。")

        self.fetch_and_save()  # 启动时先立刻执行一次
        schedule.every(5).minutes.do(self.fetch_and_save)

        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 监控服务已手动停止。")


if __name__ == '__main__':
    monitor = LondonGoldMonitor()
    monitor.start()

