FROM python:3.11
LABEL authors="jan"

WORKDIR /app
RUN mkdir -p /app/database

COPY backend.py /app
COPY schema.sql /app

EXPOSE 5000

RUN pip install flask
CMD ["python", "backend.py"]