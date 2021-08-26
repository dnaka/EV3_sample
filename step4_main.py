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
  SPEED = [240, 80]   # 通常
  SPEED2 = [120, 60]  # 低速
  SPEED3 = [240, 180] # 高速

  FLAG_NORMAL = 0
  FLAG_GREEN  = 1
  FLAG_BLUE   = 2

  def waitStart(self, dist_min_mm, dist_max_mm):
    """dist_min から dist_maxの間に物体を検知し続けている間無限ループする"""
    while True:
      if not self.__isDetectObject(dist_min_mm, dist_max_mm):
        break
    # end of while

  def trace(self):
    """ライントレースのメイン処理"""
    # RGBColorクラスの初期化
    rgbColor = RGBColor()
    self.__initMotor()

    flag = self.FLAG_NORMAL
    speed = self.SPEED

    # ラインをトレースして走る
    while True:
      # 色の取得と判定
      gotColor = rgbColor.getColor()

      if gotColor is Color.BLACK:
        if flag == self.FLAG_GREEN:
          # 緑の後に黒を検出したら90°コーナーを曲がる
          self.__turnLastCurve()
          flag = self.FLAG_NORMAL
          # あとは直線なので、高速度設定
          speed = self.SPEED3
        elif flag == self.FLAG_BLUE:
          # 青から黒を検出したら、車庫入れのために方向を整えたいので速度を落とす
          speed = self.SPEED2
          self.__run(speed[1], speed[0])
          flag = self.FLAG_NORMAL

        else:
          # 右旋回
          self.__run(speed[1], speed[0])

      elif gotColor is Color.WHITE: # 白
        # 左回転
      	self.__run(speed[0], speed[1])

      elif gotColor is Color.GREEN: # 緑
        self.__run(speed[1], speed[0])
        flag = self.FLAG_GREEN

      elif gotColor is Color.BLUE: # 青
        self.__run(speed[1], speed[0])
        flag = self.FLAG_BLUE

      elif gotColor is Color.YELLOW:
        break

      else:
        # 白以外のその他の色も右回転
      	self.__run(speed[1], speed[0])
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
    self.__turn(-90)

    # 20cm前進
    speed = self.__calcDegree(20)
    leftMotor.run_angle(speed, speed, wait=False)
    rightMotor.run_angle(speed, speed, wait=True)

    leftMotor.brake()
    rightMotor.brake()
    print("garageIn() MotorStop")

  def __initMotor(self):
    leftMotor.brake()
    rightMotor.brake()

    leftMotor.reset_angle(0)
    rightMotor.reset_angle(0)

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
    """緑から黒を検出したらよばれる、90度カーブを曲がるための制御関数"""
    # 4cm直進
    speed = self.__calcDegree(4)
    leftMotor.run_angle(speed * 2, speed, wait=False)
    rightMotor.run_angle(speed * 2, speed, wait=True)

    self.__turn(90)

  def __calcDegree(self, run_distance_cm):
    """走行距離を入力すると、必要な角度を計算する"""
    # 走行距離yは y = 5.6(cm タイヤ直径) * 3.14 * deg / 360 で計算できるので、これを変形してdegを計算する
    return run_distance_cm * 20.47

  def __turn(self, deg):
    """指定された角度だけ曲がる。＋なら右旋回、-の角度なら左旋回する"""
    # 1sで指定された角度だけ信地旋回するために必要な速度
    # 機体のトレッド=回転半径が約10cmなので、20 * 3.14 * deg / 360がタイヤの移動距離。
    # これに走行距離yを計算する式y = 5.6(cm タイヤ直径) * 3.14 * deg_s / 360 を適用すると、20/5.6 * deg

    #speed = 3.6 * deg
    speed = 4.3 * deg # 速度が上がると曲がりきれないようなので係数をあげる

    if deg > 0:
      # +なら右旋回＝左モーターを回す
      leftMotor.run_angle(speed, speed, wait=True)
      rightMotor.hold()

    else:
      # -なら左旋回＝右モーターを回す degが負値なので−する
      leftMotor.hold()
      rightMotor.run_angle(-speed, -speed, wait=True)

  def __isDetectObject(self, dist_min, dist_max):
    """指定された範囲に物体を検出したらTrueを返す"""
    dist = sonicSensor.distance()
    if (dist_min < dist and dist < dist_max):
      return True
    return False

if __name__ == "__main__":
  car = LineTraceCar()

  # start処理
  car.waitStart(50, 200)

  # ライントレース開始
  car.trace()

  # 駐車する
  car.garageIn()
