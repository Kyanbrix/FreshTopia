
import sqlite3


class ConnectionPool:


    def __init__(self):
        self.connection = sqlite3.connect('databasename')

    
    def sql_connection(self):
        return self.connection

    def close_connection(self):
        self.connection.close()

    




        
    






