import sqlite3
import time
import glob

base_dir = '/sys/bus/w1/devices/'
device_file = '/w1_slave'

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


def insert_into_db(s, t):
  conn = sqlite3.connect('temperatures.db')
  cur = conn.cursor()

  cur.execute("CREATE TABLE IF NOT EXISTS temperatures (sensor TEXT, timestamp INTEGER, temperature REAL)")
  cur.execute("INSERT INTO temperatures (sensor, timestamp, temperature) VALUES (?, ?, ?)", (s, time.time(), t))
  
  conn.commit()
  conn.close()
  
  
for sensor in get_sensors():
  insert_into_db(sensor, get_temperature(sensor))
