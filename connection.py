
import psycopg2


class ConnectionPool:


    def __init__(self):
        self.connection = psycopg2.connect(database = '',
                            user = '',
                            password = '',
                            port= '')

    
    def sql_connection(self):
        return self.connection

    def close_connection(self):
        self.connection.close()

    def insert_data(self,sql):
        
        try:
        
            self.connection.cursor(sql)
            self.connection.commit()
        
        except Exception as e:
            print(e)




        
    






