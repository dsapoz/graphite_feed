from datetime import datetime

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

def main():
    #test time
    stamp = '02/13/2015 06:00:04'
    print stamp
    print to_unix(stamp)
    
if __name__ == "__main__":
    main()


