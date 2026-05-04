# Stage 1: Build
FROM python:3.12-slim-bookworm AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.12-slim-bookworm
WORKDIR /app

# Copy only the installed packages
COPY --from=builder /root/.local /root/.local
COPY . .

# Environment
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV HOSTNAME=0.0.0.0

CMD ["python", "main.py"]
