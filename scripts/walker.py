#!/usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan
import time
import Adafruit_PCA9685

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(1)

scan_data = [10,10,10,10,10,10,10]

def cb_scan(data):
  scan_data[0] = data.ranges[96]
  scan_data[1] = data.ranges[192]
  scan_data[2] = data.ranges[288]
  scan_data[3] = data.ranges[384]
  scan_data[4] = data.ranges[480]
  scan_data[5] = data.ranges[576]
  scan_data[6] = data.ranges[672]

def laser_duty_set( ch_No, laserdata):
  if laserdata < 0.8:
    laserdata = 0.8
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
      if scan_data[counter] <= 1.4:
        laser_duty_set(counter, scan_data[counter])
        print('pwm out'),
        print(counter)
      else:
        pwm.set_pwm(counter, 0, 0)
      counter += 1
    print('')
    r.sleep()

