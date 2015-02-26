#takes time in format "MM/DD/YYYY HH/MM/SS" and converts to UNIX time stamp 
from datetime import datetime
import pytz


def to_datetime(ts):
    day = int(ts[0:2])
    month = int(ts[3:5])
    year = int(ts[6:10])
    hour = int(ts[11:13])
    minute = int(ts[14:16])
    second = int(ts[17:19])
    
    return datetime(year, day, month, hour, minute, second)

def to_unix(dt, epoch = datetime(1970, 1, 1, 0, 0, 0)):
    td = to_datetime(dt) - epoch
    return int((td.seconds + td.days * 24 * 3600) * 10**6 / 1e6)

def trend_time(ts, epoch = datetime(1970, 1, 1, 0, 0, 0)):
    if len(ts) < 5:
        ts = '0' + ts
    td = datetime(2015, 1, 1, int(ts[0:2]), int(ts[3:5]), 0) - epoch
    return int((td.seconds + td.days * 24 * 3600) * 10**6 / 1e6)

def main():
    #test time
    stamp = '02/13/2015 06:00:04'
    print stamp
    print to_unix(stamp)
    trend_stamp = '8:00'
    print trend_time(trend_stamp)
    
if __name__ == "__main__":
    main()