#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import ColorSensor
from pybricks.parameters import Port, Color
from pybricks.tools import wait

class RGBColor():
  """
  RGBカラーを取り扱うクラス。定数とメソッドのみで状態は持たない。
  Colorクラスだとpybricksのクラス名とかぶるのでRGBColorにしている。
  """
  THRESHOLD = 2

  # 各色の基準値。RGBの反射値がこれらの+-THRESHOLD以内なら、その色として扱う。単位は%
  BASE_RED = [24, 4.8, 3]
  BASE_BLUE = [3, 3, 6]
  BASE_YELLOW = [24, 19, 3]
  BASE_BLACK = [1.2, 1.2, 0.6]
  BASE_GRAY = [11, 13, 8]
  BASE_GREEN = [4, 11, 2]

  def __init__(self):
    """Constructor"""
    self.colorSensor = ColorSensor(Port.S3)

  def __parse(self, base, red, green, blue):
    """ RGBの反射値lightValが、baseで指定された色かどうか調べる"""
    if ((base[0] - self.THRESHOLD) <= red   and red   <= (base[0] + self.THRESHOLD)) and \
       ((base[1] - self.THRESHOLD) <= green and green <= (base[1] + self.THRESHOLD)) and \
       ((base[2] - self.THRESHOLD) <= blue  and blue  <= (base[2] + self.THRESHOLD)):
      return True

    return False

  def getColor(self):
    """
    センサーの取得したRGB値を具体的な色に変換する
    """
    (red, green, blue) = self.colorSensor.rgb()
    if self.__parse(self.BASE_RED, red, green, blue):
      return Color.RED
    elif self.__parse(self.BASE_BLUE, red, green, blue):
      return Color.BLUE
    elif self.__parse(self.BASE_YELLOW, red, green, blue):
      return Color.YELLOW
    elif self.__parse(self.BASE_BLACK, red, green, blue):
      return Color.BLACK
    elif self.__parse(self.BASE_GRAY, red, green, blue):
      return Color.BROWN # 本当はグレーなのだが、なぜかColor.GRAYがエラーになるので代用
    elif self.__parse(self.BASE_GREEN, red, green, blue):
      return Color.GREEN
    else:
      return Color.WHITE

if __name__ == "__main__":
  ev3 = EV3Brick()
  rgbColor = RGBColor()

  while True:
    color = rgbColor.getColor()

    ev3.screen.clear()
    if color is Color.BROWN:
      ev3.screen.draw_text(0, 0, "GRAY")
    elif color is Color.RED:
      ev3.screen.draw_text(0, 0, "RED")
    elif color is Color.BLUE:
      ev3.screen.draw_text(0, 0, "BLUE")
    elif color is Color.YELLOW:
      ev3.screen.draw_text(0, 0, "YELLOW")
    elif color is Color.BLACK:
      ev3.screen.draw_text(0, 0, "BLACK")
    elif color is Color.GREEN:
      ev3.screen.draw_text(0, 0, "GREEN")
    elif color is Color.WHITE:
      ev3.screen.draw_text(0, 0, "WHITE")
    else:
      ev3.screen.draw_text(0, 0, "UNKNOWN")

    wait(1000)
  # end of while
