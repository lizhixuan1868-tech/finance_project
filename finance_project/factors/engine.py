# ==========================================
# 这个文件是项目的“加工厂”（计算引擎）
# 它的唯一职责就是：用洗好的数据，计算出各种金融技术指标。
# ==========================================

import pandas as pd

#定义一个类
class FactorEngine:
    """
    因子计算引擎。
    专门写各种数学公式，把简单的价格变成高级的分析指标。
    """

    @staticmethod
    def add_moving_averages(df,windows=[5,10,20]):
        """
        计算移动平均线。
        :param df: 洗好的 Pandas DataFrame 数据
        :param windows: 移动平均线的窗口期列表，默认计算5、10、20日均线
        """

        #默认：先判断数据是否为空
        if df is None or df.empty:
            return None

        #遍历传入的周期，用Pandas的rolling方法计算滚动平均值
        for window in windows:
            df[f'MA_{window}'] = df['close'].rolling(window=window).mean()

        print(f'📈 均线计算完成！已添加 MA_{windows}')
        return df

    @staticmethod
    def add_rsi(df,period=14):
        """
        计算相对强弱指数（RSI）。
        :param df: 洗好的 Pandas DataFrame 数据
        :param period: RSI的周期，默认为14
        :return: 添加了RSI指标的 DataFrame
        """

        #默认：判断是否为空
        if df is None or df.empty:
            return None

        #1.计算每天价格的变化量（今天的收盘价-昨天的收盘价）
        delta = df['close'].diff()

        # 2. 把上涨的天数单独拿出来，下跌的记为 0，然后算过去 14 天的平均涨幅
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()

        # 3. 把下跌的天数单独拿出来，上涨的记为 0，然后算过去 14 天的平均跌幅
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

        # 4. 计算相对强度（RS），然后套用 RSI 公式
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))

        print(f"📊 RSI 指标计算完成！周期为 {period} 天")
        return df