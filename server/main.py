from Adafruit_BBIO import GPIO, ADC
from redis import StrictRedis
from time import sleep
import threading
from random import randint
from threading import Thread

VOLTAGE_INPUT  = "P9_33"
TRIGGER_INPUT  = "P9_24"
CLEAR_FLIPFLOP = "P9_27"

class MeasureThread(Thread):
    def __init__(self):
        self.list_adc = [0]*4096
        Thread.__init__(self)
        GPIO.setup(CLEAR_FLIPFLOP, GPIO.OUT)
        GPIO.output(CLEAR_FLIPFLOP, GPIO.LOW)
        sleep(1)
        GPIO.output(CLEAR_FLIPFLOP, GPIO.HIGH)

        GPIO.setup(TRIGGER_INPUT, GPIO.IN)

        self.client = StrictRedis(host = "127.0.0.1")
        self.list_lock = threading.Lock()

        ADC.setup()

    def run(self):
        while True:
            while not GPIO.input(TRIGGER_INPUT): # Waiting to receive start pulse
                pass

            cap_sleep = float(self.client.get("capacitor_sleep"))

            adc_value = int(ADC.read(VOLTAGE_INPUT)*4096)
            with self.list_lock:
                self.list_adc[adc_value] += 1

            GPIO.output(CLEAR_FLIPFLOP, GPIO.LOW)
            sleep(cap_sleep)
            GPIO.output(CLEAR_FLIPFLOP, GPIO.HIGH)
