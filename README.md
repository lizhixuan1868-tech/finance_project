📊 A股量化数据中台 - 接口与数据字典说明书
1. 系统概述
本系统是一个基于 Python 构建的自动化量化数据中台。采用“数据工厂（Factory）”架构，支持多资产类别（股票、黄金、期货、原油等）的数据抓取、清洗、因子计算与持久化存储。
2. 支持的资产类别与数据字典
2.1 股票数据 (Stock)
资产类型标识 (asset_type): stock
数据源: BaoStock
支持的标的: 全市场 A 股（沪深京 A 股）
代码格式要求: 纯数字 6 位代码，例如 600519（贵州茅台）、000001（平安银行）
包含字段: 日期、开盘价、最高价、最低价、收盘价、成交量、换手率
内置因子: MA_5, MA_10, MA_20, RSI_14
2.2 黄金数据 (Gold)
资产类型标识 (asset_type): gold
数据源: AkShare
支持的标的: 上海黄金交易所现货黄金
代码格式要求: Au99.99
包含字段: 日期、开盘价、最高价、最低价、收盘价、成交量
内置因子: MA_5, MA_10, MA_20, RSI_14
2.3 期货数据 (Futures)
资产类型标识 (asset_type): futures
数据源: AkShare
支持的标的: 国内主流期货品种的主力连续合约
代码格式要求: 品种小写字母 + 0，例如 rb0（螺纹钢主力）、i0（铁矿石主力）
包含字段: 日期、开盘价、最高价、最低价、收盘价、成交量、持仓量
内置因子: MA_5, MA_10, MA_20, RSI_14
2.4 原油数据 (Crude)
资产类型标识 (asset_type): crude
数据源: AkShare
支持的标的: WTI 原油期货 / 国内原油期货
代码格式要求: CL (WTI) 或 sc0 (国内原油)
包含字段: 日期、开盘价、最高价、最低价、收盘价、成交量
内置因子: MA_5, MA_10, MA_20, RSI_14
3. 调用指南 (How to Use)
3.1 核心调用方法
通过 DataFactory 的 process 方法统一调度：
python

编辑



factory.process(
    asset_type='stock',       # 必填：资产类型
    symbol='600519',          # 必填：资产代码
    start_date='20230101',    # 必填：开始日期 (YYYYMMDD)
    end_date='20231231'       # 必填：结束日期 (YYYYMMDD)
)
3.2 常用查询示例
查询贵州茅台 2023 全年数据:
factory.process('stock', '600519', '20230101', '20231231')
查询螺纹钢主力 2024 年至今数据:
factory.process('futures', 'rb0', '20240101', '20260830')
4. 数据库表结构 (Data Storage)
所有处理后的数据默认存入 SQLite 数据库，表名规则如下：
原始清洗表: {asset_type}_daily (例: stock_daily, futures_daily)
因子宽表: {asset_type}_daily_factors (例: gold_daily_factors)