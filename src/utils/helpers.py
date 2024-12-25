from datetime import datetime, timedelta

class DateTimeHelper:
    @staticmethod
    def get_date_range(start_date, end_date):
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        return start, end
    
    @staticmethod
    def format_date(date):
        return date.strftime('%Y-%m-%d')

class CurrencyHelper:
    @staticmethod
    def format_price(amount):
        return f"${amount:,.2f}" 