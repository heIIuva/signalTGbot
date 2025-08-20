# syntax=docker/dockerfile:1.7
FROM python:3.11-slim AS base

# 1) Базовые оптимизации
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    # выставь свой часовой пояс при желании
    TZ=UTC

WORKDIR /app

# 2) Системные зависимости (минимум)
# Добавь пакеты под твои либы (например, libpq5 для psycopg2-binary и т.п.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl tzdata \
    && rm -rf /var/lib/apt/lists/*

# 3) Устанавливаем зависимости Python с кешем buildx
# (cache=type=gha работает в GitHub Actions, ускоряет сборку)
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    python -m pip install --upgrade pip && \
    pip install -r requirements.txt

# 4) Копируем код
COPY . .

# 5) Безопасность: запускаем не от root
RUN useradd -ms /bin/bash appuser
USER appuser

# 6) Healthcheck (простой пинг интерпретатора)
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s \
  CMD python -c "import sys; sys.exit(0)"

# 7) Точка входа
CMD ["python", "src/bot.py"]
