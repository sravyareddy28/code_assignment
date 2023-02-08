""" The script will create table in SQLite DB.
"""

import sqlite3


class DataTable:
    """
    Class for creating a table in a SQLite database.

    Attributes:
        conn (sqlite3.connect): SQLite database connection.
        cursor (sqlite3.Cursor): SQLite database cursor.
        ddl (str): DDL statement for creating the table.

    Methods:
        create_table (): Executes the DDL statement to create the table.
        close_connection (): Closes the database connection.
    """

    def __init__(self, ddl):
        """
        Initializes the DataTable class.

        Args:
            ddl (str): DDL statement for creating the table.
        """
        self.conn = sqlite3.connect("code_assignment/src/weather.db")
        self.cursor = self.conn.cursor()
        self.ddl = ddl

    def create_table(self):
        """
        Executes the DDL statement to create the table.
        """
        self.cursor.execute(self.ddl)
        self.conn.commit()

    def close_connection(self):
        """
        Closes the database connection.
        """
        self.conn.close()


# ddl statements to create table.
ddl = """
CREATE TABLE IF NOT EXISTS weather_data (
    id INTEGER PRIMARY KEY,
    date DATE,
    station_id String,
    maximum_temp REAL,
    minimum_temp REAL,
    precipitation REAL
);
"""

if __name__ == "__main__":
    # Create an instance of the DataTable class
    weather_data_table = DataTable(ddl)
    # Call the create_table method to execute the DDL statement
    weather_data_table.create_table()
    # closing bd connection.
    weather_data_table.close_connection()
