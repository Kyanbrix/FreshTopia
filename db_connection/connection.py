
import sqlite3


class ConnectionPool:


    def __init__(self,database_name):
        self.connection = sqlite3.connect(database=database_name)

    
    def sql_connection(self):
        return self.connection

    def close_connection(self):
        self.connection.close()

    




        
    






