from calliope_mini import *
import radio

# https://github.com/calliope-mini/calliope-mini-micropython/blob/master/docs/radio.rst
LOW_POWER = 1
HIGH_POWER = 7
DEFAULT_CHANNEL = 7
EMERGENCY_CHANNEL = 12
CHECK_CHANNEL = 20


class Hospital():
    def __init__(self):
        self.beacons_from_infected = []

    def listen(self):
        received_beacon = radio.receive()
        while received_beacon != None:
            led.set_colors(150, 0, 0)
            display.scroll(received_beacon)
            led.set_colors(0, 0, 0)
            self.beacons_from_infected.append(received_beacon)
            received_beacon = radio.receive()
    
    def answer_checks(self):
        for i in self.beacons_from_infected:
            display.scroll(i)
            radio.send(str(i))

def behave_as_hospital():
    radio.on()
    
    hospital = Hospital()
    
    while True:
        if button_a.was_pressed():
            radio.config(power=HIGH_POWER,
                 channel=EMERGENCY_CHANNEL)
            display.show(Image.ARROW_N)
            led.set_colors(0, 0, 255)
            hospital.listen()
            led.set_colors(0, 0, 0)
            
        if button_b.was_pressed():
            radio.config(power=HIGH_POWER,
                         channel=CHECK_CHANNEL)

            display.show(Image.ARROW_S)
            led.set_colors(155, 155, 155)
            hospital.answer_checks()
            led.set_colors(0, 0, 0)
            

behave_as_hospital()
