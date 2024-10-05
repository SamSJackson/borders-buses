import pandas as pd
import pyodbc
import sqlalchemy as sa
import os 

# Make these ENV variables

username = "sa"
password = os.environ.get("SQL_PWD")
server = "172.17.0.1"
port = "1433"
database = "TestDB"

connection_uri = sa.engine.url.URL(
        'mssql+pyodbc',
        username=username,
        password=password,
        host=server,
        port=port,
        database=database,
        query = {
            "driver": "ODBC Driver 18 for SQL Server",
            "TrustServerCertificate": "yes"
        } 
)
engine = sa.create_engine(connection_uri)

with engine.begin() as conn:
    df = pd.read_sql_query(sa.text('SELECT * FROM Inventory'), conn)

print(df)

