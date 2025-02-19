FROM cloud-sample.tencentcloudcr.com/devops-pub/python:3.10-slim-bookworm
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# 复制应用代码
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
