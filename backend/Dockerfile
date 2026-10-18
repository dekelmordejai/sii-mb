FROM python:3.12-slim AS base
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
WORKDIR /application
COPY requirements-lock.txt ./
RUN pip install --no-cache-dir -r requirements-lock.txt
COPY app ./app
COPY alembic ./alembic

FROM base AS runtime
RUN useradd --create-home --uid 10001 sii && mkdir data && chown sii:sii data
USER sii
EXPOSE 8000
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

FROM base AS test
COPY tests ./tests
CMD ["python", "-m", "pytest", "-q"]
