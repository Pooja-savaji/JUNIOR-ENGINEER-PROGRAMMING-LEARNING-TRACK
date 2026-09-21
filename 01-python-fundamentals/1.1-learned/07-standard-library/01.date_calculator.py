from datetime import date, timedelta

today = date.today()

print("Today:", today)

days = int(input("Enter number of days: "))

future_date = today + timedelta(days=days)

print("Future date:", future_date)
