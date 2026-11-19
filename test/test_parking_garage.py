from datetime import datetime
from unittest import TestCase
from unittest.mock import patch
from unittest.mock import MagicMock

import mock.GPIO as GPIO
from mock.SDL_DS3231 import SDL_DS3231
from src.parking_garage import ParkingGarage
from src.parking_garage import ParkingGarageError

class TestParkingGarage(TestCase):

    @patch.object(GPIO, "setup")
    def test_setup(self, mock_setup: MagicMock):
        garage = ParkingGarage()

        mock_setup.assert_any_call(garage.INFRARED_PIN1, GPIO.IN)
        mock_setup.assert_any_call(garage.INFRARED_PIN2, GPIO.IN)
        mock_setup.assert_any_call(garage.INFRARED_PIN3, GPIO.IN)

    @patch.object(GPIO, "input")
    def test_check_occupancy_high(self, mock_input: MagicMock):
        mock_input.return_value = GPIO.HIGH

        garage = ParkingGarage()

        self.assertTrue(garage.check_occupancy(11))
        mock_input.assert_called_once_with(11)

    @patch.object(GPIO, "input")
    def test_check_occupancy_low(self, mock_input: MagicMock):
        mock_input.return_value = GPIO.LOW

        garage = ParkingGarage()

        self.assertFalse(garage.check_occupancy(11))
        mock_input.assert_called_once_with(11)