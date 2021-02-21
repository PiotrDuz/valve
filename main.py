import time

from python import SensorFactory, MotorController, PositionCalibrator, ValveController
from python.position import PositionCalculator

if __name__ == '__main__':
    hall = SensorFactory.getInstance().getHallSensor()
    motor = MotorController.getInstance()
    calc = PositionCalculator.getInstance()
    calibrator = PositionCalibrator.getInstance()
    valve = ValveController.getInstance()
    #
    print("Pres Enter to start")
    val = input("2- open, 1- close, 0- claibrate, 3- setPosition")
    if val == "2":
        motor.setDirectionToOpen()
        motor.turnOn()
        savedTime = time.time() * 1000
        while (time.time() * 1000 - savedTime < 8000):
            print(hall.getValue())
            print(calc.getPosition())
            print("--")
            time.sleep(0.1)
        motor.turnOff()
    if val == "1":
        motor.setDirectionToClose()
        motor.turnOn()
        savedTime = time.time() * 1000
        while (time.time() * 1000 - savedTime < 8000):
            print(hall.getValue())
            print(calc.getPosition())
            print("--")
            time.sleep(0.1)
        motor.turnOff()
    if val == "0":
        calibrator.calibrate()
    if val == "3":
        pos = input("Provide position..")
        valve.setValvePosition(float(pos))
