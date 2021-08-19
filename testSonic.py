#!/usr/bin/env pybricks-micropython
# pybricksのreferenceはここ: https://docs.pybricks.com/en/stable/index.html
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import UltrasonicSensor
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog

sonicSensor = UltrasonicSensor(Port.S4)
ev3 = EV3Brick()

while True:
  dist = sonicSensor.distance()
  ev3.screen.clear()
  message = "dist:" + str(dist) + "mm"
  ev3.screen.draw_text(0, 0, message)
  wait(1000)