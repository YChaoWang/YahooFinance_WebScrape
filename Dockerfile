FROM python:3.10

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

# 安装Chrome和相关依赖
RUN apt-get update && apt-get install -y wget unzip && \
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb && \
    apt-get clean

# 设置环境变量
ENV CHROMEDRIVER_PATH=/usr/local/bin/chromedriver

CMD ["python3", "yfinancenews.py"]
