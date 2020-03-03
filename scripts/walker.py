#!/usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan
import time
import Adafruit_PCA9685

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(1)

scan_data = [10,10,10,10,10,10,10]
tm = 0
narrow = 0

def cb_scan(data):
  scan_data[0] = data.ranges[44]
  scan_data[1] = data.ranges[129]
  scan_data[2] = data.ranges[256]
  scan_data[3] = data.ranges[384]
  scan_data[4] = data.ranges[556]
  scan_data[5] = data.ranges[640]
  scan_data[6] = data.ranges[725]

def laser_duty_set( ch_No, laserdata):
  if laserdata < 0.8:
    laserdata = 0.8
  if ch_No == 1 or ch_No == 5:
    if laserdata < 1.0:
      laserdate = 0.8
  duty = ((laserdata - 0.8)/0.8)
  print(100 - duty * 100)
  duty *= 4095
  if duty <= 0:
    duty = 1
  pwm.set_pwm( int(ch_No), int(duty), 0)

if __name__ == '__main__':
  rospy.init_node('walker')
  sub = rospy.Subscriber('scan', LaserScan, cb_scan)
  r = rospy.Rate(10)
  while not rospy.is_shutdown():
    counter = 0
    while counter < 7:
      print('scan_data'),
      print(counter),
      print(':'),
      print(scan_data[counter])
      if counter == 1 or counter == 5:
        safety_distance = 1.6
      else:
        safety_distance = 1.4
      if scan_data[counter] <= safety_distance:
        if narrow == 1 and (counter == 0 or counter == 2):
          pwm.set_pwm(0, 0, 0)
          pwm.set_pwm(2, 0, 0)
        elif narrow == 2 and (counter == 1 or counter == 3):
          pwm.set_pwm(1, 0, 0)
          pwm.set_pwm(3, 0, 0)
        elif narrow == 3 and (counter == 2 or counter == 4):
          pwm.set_pwm(2, 0, 0)
          pwm.set_pwm(4, 0, 0)
        elif narrow == 4 and (counter == 3 or counter == 5):
          pwm.set_pwm(3, 0, 0)
          pwm.set_pwm(5, 0, 0)
        elif narrow == 5 and (counter == 4 or counter == 6):
          pwm.set_pwm(4, 0, 0)
          pwm.set_pwm(6, 0, 0)
        else:
          laser_duty_set(counter, scan_data[counter])
          print('pwm out'),
          print(counter)
      else:
        if counter == 1:
          if scan_data[0] <= 1.2 and scan_data[2] <= 1.2 and tm <= 10:
            narrow = 1
            print('narrow')
          elif narrow == 1:
            narrow = 0
          pwm.set_pwm(counter, 0, 0)
        elif counter == 2:
          if scan_data[1] <= 1.3 and scan_data[3] <= 1.2 and tm <= 10:
            narrow = 2
            print('narrow')
          elif narrow == 2:
            narrow = 0
          pwm.set_pwm(counter, 0, 0)
        elif counter == 3:
          if scan_data[2] <= 1.2 and scan_data[4] <= 1.2 and tm <= 10:
            narrow = 3
            print('narrow')
          elif narrow == 3:
            narrow = 0
          pwm.set_pwm(counter, 0, 0)
        elif counter == 4:
          if scan_data[3] <= 1.2 and scan_data[5] <= 1.3 and tm <= 10:
            narrow = 4
            print('narrow')
          elif narrow == 4:
            narrow = 0
          pwm.set_pwm(counter, 0, 0)
        elif counter == 5:
          if scan_data[4] <= 1.2 and scan_data[6] <= 1.2 and tm <= 10:
            narrow = 5
            print('narrow')
          elif narrow == 5:
            narrow = 0
          pwm.set_pwm(counter, 0, 0)
        else:
          pwm.set_pwm(counter, 0, 0)
      counter += 1
    print('')
    tm += 1
    if tm > 20:
      tm = 0
    r.sleep()

  counter = 0
  while counter < 7:
    pwm.set_pwm(counter, 0, 0)
    counter += 1
