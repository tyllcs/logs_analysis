FROM python:3.13
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY tests/ ./tests/

ENV PYTHONPATH=/app

ENTRYPOINT ["pytest", "/app/tests/main_test.py", "-v"]