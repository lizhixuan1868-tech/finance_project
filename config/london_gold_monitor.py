# london_gold_monitor.py
# ==========================================
# 【伦敦金实时监控模块】
# 职责：每5分钟获取一次伦敦金最新价格，并自动存入专属的高频数据表。
# ==========================================

import time
import schedule
import pandas as pd
from datetime import datetime
from core.gold_fetcher import GoldFetcher
from core.cleaner import DataCleaner
from core.storage import DataStorage


class LondonGoldMonitor:
    """伦敦金5分钟级行情监控器"""

    def __init__(self):
        self.fetcher = GoldFetcher()
        self.cleaner = DataCleaner()
        self.storage = DataStorage()
        self.table_name = "london_gold_5min"

    def fetch_and_save(self):
        """核心动作：抓取最新数据并入库"""
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n⏰ [{now_str}] 正在获取伦敦金最新数据...")

        try:
            # 【修复1】：去掉了 freq='5min'，先让现有的抓取接口跑通
            raw_data = self.fetcher.fetch_gold_history(
                symbol='XAU',
                start_date=datetime.now().strftime("%Y%m%d"),
                end_date=datetime.now().strftime("%Y%m%d"),
                market_type='intl'
            )

            if raw_data is None or raw_data.empty:
                print("😴 当前非交易时段或暂无新数据。")
                return

            clean_data = self.cleaner.clean_london_gold_data(raw_data)

            # 【修复2】：存入数据库前，去掉完全重复的行，防止5分钟重复抓取导致数据翻倍
            clean_data = clean_data.drop_duplicates()

            self.storage.save_to_db(clean_data, self.table_name)
            print(f"✅ 成功更新 {len(clean_data)} 条数据到 [{self.table_name}]")

        except Exception as e:
            print(f"❌ 伦敦金监控任务异常: {e}")

    def start(self):
        """启动定时任务"""
        print("🚀 伦敦金5分钟监控服务已启动！")
        print("💡 提示：按 Ctrl+C 可安全停止服务。")

        self.fetch_and_save()  # 启动时先立刻执行一次

        # 【修复3】：确保 schedule 库正常加载
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