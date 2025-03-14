
from dateutil.relativedelta import relativedelta

from datetime import datetime

class AppDate:

    def __init__(self, date):
        self.current_date = date

    def add_months(self, month):
        return self.current_date + relativedelta(months=month)

    def add_days(self, days):
        return self.current_date + relativedelta(days=days)

    def add_years(self, years):
        return self.current_date + relativedelta(years=years)
    

class DateFormatter:


    def __init__(self, datetime : str):
        self.datetime = datetime
    

    def format_datetime_to_fullname(self):
        datetime_obj = datetime.strptime(self.datetime,'%Y-%m-%d')

        return datetime_obj.date().strftime('%B %d, %Y')






        