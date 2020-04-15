from calliope_mini import *
import radio

IS_ALICE = False
    # https://github.com/calliope-mini/calliope-mini-micropython/blob/master/docs/radio.rst
LOW_POWER = 1
HIGH_POWER = 7
DEFAULT_CHANNEL = 7
EMERGENCY_CHANNEL = 12
CHECK_CHANNEL = 20

MAX_EPOCHS = 3
# this would be replaced with random numbers!
if IS_ALICE:
    SECRET = 10
    DELTA_FOR_NEW_BEACON = 1
else: #it´s Bob
    SECRET = 50
    DELTA_FOR_NEW_BEACON = 1


class Person():
    def __init__(self):
        self.beacons_from_others = [[]]
        self.my_beacons = []
        self.my_beacons.insert(0, SECRET)
        self.beacons_from_hospital = []

    def create_next_beacon(self):
        return int(self.my_beacons[0]) + DELTA_FOR_NEW_BEACON
    
    def update_my_beacon(self):
        self.my_beacons.insert(0, self.create_next_beacon())
        if len(self.my_beacons) > MAX_EPOCHS:
            self.my_beacons.pop()
    
    def next_epoch(self):
        self.update_my_beacon()
        self.beacons_from_others.insert(0, [])
        if len(self.beacons_from_others) > MAX_EPOCHS:
            self.beacons_from_others.pop()
    
    def add_beacons_from_contact(self):
        received_beacon = radio.receive()
        if received_beacon != None:
            led.set_colors(0, 0, 255)
            sleep(1000)
            led.set_colors(0, 0, 0)
            self.beacons_from_others[0].append(received_beacon)

    def send_my_beacon(self):
        radio.send(str(self.my_beacons[0]))
    
    def send_beacons_sent(self):
        for i in self.my_beacons:
            display.scroll(str(i))
            radio.send(str(i))
    
    def check_with_hospital(self):
        is_at_risk = False
        infected_beacon = radio.receive()
        while infected_beacon != None:
            display.scroll(infected_beacon)
            for t in self.beacons_from_others:
                if infected_beacon in t:
                    led.set_colors(255, 0, 0)
                    sleep(500)
                    is_at_risk = True
                else:
                    led.set_colors(0, 255, 0)
                    sleep(100)
            infected_beacon = radio.receive()
            
		if is_at_risk:
			display.scroll('Stay at home')
		else:
			display.scroll('All clear')
        led.set_colors(0, 0, 0)
            
def behave_as_person():
    def check_if_buttons_pressed():
        if button_a.was_pressed():
            display.scroll('To hospital')
            radio.config(power=HIGH_POWER, 
                         channel=EMERGENCY_CHANNEL)
            myself.send_beacons_sent()
            radio.config(power=LOW_POWER,
                         channel=DEFAULT_CHANNEL)
            
        if button_b.was_pressed():
            # check with hospital
            radio.config(power=HIGH_POWER,
                         channel=CHECK_CHANNEL,
                         queue=10)
            display.scroll('???')
            myself.check_with_hospital()
    
            #radio.config(power=LOW_POWER,
            #             channel=DEFAULT_CHANNEL)


    radio.on()
    radio.config(power=LOW_POWER,
                 channel=DEFAULT_CHANNEL)
    
    myself = Person()
    epoch = 0
    
    while epoch < MAX_EPOCHS:
        # Upload/send
        display.show(Image.ARROW_N)
        myself.send_my_beacon()
        led.set_colors(0, 0, 255)
        display.scroll('Sent ' + str(myself.my_beacons[0]))
        led.set_colors(0, 0, 0)
        
        # Download/receive
        display.show(Image.ARROW_S)
        myself.add_beacons_from_contact()
        display.scroll('Received ' + str(myself.beacons_from_others[0]))
        display.clear()
    
        display.scroll('Epoch ' + str(epoch))
        myself.next_epoch()
        display.scroll('OK')

        epoch += 1
    
    while True:
        check_if_buttons_pressed()


behave_as_person()
