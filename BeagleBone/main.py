from Adafruit_BBIO import GPIO, ADC
from redis import *
from time import sleep

#capDischarge  = "P9_xx" # Usar o mesmo pino do clear do FlipFLop ???
voltageInput  = "P9_33"
triggerInput  = "P8_15"
clearFlipFlop = "P8_12"

list_adc = [0]*4096

ADC.setup()

#GPIO.setup(capDischarge, GPIO.OUT)
#GPIO.output(capDischarge, GPIO.LOW)

GPIO.setup(clearFlipFlop, GPIO.OUT)
GPIO.output(clearFlipFlop, GPIO.HIGH)

GPIO.setup(triggerInput, GPIO.IN)

client = StrictRedis(host = "127.0.0.1")
client.lpush("gamma_energy", 0, 0)

for i in range(4096):
    client.lpush("gamma_energy_total")

while(True):
    while(not(GPIO.input(triggerInput))): # Waiting to receive start pulse
        pass

    capDischarge_sleep = float(client.get("capacitor_sleep"))

    adc_value = int(ADC.read(voltageInput)*4096)
    list_adc[adc_value] += 1

#    GPIO.output(capDischarge, GPIO.HIGH)
    GPIO.output(clearFlipFlop, GPIO.LOW)

    sleep(capDischarge_sleep)

    client.lset("gamma_energy", 0, adc_value)
    client.lset("gamma_energy", 1, list_adc[adc_value])


    client.lset("gamma_energy_total", adc_value, list_adc[adc_value])

#    GPIO.output(capDischarge, GPIO.LOW)
    GPIO.output(clearFlipFlop, GPIO.HIGH)

