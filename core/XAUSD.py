import akshare as ak
import pandas as pd
import schedule
import time
from datetime import datetime
from core.storage import DataStorage


class LondonGoldMonitor:
    """伦敦金日线行情监控器（带均线计算）"""

    def __init__(self):
        self.storage = DataStorage()
        self.table_name = "new_london_gold"

    def fetch_and_save(self):
        """核心动作：抓取日线数据、计算均线并入库"""
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n⏰ [{now_str}] 正在获取伦敦金最新日线数据...")

        try:
            # 1. 获取历史日K线数据
            df = ak.futures_foreign_hist(symbol="XAU")

            if df is None or df.empty:
                print("😴 API返回空数据（可能是休市），跳过本次入库。")
                return

            # 2. 数据清洗与排序
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values(by='date', ascending=True).reset_index(drop=True)

            # 3. 计算常用均线
            df['MA5'] = df['close'].rolling(window=5).mean()
            df['MA10'] = df['close'].rolling(window=10).mean()
            df['MA20'] = df['close'].rolling(window=20).mean()
            df['MA30'] = df['close'].rolling(window=30).mean()

            # 4. 截取最近30天的数据，并将日期改为降序（最新的在最上面）
            df_last_30_days = df.tail(30).sort_values(by='date', ascending=False).reset_index(drop=True)

            # 5. 强力安检：过滤掉价格为 0 的无效数据
            price_cols = ['close', 'open']
            for col in price_cols:
                if col in df_last_30_days.columns:
                    df_last_30_days = df_last_30_days[df_last_30_days[col] != 0]

            if df_last_30_days.empty:
                print("😴 清洗后无有效数据，跳过入库。")
                return

            # 6. 写入腾讯云数据库
            self.storage.save_to_db(df_last_30_days, self.table_name)

            # 打印最新价格
            latest_price = df_last_30_days.iloc[0]['close']
            print(f"✅ 成功更新 {len(df_last_30_days)} 条日线数据到 [{self.table_name}]")
            print(f"📈 伦敦金 (XAU) 最新价格: {latest_price} 美元/盎司")

        except Exception as e:
            print(f"❌ 伦敦金监控任务异常: {e}")
            import traceback
            traceback.print_exc()

    def start(self):
        print("🚀 伦敦金日线独立监控服务已启动！")
        print("💡 提示：按 Ctrl+C 可安全停止服务。")

        # 启动时先立刻执行一次
        self.fetch_and_save()

        # 每天固定时间执行（比如每天 08:30，因为此时美股刚收盘，日线数据最全）
        schedule.every().day.at("08:30").do(self.fetch_and_save)

        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 监控服务已手动停止。")


if __name__ == "__main__":
    m = LondonGoldMonitor()
    m.start()