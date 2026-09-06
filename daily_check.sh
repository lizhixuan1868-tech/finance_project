#!/bin/bash
cd ~/finance_project
echo "========================================" >> daily_check.log
echo "巡检时间: $(date '+%Y-%m-%d %H:%M:%S')" >> daily_check.log
echo "========================================" >> daily_check.log
echo '' >> daily_check.log
echo '▸ 进程运行状态' >> daily_check.log
ps aux | grep -E 'scheduler|london_gold_monitor' | grep -v grep | awk '{printf "  %-35s PID: %-8s 运行中\n", $11, $2}' >> daily_check.log
echo '' >> daily_check.log
echo '▸ 调度器日志 (最近5行)' >> daily_check.log
cat config/scheduler.log scheduler.log 2>/dev/null | tail -5 | sed 's/^/  /' >> daily_check.log
echo '' >> daily_check.log
echo '▸ 数据产出文件' >> daily_check.log
ls -lht data/ 2>/dev/null | head -6 | sed 's/^/  /' >> daily_check.log
echo '' >> daily_check.log
echo '▸ 磁盘使用情况' >> daily_check.log
df -h / | tail -1 | awk '{printf "  已用: %s / 总量: %s (使用率: %s)\n", $3, $2, $5}' >> daily_check.log
echo '' >> daily_check.log
