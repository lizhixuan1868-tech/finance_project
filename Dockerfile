# 1. 基础镜像：Python 3.14 精简版
FROM python:3.14-slim

# 2. 设置工作目录
WORKDIR /app

# 3. 【关键】安装系统级编译工具、库和CA证书
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libxml2-dev \
    libxslt1-dev \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# 4. 复制清理后的依赖文件
COPY requirements.txt .

# 5. 安装 Python 依赖（--trusted-host 跳过SSL验证检查）
RUN pip install --no-cache-dir --ignore-requires-python -r requirements.txt

# 6. 复制项目源码
COPY . .

# 7. 暴露端口
EXPOSE 8000

# 8. 启动命令
CMD ["python", "scheduler.py"]