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

  SPEED = [120, 60]

  FLAG_NORMAL  = 0
  FLAG_GREEN   = 1

  def trace(self):
    # RGBColorクラスの初期化
    rgbColor = RGBColor()
    self.__initMotor()

    flag = self.FLAG_NORMAL

    # ラインをトレースして走る
    while True:
      # 色の取得と判定
      gotColor = rgbColor.getColor()

      if gotColor is Color.BLACK:
        if flag == self.FLAG_GREEN:
          # 緑の後に黒を検出したら90°コーナーを曲がる
          self.__turnLastCurve()
          flag = self.FLAG_NORMAL

        else:
          # 右旋回
          self.__run(self.SPEED[1], self.SPEED[0])

      elif gotColor is Color.WHITE: # 白
        # 左回転
      	self.__run(self.SPEED[0], self.SPEED[1])

      elif gotColor is Color.GREEN: # 緑
        self.__run(self.SPEED[1], self.SPEED[0])
        flag = self.FLAG_GREEN

      elif gotColor is Color.YELLOW:
        break

      else:
        # 白以外のその他の色も右回転
      	self.__run(self.SPEED[1], self.SPEED[0])
    # end of while

    # モーターを停止
    leftMotor.stop()
    rightMotor.stop()
    print("trace MotorStop")

  def garageIn(self):
    """
    車庫入れの実施
    """
    # 少し直進
    self.__initMotor()
    
    speed = self.__calcDegree(10)
    leftMotor.run_angle(speed, speed, wait=False)
    rightMotor.run_angle(speed, speed, wait=True)

    # 90度左旋回
    self.turn(-90)

    # 20cm前進
    speed = self.__calcDegree(20)
    leftMotor.run_angle(speed / 3, speed, wait=False)
    rightMotor.run_angle(speed / 3, speed, wait=True)

    leftMotor.stop()
    rightMotor.stop()
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
      leftMotor.stop()
    else:
      leftMotor.run(l_motor_speed)

    if r_motor_speed == 0:
      rightMotor.stop()
    else:
      rightMotor.run(r_motor_speed)

  def __turnLastCurve(self):
    """緑から黒を検出したらよばれる関数"""
    # 5cm直進
    speed = self.__calcDegree(5)
    leftMotor.run_angle(speed, speed, wait=False)
    rightMotor.run_angle(speed, speed, wait=True)

    self.turn(90)

  def __calcDegree(self, run_distance_cm):
    """走行距離を入力すると、必要な角度を計算する"""
    # 走行距離yは y = 5.6(cm タイヤ直径) * 3.14 * deg / 360 で計算できるので、これを変形してdegを計算する
    return run_distance_cm * 20.47

  def turn(self, deg):
    # 1sで指定された角度だけ信地旋回するために必要な速度
    # 機体のトレッド=回転半径が約10cmなので、20 * 3.14 * deg / 360がタイヤの移動距離。
    # これに走行距離yを計算する式y = 5.6(cm タイヤ直径) * 3.14 * deg_s / 360 を適用すると、20/5.6 * deg
    speed = 3.6 * deg

    if deg > 0:
      # +なら右旋回＝左モーターを回す
      leftMotor.run_angle(speed, speed, wait=True)
      rightMotor.hold()

    else:
      # -なら左旋回＝右モーターを回す degが負値なので−する
      leftMotor.hold()
      rightMotor.run_angle(-speed, -speed, wait=True)

  def __turnX(self, turnDeg):
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
