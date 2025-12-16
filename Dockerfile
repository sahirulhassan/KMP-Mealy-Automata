# 1) Base image with Python
FROM python:3.12-slim

# 2) Install graphviz OS package
RUN apt-get update && \
    apt-get install -y graphviz && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 3) Set working directory
WORKDIR /app

# 4) Copy requirements & install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5) Copy the rest of the app
COPY . .

# 6) Expose port Cloud Run will use
ENV PORT 8080
EXPOSE 8080

# 7) Run with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
