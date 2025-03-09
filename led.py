import utils.expiration_check as exp
import db_connection.connection as connection
from gpiozero import LED



led1 = LED(17)




expired_items = []

conn = connection.ConnectionPool().sql_connection()

cursor = conn.cursor()

cursor.execute("SELECT * FROM inventory") ## I change ang table name

data = cursor.fetchall()

for row in data:
    if row[0] in expired_items:
        continue
    if exp.is_expired(row[3]):
        expired_items.append(row[0])
        led1.on()
        
    







    
    
    



