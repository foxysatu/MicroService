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
#get api
EXPOSE 80


EXPOSE 3001
#get BD

EXPOSE 5051
#get server

RUN pip install flask python-keycloak prometheus_flask_exporter

CMD ["python", "main.py"]
