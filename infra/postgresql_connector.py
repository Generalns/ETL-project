import psycopg2

def connect_postgresql():
    conn = psycopg2.connect(
        host="postgres", dbname="jobs_project", user="postgres", password="postgres", port="5432"
    )
    return conn
