# MotorControl.py
# TB6612FNG电机驱动
# 电机控制

import RPi.GPIO as GPIO
'''
self.GPIO_PWM
self.GPIO_IN1
self.GPIO_IN2
self.freq

self.last_pwm
self.pwm
'''
class Motor(object):
    
    def __init__(self, GPIO_PWM, GPIO_IN1, GPIO_IN2, freq=300) -> None:
        super().__init__()
        self.GPIO_PWM = GPIO_PWM
        self.GPIO_IN1 = GPIO_IN1
        self.GPIO_IN2 = GPIO_IN2
        self.freq = freq

        GPIO.setmode(GPIO.BCM)
        #GPIO.setwarnings(False)
        
        GPIO.setup(self.GPIO_PWM, GPIO.OUT)
        GPIO.setup(self.GPIO_IN1, GPIO.OUT)
        GPIO.setup(self.GPIO_IN2, GPIO.OUT)

        self.pwm = GPIO.PWM(self.GPIO_PWM, self.freq)
        self.last_pwm = 0
        self.pwm.start(self.last_pwm)

    ''' 静态方法 TB6612FNG的STBY引脚
    1. GPIO_STBY int BCM编码号
    2. status bool 为true则TB6612FNG工作，反之待机 默认为false
    '''
    @staticmethod
    def standby(GPIO_STBY,status=False):
        GPIO.setmode(GPIO.BCM)
        #GPIO.setwarnings(False)
        if status:
            GPIO.setup(status, GPIO.OUT)
            GPIO.output(status, True)
        else:
            GPIO.output(status, False)
    
    ''' 设置PWM占空比
    1. dc 占空比 [0,100]
    '''
    def __setPWM(self, dc):
        if dc != self.last_pwm:
            self.pwm.ChangeDutyCycle(dc)
            self.last_pwm = dc


    ''' 启动
    1. speed int 范围[-100,100] 正数则正转，负数则反转
    '''
    def run(self, speed):
        if(speed>=0):
            GPIO.output(self.GPIO_IN1, False)
            GPIO.output(self.GPIO_IN2, True)
            self.__setPWM(speed)
        else:
            GPIO.output(self.GPIO_IN1, True)
            GPIO.output(self.GPIO_IN2, False)
            self.__setPWM(-speed)
        

    '''停止'''
    def stop(self):
        GPIO.output(self.GPIO_IN1, False)
        GPIO.output(self.GPIO_IN2, False)
        self.__setPWM(0)


    def cleanup(self):
        self.stop()
        self.pwm.stop()
