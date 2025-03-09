from datetime import datetime, timedelta

def is_expired(expiration_date):
    date = datetime.strptime(expiration_date,'%d-%m-%Y').date()
    
    today = datetime.today().date()

    return date < today

def will_expire_soon(expire_date, days=7):

    expire_date = datetime.strptime(expire_date,'%Y-%m-%d').date()
    today = datetime.today().date()
    return today >= expire_date - timedelta(days=days)



