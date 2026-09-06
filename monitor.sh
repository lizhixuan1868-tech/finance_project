#!/bin/bash
cd ~/finance_project

RED="\033[0;31m"
GREEN="\033[0;32m"
YELLOW="\033[1;33m"
BLUE="\033[0;34m"
PURPLE="\033[0;35m"
CYAN="\033[0;36m"
WHITE="\033[1;37m"
BOLD="\033[1m"
NC="\033[0m"
BG_BLUE="\033[44m"

while true; do
  clear
  echo -e "${BG_BLUE}${WHITE}${BOLD}"
  echo "╔══════════════════════════════════════════════════════════════╗"
  echo "║     🏦 Finance Project 实时监控面板  |  $(date '+%Y-%m-%d %H:%M:%S')     ║"
  echo "╚══════════════════════════════════════════════════════════════╝"
  echo -e "${NC}"
  echo ""
  echo ""

  # ========== 进程运行状态 ==========
  echo -e "${YELLOW}${BOLD}┌── 📡 进程运行状态 ─────────────────────────────────────────┐${NC}"
  SCHEDULER=$(ps aux | grep "scheduler" | grep -v grep)
  if [ -n "$SCHEDULER" ]; then
    PID=$(echo "$SCHEDULER" | awk "{print \$2}")
    CPU=$(echo "$SCHEDULER" | awk "{print \$3}")
    MEM=$(echo "$SCHEDULER" | awk "{print \$4}")
    UPTIME=$(ps -p "$PID" -o etime= 2>/dev/null | tr -d " ")
    echo -e "  ${GREEN}✅ scheduler.py${NC}"
    echo -e "     ${WHITE}PID  : ${BOLD}$PID${NC}"
    echo -e "     ${WHITE}CPU  : ${YELLOW}$CPU%%${NC}"
    echo -e "     ${WHITE}MEM  : ${YELLOW}$MEM%%${NC}"
    echo -e "     ${WHITE}运行 : ${PURPLE}$UPTIME${NC}"
  else
    echo -e "  ${RED}❌ scheduler.py 未运行！${NC}"
  fi
  echo ""
  LONDON=$(ps aux | grep "london_gold_monitor" | grep -v grep)
  if [ -n "$LONDON" ]; then
    LPID=$(echo "$LONDON" | awk "{print $2}")
    LCPU=$(echo "$LONDON" | awk "{print $3}")
    LMEM=$(echo "$LONDON" | awk "{print $4}")
    LUPTIME=$(ps -p "$LPID" -o etime= 2>/dev/null | tr -d " ")
    echo -e "  ${GREEN}✅ london_gold_monitor.py${NC}"
    echo -e "     ${WHITE}PID  : ${BOLD}$LPID${NC}"
    echo -e "     ${WHITE}CPU  : ${YELLOW}$LCPU%%${NC}"
    echo -e "     ${WHITE}MEM  : ${YELLOW}$LMEM%%${NC}"
    echo -e "     ${WHITE}运行 : ${PURPLE}$LUPTIME${NC}"
  else
    echo -e "  ${RED}❌ london_gold_monitor.py 未运行！${NC}"
  fi
  echo -e "${YELLOW}└──────────────────────────────────────────────────────────────┘${NC}"
  echo ""
  echo ""

  # ========== 调度器日志 ==========
  echo -e "${PURPLE}${BOLD}┌── 📋 调度器日志 (最近8行) ─────────────────────────────────┐${NC}"
  tail -8 scheduler.log 2>/dev/null | while IFS= read -r line; do
    echo -e "  ${CYAN}$line${NC}"
  done
  echo -e "${PURPLE}└──────────────────────────────────────────────────────────────┘${NC}"
  echo ""
  echo ""

  # ========== 系统资源监控 ==========
  echo -e "${BLUE}${BOLD}┌── 💻 系统资源监控 ─────────────────────────────────────────┐${NC}"
  CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk "{print \$2}" | cut -d"%" -f1)
  CPU_INT=${CPU_USAGE%.*}
  BAR_LEN=30
  FILLED=$((CPU_INT * BAR_LEN / 100))
  EMPTY=$((BAR_LEN - FILLED))
  BAR=""
  for ((i=0; i<FILLED; i++)); do BAR+="█"; done
  for ((i=0; i<EMPTY; i++)); do BAR+="░"; done
  echo -e "  ${WHITE}CPU  :${NC} ${GREEN}[${BAR}]${NC} ${BOLD}${CPU_USAGE}%%${NC}"
  MEM_TOTAL=$(free -m | awk "/Mem:/{print \$2}")
  MEM_USED=$(free -m | awk "/Mem:/{print \$3}")
  MEM_PERCENT=$((MEM_USED * 100 / MEM_TOTAL))
  MEM_FILLED=$((MEM_PERCENT * BAR_LEN / 100))
  MEM_EMPTY=$((BAR_LEN - MEM_FILLED))
  MEM_BAR=""
  for ((i=0; i<MEM_FILLED; i++)); do MEM_BAR+="█"; done
  for ((i=0; i<MEM_EMPTY; i++)); do MEM_BAR+="░"; done
  echo -e "  ${WHITE}内存 :${NC} ${GREEN}[${MEM_BAR}]${NC} ${BOLD}${MEM_PERCENT}%%${NC}  (${MEM_USED}M / ${MEM_TOTAL}M)"
  DISK_USED=$(df -h / | tail -1 | awk "{print \$3}")
  DISK_TOTAL=$(df -h / | tail -1 | awk "{print \$2}")
  DISK_PERCENT=$(df -h / | tail -1 | awk "{print \$5}" | tr -d "%")
  DISK_FILLED=$((DISK_PERCENT * BAR_LEN / 100))
  DISK_EMPTY=$((BAR_LEN - DISK_FILLED))
  DISK_BAR=""
  for ((i=0; i<DISK_FILLED; i++)); do DISK_BAR+="█"; done
  for ((i=0; i<DISK_EMPTY; i++)); do DISK_BAR+="░"; done
  echo -e "  ${WHITE}磁盘 :${NC} ${GREEN}[${DISK_BAR}]${NC} ${BOLD}${DISK_PERCENT}%%${NC}  (${DISK_USED} / ${DISK_TOTAL})"
  LOAD=$(uptime | awk -F"load average:" "{print \$2}")
  echo -e "  ${WHITE}负载 :${NC} ${PURPLE}$LOAD${NC}"
  echo -e "${BLUE}└──────────────────────────────────────────────────────────────┘${NC}"
  echo ""
  echo ""

  # ========== 数据产出文件 ==========
  echo -e "${GREEN}${BOLD}┌── 📊 数据产出文件 ─────────────────────────────────────────┐${NC}"
  ls -lht data/ 2>/dev/null | head -4 | tail -3
  echo -e "${GREEN}└──────────────────────────────────────────────────────────────┘${NC}"
  echo ""
  echo ""

  echo -e "${BG_BLUE}${WHITE} 按 Ctrl+C 退出监控  |  刷新间隔: 60秒  |  服务器: $(hostname)  ${NC}"
  sleep 60
done
