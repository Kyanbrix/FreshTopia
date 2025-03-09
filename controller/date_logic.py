
from dateutil.relativedelta import relativedelta

class AppDate:

    def __init__(self, date):
        self.current_date = date

    def add_months(self, month):
        return self.current_date + relativedelta(months=month)

    def add_days(self, days):
        return self.current_date + relativedelta(days=days)

    def add_years(self, years):
        return self.current_date + relativedelta(years=years)