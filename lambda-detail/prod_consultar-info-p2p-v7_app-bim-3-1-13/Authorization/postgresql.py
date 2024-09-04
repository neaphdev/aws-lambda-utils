

import psycopg2
from collections import namedtuple
from datetime import datetime, timedelta
import pytz

class PostgreSQLData:
    """Database connection class."""

    def __init__(self,cfg):
        self.db_username = cfg["user"]
        self.db_password = cfg["password"]
        self.db_name = cfg["database"]
        self.db_host = cfg["host"]
        self.db_port = cfg["port"]
        self.db_cnn_timeout = cfg["timeout"]
        self.conn = None

    def open_connection(self):
        """Connect to PostgreSQL Database."""
        try:
            if self.conn is None:
                self.conn = psycopg2.connect(
                    dbname=self.db_name,
                    user=self.db_username,
                    password=self.db_password,
                    host=self.db_host,
                    port=self.db_port,
                    connect_timeout=self.db_cnn_timeout,
                )
        except psycopg2.Error as e:
            print("Error psycopg2:", e)
        except Exception as e:
            print("Error otro:", e)
        finally:
            print("Connection opened successfully.")

    def select_query(self, query: str, param: tuple) -> tuple:
        """Select SQL query."""
        try:
            self.open_connection()
            cursor = self.conn.cursor()
            cursor.execute(query, param)
            columns = [desc[0] for desc in cursor.description]  # Obtener los nombres de las columnas
            Row = namedtuple('Row', columns)  # Crear una namedtuple con los nombres de las columnas
            records = [Row(*row) for row in cursor.fetchall()]  
            affected = cursor.rowcount
            cursor.close()
            return True, records, affected
        except psycopg2.Error as e:
            print("Error psycopg2:", e)
            return False, e, 0
        finally:
            if self.conn:
                self.conn.close()
                self.conn = None
                print("Database connection closed.")

    def insert_query(self, query: str, param: tuple) -> tuple:
        """Insert SQL query."""
        try:
            self.open_connection()
            with self.conn.cursor() as cur:
                _ = cur.execute(query, param)
                self.conn.commit()
                affected = cur.rowcount
                return True, affected
        except psycopg2.Error as e:
            print("Error psycopg2:", e)
            return False, e
        finally:
            if self.conn:
                self.conn.close()
                self.conn = None
                print("Database connection closed.")

    def update_query(self, query: str, param: tuple) -> tuple:
        """Update SQL query."""
        try:
            self.open_connection()
            with self.conn.cursor() as cur:
                cur.execute(query, param)
                self.conn.commit()
                affected = cur.rowcount
                return True, affected
        except psycopg2.Error as e:
            print("Error psycopg2:", e)
            return False, e
        finally:
            if self.conn:
                self.conn.close()
                self.conn = None
                print("Database connection closed.")

    def delete_query(self, query: str, param: tuple) -> tuple:
        """Delete SQL query."""
        try:
            self.open_connection()
            with self.conn.cursor() as cur:
                cur.execute(query, param)
                self.conn.commit()
                affected = cur.rowcount
                return True, affected
        except psycopg2.Error as e:
            print("Error psycopg2:", e)
            return False, e
        finally:
            if self.conn:
                self.conn.close()
                self.conn = None
                print("Database connection closed.")
