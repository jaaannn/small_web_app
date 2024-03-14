FROM python:3.11
LABEL authors="jan"

WORKDIR /app

COPY frontend.py /app/

EXPOSE 8080

RUN pip install pywebio requests
CMD ["python", "frontend.py"]