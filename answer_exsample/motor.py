#!/usr/bin/env pybricks-micropython
# pybricksのreferenceはここ: https://docs.pybricks.com/en/stable/index.html
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port
from pybricks.tools import wait

leftMotor = Motor(Port.C)
rightMotor = Motor(Port.B)

def calcDegree(run_distance_cm):
  """走行距離を入力すると、必要な角度を計算する"""
  # 走行距離yは y = 5.5(cm タイヤ直径) * 3.14 * deg / 360 で計算できるので、これを変形してdegを計算する
  return run_distance_cm * 20.85

def run_init():
  leftMotor.brake()
  rightMotor.brake()

  leftMotor.reset_angle(0)
  rightMotor.reset_angle(0)

def run(l_motor_speed, r_motor_speed):
  """
  モーターを回す。引数は左右モーターの角速度(deg/s)
  """
  if l_motor_speed == 0:
    # TODO: hold()でもいいかも
    leftMotor.brake()
  else:
    leftMotor.run(l_motor_speed)

  if r_motor_speed == 0:
    rightMotor.brake()
  else:
    rightMotor.run(r_motor_speed)

# ここから走行
run_init()

# 10cm走る
deg = calcDegree(10)
run(deg, deg)
wait(1000) # 1sで10cm走る角度をdegに設定しているので1s待つ

# 3回ループ
for i in range(0, 3):
  # 左右のタイヤの数値を変えることで蛇行する
  run(300, 100)
  wait(1000) 

  run(100, 300)
  wait(1000)

# 5cm走る
deg = calcDegree(5)
run(deg, deg)
wait(1000)

