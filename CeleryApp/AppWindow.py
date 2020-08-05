from celery import group, chain, chord
from HW11Celery import weather
import time


sleep_time = 5


testweather = weather()

while True:
    print(testweather.state)
    print(testweather.get)
    print('To exit a program hit Ctrl+C')
    time.sleep(sleep_time)
