from opentelemetry import trace
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from mysql.connector import connect, Error
import os
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.export import ConsoleSpanExporter
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource

provider = TracerProvider()
processor = BatchSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(
    TracerProvider(resource=Resource.create({SERVICE_NAME: "dataManager2"}))
)
jaeger_exporter = JaegerExporter(
    agent_host_name=os.getenv("JAGER_HOSTNAME", "localhost"),
    agent_port=6831,
)
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(jaeger_exporter))

tracer = trace.get_tracer("choice")

app = FastAPI()


def start_con():
    try:
        with tracer.start_as_current_span("listMovieData"):
            connection = connect(
                host=os.getenv('MYSQL_HOST', 'mysql_db'),
                user=os.getenv('MYSQL_USER', 'root'),
                password=os.getenv('MYSQL_PASSWORD', 'Qwerty123'),
            )
            print(connection)
            create_db_query = "CREATE DATABASE IF NOT EXISTS cot"
            use_db_query = "USE cot"
            create_table_query = "CREATE TABLE IF NOT EXISTS imgCot (urlP VARCHAR(255))"
            with connection.cursor() as cursor:
                cursor.execute(create_db_query)
                cursor.execute(use_db_query)
                cursor.execute(create_table_query)
            connection.commit()
    except Error as e:
        print(e)
        return
    return connection

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/')
async def root(data = Body()):

    url = str(data['url'])
    connection = start_con()
    if not connection:
        return
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO imgCot(urlP) VALUES (%s)"
            cursor.execute(sql, (url,))
            # cursor.execute(f"""INSERT INTO imgCot (urlP) VALUES ({url})""")
        connection.commit()
    except Error as e:
        print(e)
    return data

@app.get('/')
async def get_data():
    connection = start_con()
    if not connection:
        return
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT urlP FROM imgCot")
            return [j for i in cursor.fetchall() for j in i]
    except Error as e:
        print(e)
    return list()


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=3001)
