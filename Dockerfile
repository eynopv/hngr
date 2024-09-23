FROM python:3.12-slim-bookworm

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install --with-deps

CMD ["uvicorn", "hngr.main:app", "--host", "0.0.0.0", "--port", "5000"]
