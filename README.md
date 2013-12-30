# temperatures

## Requisites
- Raspberry Pi or similar
- w1-gpio & w1-therm
- DS18B20 sensor(s)

## To Do
- Design "protocol" (ecrypted JSON)
- Create API for webserver
- Update webserver through API
- Update central database periodically with high res data

## client-scripts
Scripts running on the client side

#### getTemp.py
Looks for sensors and inserts sensor-id, current timestamp and current temperature into an SQLite db.
Set up a crontab to run it.
