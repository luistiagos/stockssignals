from datetime import datetime

def utc_to_localdate(utcdate):
    diff = datetime.utcnow() - datetime.now()
    return utcdate - diff

def new_utc_date():
    return datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

def new_utc_date_hours():
    return datetime.utcnow().replace(minute=0, second=0, microsecond=0)

def new_utc_date_minutes():
    return datetime.utcnow().replace(second=0, microsecond=0)

def strdatetime_to_date(datestr, timestr):
    date_time_str = datestr + ' ' + timestr
    return datetime.strptime(date_time_str, '%d/%m/%Y %H:%M:%S')
