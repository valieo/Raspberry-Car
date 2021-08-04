# Start.py
from bottle import get,post,run,request,template
from CarControl import Car
from RaspberryInfo import *

car = Car()

def main(status):
    print("Event: "+status)
    if status == "forward":
        car.forward()
    elif status == "backward":
        car.backward()
    elif status == "turnLeft":
        car.turnLeft()
    elif status == "turnRight":
        car.turnRight()
    elif status == "speedUp":
        car.setSpeed(car.getSpeed() + 5)
    elif status == "slowDown":
        car.setSpeed(car.getSpeed() - 5)
    elif status == "leftFineTuning":
        car.fineTuning(True)
    elif status == "rightFineTuning":
        car.fineTuning(False)
    elif status == "stop":
        car.stop()


# 控制台
@get("/")
def index():
    print("request index.html")
    return template("index.html")

# 控制小车
@post("/cmd")
def cmd():
    adss=request.body.read().decode()
    main(adss)
    return "OK"

# 小车信息
@get("/info")
def info():
    print("Update status Information")
    return template("info.html", speed=car.getSpeed(), distance=car.getDistance(), cpuTemp=getCpuTemp(), cpuUsage=getCpuUsage(), ramUsage=getRamUsage())

run(host='0.0.0.0', port=8088, debug=False)

car.cleanup()