#test feeding data to graphite using StatsD

import statsd
from random import randint
from time import sleep

delay = 60 #sending UDP packet every 60 seconds

#gauge is a metric type used by StatsD that sends the most recent data
#until a new value is sent. 'random int' is the name of the metric to
#be sent to graphite, and x is the value associated with it. For the
#gauge metric type, timestamps are added automatically when send() is used
def test_random(delay):
    gauge = statsd.Gauge('test')
    while True:
        for i in range(10):
            x = randint(0+6*i, 10+6*i)
            gauge.send('random int', x)
            print x, 'sent'
            sleep(delay)

def main():
    test_random(delay)

if __name__ == "__main__":
    main()
