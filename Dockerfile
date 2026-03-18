FROM python:3.12-slim

# 安装 WeasyPrint 系统依赖
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libcairo2 \
    libgdk-pixbuf-xlib-2.0-0 \
    libffi-dev \
    shared-mime-info \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 安装 Playwright
RUN playwright install --with-deps chromium

COPY . .

# 下载字体
RUN python download_fonts.py

EXPOSE $PORT

CMD gunicorn app:app --bind 0.0.0.0:$PORT --timeout 120 --workers 2