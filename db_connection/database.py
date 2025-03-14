import sqlite3


class Database:


    def __init__(self, db_name : str):
        self.db_name = db_name
        self.connect = sqlite3.connect(database=self.db_name)
        self.cursor = self.connect.cursor()

    
    def executeQuery(self, query : str, params : tuple = ()):
        try:
            self.cursor.execute(query,params)
            self.connect.commit()
        except sqlite3.Error as e:
            print(f"Error on executing a query in database -> {e}")

    def fetch_all_query(self, query : str, params : tuple = ()):
        try:

            self.cursor.execute(query,params)
            return self.cursor.fetchall()
        
        except sqlite3.Error as e:
            print(f"Error on fetching all data -> {e}")

    def fetch_one_query(self, query : str , params : tuple = ()):
        try:
            self.cursor.execute(query,params)
            return self.cursor.fetchone()
        
        except sqlite3.Error as e:
            print(f"Error on fetching a single data -> {e}")
    
    def disconnect(self):
        self.connect.close()
        print('Database closed!')


    
    
