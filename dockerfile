FROM python:3.11.7-slim-bullseye

WORKDIR /app
COPY . .

RUN pip install requests
RUN pip install uvicorn
RUN pip install fastapi
RUN pip install opentelemetry-sdk
RUN pip install opentelemetry-api
RUN pip install opentelemetry-exporter-jaeger
RUN pip install tracer



#RM if loading to yandex
EXPOSE 80

CMD ["python", "main.py"]
