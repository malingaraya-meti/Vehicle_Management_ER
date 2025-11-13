import mysql.connector
from mysql.connector import pooling
from mysql.connector import Error

class DatabaseConnection:
    def __init__(self, config):
        self.config = config
        self.pool = self.create_pool()

    def create_pool(self):
        try:
            pool = pooling.MySQLConnectionPool(
                pool_name="vehicle_management_pool",
                pool_size=5,
                **self.config
            )
            return pool
        except Error as e:
            print(f"Error creating connection pool: {e}")
            return None

    def get_connection(self):
        try:
            connection = self.pool.get_connection()
            return connection
        except Error as e:
            print(f"Error getting connection: {e}")
            return None

    def close_connection(self, connection):
        if connection.is_connected():
            connection.close()