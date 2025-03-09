from datetime import datetime, timedelta

def is_expired(expiration_date):
    date = datetime.strftime(expiration_date,'%Y-%d-%m')
    
    today = datetime.today().date()

    return date < today

def will_expire_soon(expire_date, days=7):
    date = datetime.strftime(expire_date,'%Y-%d-%m')
    today = datetime.today().date()
    return today >= date - timedelta(days=days)



