# temperatures

## To Do
- [x] Read temperatures and save to local database
- [ ] Design "protocol" (ecrypted JSON)
- [ ] Create API for webserver
- [ ] Update webserver through API
- [ ] Update central database periodically with high res data

## client-scripts
Scripts running on the client side

#### getTemp.py
Looks for sensors and inserts sensor-id, current timestamp and current temperature into an SQLite db.
Set up a crontab to run it.
