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
from main import LineTraceCar

# EV3の固有デバイス初期化
leftMotor = Motor(Port.C)
rightMotor = Motor(Port.B)
sonicSensor = UltrasonicSensor(Port.S4)

class LineTraceCar2(LineTraceCar):
  """
  ライントレースと車庫入れを行うクラス2
  """
  DISTANCE_THRESHOLD = 20
  DISTANCE_SHORT_MM = 200
  DISTANCE_MEDIUM_MM = 240

  def measureBlock(self):
    """BLOCKまでの処理を測定する"""
    distance = sonicSensor.distance()
    if (self.DISTANCE_SHORT_MM - self.DISTANCE_THRESHOLD) <= distance and distance <= (self.DISTANCE_SHORT_MM + self.DISTANCE_THRESHOLD):
      return Color.BLUE
    elif (self.DISTANCE_MEDIUM_MM - self.DISTANCE_THRESHOLD) <= distance and distance <= (self.DISTANCE_MEDIUM_MM + self.DISTANCE_THRESHOLD):
      return Color.YELLOW
    else:
      # YELLOW以上に長ければ全てREDとみなす
      return Color.RED

  def trace(self):
    # RGBColorクラスの初期化
    rgbColor = RGBColor()

    self.__initMotor()

    greenFlag = False
    garageColor = None

    # ラインをトレースして走る
    while True:
      # 色の取得と判定
      gotColor = rgbColor.getColor()

      if gotColor is Color.BLACK: # 黒
        if greenFlag == True:
          # 緑から黒に変わった位置で距離を測定
          leftMotor.stop()
          rightMotor.stop()
          garageColor = self.measureBlock()

        # 右回転
        self.__run(self.HIGH_SPEED_DEG_S, self.LOW_SPEED_DEG_S)

      elif gotColor is Color.WHITE: # 白
        # 左回転
      	self.__run(self.LOW_SPEED_DEG_S, self.HIGH_SPEED_DEG_S)

      elif gotColor is Color.GREEN: # 緑
        # 線としては黒と同じ扱いなので右回転
        self.__run(self.HIGH_SPEED_DEG_S, self.LOW_SPEED_DEG_S)
        greenFlag = True

      else:
        if garageColor == None or gotColor is not garageColor:
          # 駐車位置の色の測定前にその他の色を検知するか、駐車位置の色の判明後でも他の色を検知したら黒扱いで右回転
      	  self.__run(self.HIGH_SPEED_DEG_S, self.LOW_SPEED_DEG_S)
        else:
          # 駐車位置の色が判明して、かつその色ならbreak
          break

    # end of while

    # モーターを停止
    self.__initMotor()
    leftMotor.stop()
    rightMotor.stop()
    print("trace MotorStop")

if __name__ == "__main__":
  car = LineTraceCar2()

  # ライントレース開始
  car.trace()
  # 駐車する
  car.garageIn()
