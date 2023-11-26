from datetime import datetime, timedelta

def print_x(raw_str):
    datetime_x = datetime.utcnow() + timedelta(hours=5.0, minutes=30.0)
    datetime_x = datetime_x.strftime('%Y-%m-%d %H:%M:%S IST -> ')

    print(f"{datetime_x} {raw_str}")
