from datetime import datetime

def convert_date(date_string):
    date_string = date_string[:-4]  # Remove the last three zeros
    new_date = (datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%f'))
    return new_date