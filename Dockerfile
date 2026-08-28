FROM python:3.12-slim

WORKDIR /app

# Install system dependencies and Chinese fonts for Pillow & Word
RUN apt-get update && apt-get install -y --no-install-recommends \
    fonts-wqy-zenhei \
    fontconfig \
    && fc-cache -fv \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies via Tsinghua mirror
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# Copy backend code and pre-compiled frontend dist
COPY backend ./backend
COPY frontend/dist ./frontend/dist

WORKDIR /app/backend

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
