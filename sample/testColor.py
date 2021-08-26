#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import ColorSensor
from pybricks.parameters import Port, Color
from pybricks.tools import wait, DataLog

"""
色センサーの確認用コード
"""
colorSensor = ColorSensor(Port.S3)
ev3 = EV3Brick()

# ログファイル指定
#data = DataLog('R', 'G', 'B', append=True)

while True:
  (r, g, b) = colorSensor.rgb()
  ev3.screen.clear()
  message = "R:" + str(r) + " G:" + str(g) + " B:" + str(b) 
  ev3.screen.draw_text(0, 0, message)

  #data.log(r, g, b)
  wait(1000)
