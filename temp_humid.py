import sys
import Adafruit_DHT
import requests
import time
import requests


GPIO_2302_PIN = 22
SENSOR = Adafruit_DHT.AM2302
SAMPLE_INTERVAL = 60*10
#ILISO_HOST = "http://10.164.149.141:12345/update"
ILISO_HOST = "https://iliso.herokuapp.com/update"

while True:
    time.sleep(SAMPLE_INTERVAL)

    humidity, temperature = Adafruit_DHT.read_retry(SENSOR, GPIO_2302_PIN)
    while humidity is None or temperature is  None:
        humidity, temperature = Adafruit_DHT.read_retry(SENSOR, GPIO_2302_PIN)
    # print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
    current_time = time.time()
    payload = {"all_feeds":[{"feed_name":"temperature","samples":[{"value":temperature,"time":current_time}]},
                            {"feed_name":"humidity","samples":[{"value":humidity,"time":current_time}]}]}
    try:
        r = requests.post(ILISO_HOST, json=payload)
    except requests.exceptions.RequestException as e:
        print(e)
        






