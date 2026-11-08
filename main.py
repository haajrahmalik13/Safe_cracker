# Raspberry Pi Safe Lock
# Program by: Haajrah Malik
#
# Set a four-digit code using numbers 1–4.
# Enter it with the buttons to toggle the simulated lock.
# Three incorrect attempts trigger the sealed state.
# Enter the master code to restart.

from gpiozero import LED, Button
from time import sleep

# BCM GPIO numbering
button1 = Button(pin=2, bounce_time=0.05)
button2 = Button(pin=3, bounce_time=0.05)
button3 = Button(pin=4, bounce_time=0.05)
button4 = Button(pin=17, bounce_time=0.05)

green_led = LED(27)
red_led = LED(22)
yellow_led = LED(10)
yellow_led2 = LED(9)

leds = (green_led, red_led, yellow_led, yellow_led2)

MASTER_CODE = "1234321"
run_program = True
sequence = ""


def leds_on():
    for led in leds:
        led.on()


def leds_off():
    for led in leds:
        led.off()


def valid_password(text):
    if len(text) != 4:
        return False

    for char in text:
        if char not in "1234":
            return False

    return True


def one_pressed():
    global sequence
    sequence += "1"
    green_led.on()


def two_pressed():
    global sequence
    sequence += "2"
    red_led.on()


def three_pressed():
    global sequence
    sequence += "3"
    yellow_led.on()


def four_pressed():
    global sequence
    sequence += "4"
    yellow_led2.on()


def unlocked_lights():
    leds_on()
    sleep(3)
    leds_off()


def locked_lights():
    for repeat in range(2):
        leds_on()
        sleep(0.5)
        leds_off()
        sleep(0.5)


def error_lights():
    for repeat in range(3):
        leds_on()
        sleep(0.15)
        leds_off()
        sleep(0.15)


def sealed_lights():
    for repeat in range(10):
        leds_on()
        sleep(0.1)
        leds_off()
        sleep(0.1)


button1.when_pressed = one_pressed
button2.when_pressed = two_pressed
button3.when_pressed = three_pressed
button4.when_pressed = four_pressed

button1.when_released = leds_off
button2.when_released = leds_off
button3.when_released = leds_off
button4.when_released = leds_off

while run_program:
    password = ""

    while not valid_password(password):
        password = input("Set a 4 digit password with numbers 1-4 only: ")

    print("The code is set! Safe is locked.")

    locked = True
    attempts = 0
    sequence = ""

    while attempts < 3:
        if len(sequence) == 4:
            if sequence == password:
                attempts = 0
                if locked:
                    locked = False
                    unlocked_lights()
                else:
                    locked = True
                    locked_lights()
            else:
                attempts += 1
                error_lights()
            sequence = ""
        sleep(0.01)

    sealed_lights()
    print(
        "The safe has been sealed. Enter the master code to restart, "
        "or the program will exit"
    )

    sequence = ""
    while len(sequence) < 7:
        sleep(0.01)

    if sequence != MASTER_CODE:
        run_program = False

print("Program has ended")
