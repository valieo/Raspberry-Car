# CarControl.py
# 控制小车移动 （前进 后退 左转 右转）
# 驱动：TB6612FNG
import RPi.GPIO as GPIO
from MotorControl import Motor
from Distance import Measure

''' 
TB6612FNG 接口
        # STBY
        GPIO_STBY = 27
        # 左边电机
        GPIO_PWMA = 18
        GPIO_AIN1 = 14
        GPIO_AIN2 = 15
        # 右边电机
        GPIO_PWMB = 19
        GPIO_BIN1 = 23
        GPIO_BIN2 = 24

HC-SR04 接口
        GPIO_TRIG = 5
        GPIO_ECHO = 6

小车功能
        1. 微调
        2. 变速
        3. 前进
        4. 后退
        5. 左转
        6. 右转
        7. 停车
        8. 测距
'''


class Car(object):
    def __init__(self) -> None:
        super().__init__()

        '''电机模块'''
        # STBY引脚定义
        self.GPIO_STBY = 27
        GPIO.setmode(GPIO.BCM)
        #GPIO.setwarnings(False)
        GPIO.setup(self.GPIO_STBY, GPIO.OUT)

        # 左右两个电机
        self.motor_left = Motor(18,14,15)
        self.motor_right = Motor(19,23,24)

        # STBY = True  TB6612FNG开始工作
        Motor.standby(self.GPIO_STBY,True)

        # 速度  占空比
        self.motor_speed = 60
        self.motor_left_speed = 60
        self.motor_right_speed = 60
        # 速度系数 用于微调
        self.motor_left_coefficient = 1.0
        self.motor_right_coefficient = 1.0

        '''超声波测距模块'''
        self.measure = Measure(5, 6)


    # 微调 使两个电机转速一致  left=True向左微调 反之向右
    def fineTuning(self, left):
        if left:
            # 向左微调 左边的电机减速 右边的电机加速
            self.motor_left_coefficient -= 0.05
            self.motor_right_coefficient += 0.05
        else:
            # 向右边微调 左边的电机加速 右边的电机减速
            self.motor_left_coefficient += 0.05
            self.motor_right_coefficient -= 0.05

    # 更改速度 [0,100]
    def setSpeed(self, speed):
        if speed>100:
            speed = 100
        if speed<0:
            speed = 0
        self.motor_speed = speed
        self.motor_left_speed = self.motor_left_coefficient * speed
        self.motor_right_speed = self.motor_right_coefficient * speed

    # 前进
    def forward(self):
        self.motor_left.run(self.motor_left_speed)
        self.motor_right.run(self.motor_right_speed)

    # 后退
    def backward(self):
        self.motor_left.run(-self.motor_left_speed)
        self.motor_right.run(-self.motor_right_speed)
    
    # 左转
    def turnLeft(self):
        self.motor_left.run(-self.motor_left_speed)
        self.motor_right.run(self.motor_right_speed)

    # 右转
    def turnRight(self):
        self.motor_left.run(self.motor_left_speed)
        self.motor_right.run(-self.motor_right_speed)

    # 停止
    def stop(self):
        self.motor_left.stop()
        self.motor_right.stop()

    # 测距
    def getDistance(self):
        return self.measure.getDistance()

    def getSpeed(self):
        return self.motor_speed

    # 释放资源
    def cleanup(self):
        self.motor_left.cleanup()
        self.motor_right.cleanup()
        GPIO.cleanup()