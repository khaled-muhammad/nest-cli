import psycopg2
from utils import username
import os

def create_db(db_name):
    os.system(f'nest db create {db_name}')

def list_user_databases():
    conn = psycopg2.connect(
        dbname=username,
    )
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
    dbs = [row[0] for row in cur.fetchall() if row[0].startswith(username + "_")]
    cur.close()
    conn.close()
    return dbs

def remove_database(db_name):
    conn = psycopg2.connect(
        dbname='postgres',
    )
    conn.autocommit = True
    cur = conn.cursor()
    try:
        cur.execute(f"DROP DATABASE {db_name};")
        success = True
        message = f"Database {db_name} removed successfully."
    except Exception as e:
        success = False
        message = str(e)
    cur.close()
    conn.close()
    return success, message