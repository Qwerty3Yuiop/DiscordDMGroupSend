import os
import mysql.connector

class MySqlDb:
    def __init__(self):
        db_config = {
            'host': os.environ['MYSQL_HOST'],
            'user': os.environ['MYSQL_USER'],
            'password': os.environ['MYSQL_PASS'],
            'database': os.environ['MYSQL_NAME'] 
        }
        self.connection = mysql.connector.connect(**db_config)

        if self.connection.is_connected():
            self.cursor = self.connection.cursor()
        else:
            raise ConnectionRefusedError("Not connected to db")

    def query(self, query:str, params: tuple = None):
        """
        Executes any SQL query
        """
        if not self.connection or not self.connection.is_connected():
            raise ConnectionRefusedError("Not connected to db")
        
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            if query.strip().upper().startswith("SELECT"):
                return self.cursor.fetchall()
            else:
                return None
        except mysql.connector.Error as err:
            raise err
    
    def commit(self):
        """
        Commits the current transaction to the database.
        Call this after INSERT, UPDATE, DELETE operations.
        """
        if self.connection and self.connection.is_connected():
            try:
                self.connection.commit()
                print("Transaction committed successfully.")
            except mysql.connector.Error as err:
                raise err
        else:
            raise ConnectionRefusedError("Not connected to db")

    def cleanup(self):
        """
        Closes the database cursor and connection.
        """
        if self.cursor:
            self.cursor.close()
            print("Cursor closed.")
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("MySQL connection closed.")

