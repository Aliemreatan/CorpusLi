# Python 3.9 yerine 3.10 kullanıyoruz
FROM python:3.14-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    libx11-6 \
    && rm -rf /var/lib/apt/lists/*

# pip'i en güncel sürüme çekiyoruz (hata logunda uyarı vermişti)
RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN python -m spacy download tr_core_news_sm

COPY . .

CMD ["python", "run_gui.py"]