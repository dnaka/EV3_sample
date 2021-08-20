#!/usr/bin/env pybricks-micropython
# pybricksのreferenceはここ: https://docs.pybricks.com/en/stable/index.html
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port
from pybricks.tools import wait

SPEED_DEG_S = 360 # 単位は角速度(一秒間にタイヤが何°回転するか)

leftMotor = Motor(Port.C)
rightMotor = Motor(Port.B)

leftMotor.reset_angle(0)
rightMotor.reset_angle(0)

leftMotor.run(SPEED_DEG_S)
rightMotor.run(SPEED_DEG_S)

# Motor.run()は「次の命令が来るまで」指定した速度で回転させ続ける関数なので、
# waitしないとすぐプログラムが終了してMotorが止まる
wait(10000)
