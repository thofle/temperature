#
# Based on article from Adafruit by Simon Monk
# http://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/software
#

import sqlite3
import time
import glob

base_dir = '/sys/bus/w1/devices/'
device_file = '/w1_slave'
database_file = 'temperatures.db'

def get_sensors():
  sensors = []
  for sensor_path in glob.glob(base_dir + '28*'):
    sensors.append(sensor_path.strip()[-15:])
  return sensors
  
def get_temperature(s):
  lines = read_file_raw(base_dir + s + device_file)
  while lines[0].strip()[-3:] != 'YES':
    time.sleep(0.2)
    lines = read_file_raw(base_dir + s + device_file)
  equals_pos = lines[1].find('t=')
  if equals_pos != -1:
    temp_string = lines[1][equals_pos+2:]
    return repr(float(temp_string) / 1000.0)

def read_file_raw(f):
  file = open(f, 'r')
  lines = file.readlines()
  file.close()
  return lines

def insert_temperature_into_db(s, t):
  conn = sqlite3.connect(database_file)
  cur = conn.cursor()
  cur.execute("CREATE TABLE IF NOT EXISTS temperatures (sensor TEXT, timestamp INTEGER, temperature REAL)")
  cur.execute("INSERT INTO temperatures (sensor, timestamp, temperature) VALUES (?, ?, ?)", (s, time.time(), t))
  conn.commit()
  conn.close()
  
def insert_message_into_db(m):
  conn = sqlite3.connect(database_file)
  cur = conn.cursor()
  cur.execute("CREATE TABLE IF NOT EXISTS messages (message TEXT, timestamp INTEGER)")
  cur.execute("INSERT INTO messages (message, timestamp) VALUES (?, ?, ?)", (m, time.time()))
  conn.commit()
  conn.close()
  

for sensor in get_sensors():
  temperature = get_temperature(sensor)
  
  # Temperature should not be 85, this seems to be a sensor bug, retry.
  if temperature == 85:
    temperature = get_temperature(sensor) 
  
  if temperature == 85:
    insert_message_into_db('Unable to read temperature from ' + sensor)
  else:
    insert_temperature_into_db(sensor, temperature)
