import psycopg2
import json
import utils.expiration_check as exp
from datetime import datetime

connection = psycopg2.connect(database = 'postgres',user = 'postgres',password = 'password', port = 5432)


cursor = connection.cursor()

cursor.execute("SELECT * FROM inventory")

rows = cursor.fetchall()


for row in rows:

    try:
       print(row[3])
       print(exp.is_expired(row[3]))

    except Exception as e:
        new_date = datetime.strptime(row[3],"%Y-%m-%d %H:%M:%S").date()
        print(new_date)
      

connection.close()


