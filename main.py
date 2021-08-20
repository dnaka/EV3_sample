#!/usr/bin/env pybricks-micropython
import sys
sys.path.append("./")

# pybricksのreferenceはここ: https://docs.pybricks.com/en/stable/index.html
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from color import RGBColor

# EV3の固有デバイス初期化
leftMotor = Motor(Port.C)
rightMotor = Motor(Port.B)
sonicSensor = UltrasonicSensor(Port.S4)

class LineTraceCar():
  """
  ライントレースと車庫入れを行うクラス
  """
  # タイヤの速度。ターンする時は片方をLOW、もう片方をHIGHにすると曲がる。単位は角度/s (deg/s)
  # TODO: タイヤの円周を測定してマクロにし、角度 * タイヤ円周で移動距離を計算できると、もう少し制御しやすそう
  BACK_SPEED_DEG_S = 300
  HIGH_SPEED_DEG_S = 200
  MIDDLE_SPEED_DEG_S = 100
  LOW_SPEED_DEG_S= 60

  BLOCK_DISTANCE_MM = 200

  def isDetectObject(self, distance, threshold = 10):
    """引数distanceから前後thresholdの距離で何か発見したらTrueを返す """
    dist = sonicSensor.distance()
    if (distance - threshold) <= dist and dist <= (distance + threshold):
      return True

    return False

  def trace(self):
    # RGBColorクラスの初期化
    rgbColor = RGBColor()
    self.__initMotor()

    # ラインをトレースして走る
    while True:
      # 色の取得と判定
      gotColor = rgbColor.getColor()

      if gotColor is Color.BLACK: # 黒
      	# 右回転
        self.__run(self.HIGH_SPEED_DEG_S, self.LOW_SPEED_DEG_S)

      elif gotColor is Color.WHITE: # 白
        # 左回転
      	self.__run(self.LOW_SPEED_DEG_S, self.HIGH_SPEED_DEG_S)
      else:
        # 白以外のその他の色も右回転
      	self.__run(self.HIGH_SPEED_DEG_S, self.LOW_SPEED_DEG_S)

      if self.isDetectObject(self.BLOCK_DISTANCE_MM):
        # 指定範囲内に障害物を検知したらbreak
        break
    # end of while

    # モーターを停止
    self.__initMotor()
    leftMotor.stop()
    rightMotor.stop()
    print("trace MotorStop")

  def garageIn(self):
    """
    車庫入れの実施
    """
    # 少し直進
    self.__initMotor()
    while leftMotor.angle() < 400:
    	self.__run(self.MIDDLE_SPEED_DEG_S, self.MIDDLE_SPEED_DEG_S)

    # 90度超信地旋回
    self.__turn(90)

    # 後進して止める
    self.__initMotor()
    while rightMotor.angle() > -500:
    	self.__run(-self.BACK_SPEED_DEG_S, -self.BACK_SPEED_DEG_S)

    leftMotor.brake()
    rightMotor.brake()
    print("garageIn() MotorStop")

  def __initMotor(self):
    leftMotor.brake()
    rightMotor.brake()

    leftMotor.reset_angle(0)
    rightMotor.reset_angle(0)

	# モーターを回す
  def __run(self, l_motor_speed, r_motor_speed):
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

  def __turn(self, turnDeg):
    """
    超信地旋回させる。turnDeg > 0なら左旋回（反時計回り), turnDeg < 0なら右旋回(時計回り)
    """
    self.__initMotor()

    if turnDeg > 0:
      # 厳密には、turnDegはモーターの回転角度で車体の角度ではないが、左右がそれぞれ90度回転する＝片方がタイヤ半回転相当のはず。
      # タイヤ半回転で大体90度横を向く、という計算の上での処理になっている。
      while rightMotor.angle() < turnDeg * 2:
      	self.__run(-self.MIDDLE_SPEED_DEG_S, self.MIDDLE_SPEED_DEG_S)

    else:
      while leftMotor.angle() < turnDeg * 2:
      	self.__run(self.MIDDLE_SPEED_DEG_S, -self.MIDDLE_SPEED_DEG_S)

    # TODO: 要検証だが以下のような書き方でもいいかも
    #leftMotor.run_angle(-MIDDLE_SPEED_DEG_S, -turnDeg * 2, Stop.HOLD, False）
    #rightMotor.run_angle(MIDDLE_SPEED_DEG_S, turnDeg * 2, Stop.HOLD, True）

if __name__ == "__main__":
  car = LineTraceCar()

  # ライントレース開始
  car.trace()
  # 駐車する
  car.garageIn()
