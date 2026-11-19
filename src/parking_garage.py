import math
from datetime import datetime
from operator import truediv

try:
    import RPi.GPIO as GPIO
except:
    import mock.GPIO as GPIO

try:
    import SDL_DS3231
except:
    import mock.SDL_DS3231 as SDL_DS3231

class ParkingGarage:

    # Pin number declarations
    INFRARED_PIN1 = 11
    INFRARED_PIN2 = 12
    INFRARED_PIN3 = 13
    SERVO_PIN = 16
    LED_PIN = 18

    def __init__(self):
        # See User Stories #1, #3-5
        GPIO.setmode(GPIO.BOARD) # Set the numbering schema to bord mode
        GPIO.setwarnings(False)
        self.rtc = SDL_DS3231.SDL_DS3231() # Variable not initialize yet (see User Story #3)
        self.servo = None # Variable not initialize yet (see User Story #4)
        self.door_open = None # Variable not initialize yet (see User Story #4)
        self.red_light_on = None # Variable not initialize yet (see User Story #5)

        GPIO.setup(self.INFRARED_PIN1, GPIO.IN)
        GPIO.setup(self.INFRARED_PIN2, GPIO.IN)
        GPIO.setup(self.INFRARED_PIN3, GPIO.IN)

        GPIO.setup(self.SERVO_PIN, GPIO.OUT)
        self.servo = GPIO.PWM(self.SERVO_PIN, 50)
        self.servo.start(5)
        self.door_open = False


    def check_occupancy(self, pin: int) -> bool:
        if pin not in (self.INFRARED_PIN1, self.INFRARED_PIN2, self.INFRARED_PIN3):
            raise ParkingGarageError

        return not GPIO.input(pin)
        # See User Story #1

    def get_number_occupied_spots(self) -> int:
        cnt = 0

        for pin in [self.INFRARED_PIN1, self.INFRARED_PIN2, self.INFRARED_PIN3]:
            if self.check_occupancy(pin):
                cnt+=1

        # See User Story #2
        return cnt

    def calculate_parking_fee(self, entry_time: datetime) -> float:
        now = self.rtc.read_datetime()
        elapsed = now - entry_time
        hours = elapsed.total_seconds() / 3600
        hours_ceil = math.ceil(hours)

        # See User Story #3
        return 2.5*hours_ceil

    def open_garage_door(self) -> None:
        self.servo.ChangeDutyCycle(10)
        self.door_open = True

    def close_garage_door(self) -> None:
        self.servo.ChangeDutyCycle(10)
        self.door_open = False

    def turn_on_red_light(self) -> None:
        # See User Story #5
        pass

    def turn_off_red_light(self) -> None:
        # See User Story #5
        pass

    def manage_red_light(self) -> None:
        # See User Story #6
        pass


    # This method is meant to show you how to release the hardware resources when the program running on real hardware ends.
    def cleanup(self) -> None:
        self.servo.stop() # Stops generating PWM on the pin
        GPIO.cleanup() # Resets every GPIO pin


class ParkingGarageError(Exception):
    pass
