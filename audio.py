import pyaudio
import numpy as np
import time
from datetime import datetime
import requests

ILISO_HOST = "http://10.164.149.141:12345/update"

CHUNK_SIZE = 8192
AUDIO_FORMAT = pyaudio.paInt16
SAMPLE_RATE = 16000

p = pyaudio.PyAudio()
stream = p.open(format=AUDIO_FORMAT, channels=1, rate=SAMPLE_RATE, input=True, frames_per_buffer=CHUNK_SIZE)
t_before = 0
minute_max = 0
while True:
    audio = np.fromstring(stream.read(CHUNK_SIZE), np.int16)
    minute_max = max(minute_max, np.abs(audio).max())
    t_now = time.time()
    if (t_now - t_before) / 60 >= 1:
        payload = {"all_feeds":[{"feed_name":"audio","samples":[{"value":int(minute_max),"time":t_now}]}]}
        try:
            r = requests.post(ILISO_HOST, json=payload)
        except requests.exceptions.RequestException as e:
            print(e)
        t_before = t_now
        minute_max = 0
