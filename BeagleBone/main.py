from Adafruit_BBIO import GPIO, ADC
from redis import *
from time import sleep

capDischarge  = "P9_xx" # Usar o mesmo pino do clear do FlipFLop ???
voltageInput  = "P9_yy"
triggerInput  = "P9_zz"
clearFlipFlop = "P9_ww"

list_adc = [0]*4096

ADC.setup()

GPIO.setup(capDischarge, GPIO.OUT)
GPIO.output(capDischarge, GPIO.LOW)

GPIO.setup(clearFlipFlop, GPIO.OUT)
GPIO.output(clearFlipFlop, GPIO.HIGH)

GPIO.setup(triggerInput, GPIO.IN)

client = StrictRedis(host = "127.0.0.1")

while(True):
    while(not(GPIO.input(triggerInput))): # Waiting to receive start pulse
        pass

    capDischarge_sleep = float(client.get("capDischarge_sleep"))

    adc_value = int(ADC.read(voltageInput)*4096)
    list_adc[adc_value] += 1

    GPIO.output(capDischarge, GPIO.HIGH)
    GPIO.output(clearFlipFlop, GPIO.LOW)

    sleep(capDischarge_sleep)

    client.set("GammaEnergy:List", list_adc)

    GPIO.output(capDischarge, GPIO.LOW)
    GPIO.output(clearFlipFlop, GPIO.HIGH)
