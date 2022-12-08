import mariadb
import sys
from os import environ

try:
    pool: mariadb.Connection = mariadb.ConnectionPool(
        user=environ.get("DB_USER"),
        password=environ.get("DB_PASSWORD"),
        host=environ.get("DB_HOST"),
        port=3306,
        database=environ.get("DB_NAME"),
        pool_name="web-app",
        pool_size=3,
    )
except mariadb.Error as e:
    print(f"Error connecting to MySQL Platform: {e}")
    sys.exit(1)