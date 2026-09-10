import akshare as ak
import pandas as pd
from core.london_gold_fetcher import LondonGoldFetcher
from core.cleaner import DataCleaner
from core.storage import DataStorage


def get_gold_monthly_data():
    try:
        print("正在获取伦敦金(XAU)历史数据并计算均线...")

        # 1. 获取历史日K线数据
        # 注意：为了计算30日均线，这里我们拉取过去60天的数据，避免前30天均线为空
        df = ak.futures_foreign_hist(symbol="XAU")

        # 2. 数据清洗与排序
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values(by='date', ascending=True).reset_index(drop=True)

        # 3. 核心功能：计算常用均线 (MA5, MA10, MA20, MA30)
        df['MA5'] = df['close'].rolling(window=5).mean()
        df['MA10'] = df['close'].rolling(window=10).mean()
        df['MA20'] = df['close'].rolling(window=20).mean()
        df['MA30'] = df['close'].rolling(window=30).mean()

        # 4. 截取最近30天的数据，并将日期改为降序（最新的在最上面）
        df_last_30_days = df.tail(30).sort_values(by='date', ascending=False).reset_index(drop=True)

        # 5. 提取最新的实时价格（即最新一天的收盘价）
        latest_price = df_last_30_days.iloc[0]['close']

        # 6. 格式化输出
        print("=" * 90)
        print(f"📈 伦敦金 (XAU) 最新价格: {latest_price} 美元/盎司")
        print(f"📊 过去30天每日行情及均线数据:")
        print("=" * 90)

        # 筛选出需要展示的列，并保留两位小数让表格更清爽
        display_cols = ['date', 'open', 'high', 'low', 'close', 'MA5', 'MA10', 'MA20', 'MA30']
        display_df = df_last_30_days[display_cols].copy()
        display_df.columns = ['日期', '开盘价', '最高价', '最低价', '收盘价', 'MA5', 'MA10', 'MA20', 'MA30']

        # 将数值统一保留两位小数
        # 只对价格和均线列保留两位小数
        price_cols = ['开盘价', '最高价', '最低价', '收盘价', 'MA5', 'MA10', 'MA20', 'MA30']
        display_df[price_cols] = display_df[price_cols].round(2)

        print(display_df.to_string(index=False))
        print("=" * 90)

        return latest_price, df_last_30_days

    except Exception as e:
        print(f"❌ 获取数据失败: {e}")
        return None, None




if __name__ == "__main__":
    get_gold_monthly_data()