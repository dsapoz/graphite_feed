#test feeding data to graphite using StatsD

import statsd
from random import randint
from time import sleep

delay = 60

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