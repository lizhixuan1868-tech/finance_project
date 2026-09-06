from apscheduler.schedulers.blocking import BlockingScheduler
from main import main  # 导入你写好的总指挥
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def run_daily_task():
    """
    定时任务包装器。
    """
    # 【核心】：在触发任务时，动态获取当天的日期
    today = datetime.now().strftime('%Y%m%d')

    logging.info(f"⏰ 定时任务触发：开始执行 {today} 的数据抓取与清洗...")
    try:
        main(target_date=today)  # 【修改】把今天的日期传给 main 函数
        logging.info(f"✅ {today} 数据任务执行成功！")
    except Exception as e:
        logging.error(f"❌ {today} 数据任务执行失败: {e}")


if __name__ == '__main__':
    scheduler = BlockingScheduler()

    # 设定每个工作日的 16:30 自动执行
    scheduler.add_job(
        run_daily_task,
        'cron',
        day_of_week='mon-fri',
        hour=5,
        minute=30,
        timezone='Asia/Shanghai'
    )

    logging.info("🚀 数据调度服务已启动，等待定时触发... (按 Ctrl+C 退出)")

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logging.info("调度服务已安全退出。")