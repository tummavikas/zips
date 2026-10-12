FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend backend
COPY frontend frontend
COPY data/documents data/documents
COPY Readme.md README.md
EXPOSE 8000 8501
