# 获取树莓派 CPU温度 内存使用率 CPU使用率

import os

# CPU温度
def getCpuTemp():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n",""))

# CPU使用率
def getCpuUsage():
    return(str(os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip()))

# RAM信息
def getRAMinfo():
    p = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i==2:
            return(line.split()[1:4])

# 内存使用率
def getRamUsage():
    RAM_stats = getRAMinfo()
    return round(int(RAM_stats[1]) / int(RAM_stats[0])*100,1)