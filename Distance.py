# 超声波测距模块 HC-SR04
import RPi.GPIO as GPIO
import time

class Measure(object):

    def __init__(self, GPIO_TRIG, GPIO_ECHO) -> None:
        super().__init__()
        self.GPIO_TRIG = GPIO_TRIG
        self.GPIO_ECHO = GPIO_ECHO

        GPIO.setmode(GPIO.BCM)
        #设置 GPIO 的工作方式 (IN / OUT)
        GPIO.setup(GPIO_TRIG, GPIO.OUT)
        GPIO.setup(GPIO_ECHO, GPIO.IN)


    def getDistance(self):
        # 向Trig引脚发送10us的脉冲信号
        GPIO.output(self.GPIO_TRIG, True)
        time.sleep(0.00001)
        GPIO.output(self.GPIO_TRIG, False)

        # 开始发送超声波的时刻
        while GPIO.input(self.GPIO_ECHO)==0:
            pass
        startTime=time.time()
 
        # 收到返回超声波的时刻
        while GPIO.input(self.GPIO_ECHO)==1:
            pass
        endTime=time.time()

        # 计算距离 距离=(声波的往返时间*声速)/2
        timeDelta = endTime - startTime
        distance = (timeDelta * 34300) / 2
  
        return round(distance,2)