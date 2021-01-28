from time import sleep
from vrzero.hmd import OpenHMD

hmd = OpenHMD()

while True:
    hmd.poll()
    print(hmd.rotation)
    sleep(0.01)