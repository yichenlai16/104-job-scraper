FROM python:3.12
ENV PYTHONUNBUFFERED 1

# 設定工作目錄
WORKDIR /app

# 複製 requirements.txt 到 container
COPY requirements.txt .

# 安裝packages
RUN pip install -r requirements.txt

# 複製專案到 container
COPY . .

# 執行命令
CMD ["python", "scraper/run.py"]