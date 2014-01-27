import sqlite3
import time
import urllib.request
import urllib.parse
import json
import platform
import simplecrypto
from socket import gethostname
from os.path import realpath

script_path = realpath(__file__)
script_base = script_path[:script_path.rfind('/')+1]

database_file = script_base + 'temperatures.db'
public_key_path = script_base + 'balder.pub'
api_url = 'http://temperature.certexp.com/deliver/temperature'

db_connection = sqlite3.connect(database_file)
db_cursor = db_connection.cursor()
time_script_started = time.time()

def get_temperatures():
	temperatures = {}
	for row in db_cursor.execute('SELECT sensor, temperature, timestamp FROM temperatures ORDER BY sensor ASC'):
		if row[0] in temperatures:
			temperatures[row[0]].append({
				'temperature' : row[1],
				'timestamp' : row[2]})
		else:
			temperatures[row[0]] = [{
				'temperature' : row[1],
				'timestamp' : row[2]}]
	return temperatures

def clean_temperatures():	
	db_cursor.execute('DELETE FROM temperatures WHERE timestamp < ?', (time_script_started,))
	db_connection.commit()
	
def get_messages():
	messages = []
	
	# the messages table might not exists as it's not much used, create temporary table if missing.
	db_cursor.execute("CREATE TABLE IF NOT EXISTS messages (message TEXT, timestamp INTEGER)")
	for row in db_cursor.execute('SELECT message, timestamp FROM messages'):
		messages.append({
			'message' : row[0],
			'timestamp' : row[1]})
	return messages
	
def clean_messages():	
	db_cursor.execute('DELETE FROM messages WHERE timestamp < ?', (time_script_started,))
	db_connection.commit()
	
def add_message(m):
	db_cursor.execute("CREATE TABLE IF NOT EXISTS messages (message TEXT, timestamp INTEGER)")
	db_cursor.execute("INSERT INTO messages (message, timestamp) VALUES (?, ?)", (m, time.time()))
	db_connection.commit()
	
def get_systeminfo():
	systeminfo = {}
	systeminfo['hostname'] = gethostname()
	systeminfo['platform'] = platform.platform()
	systeminfo['version'] = platform.version()
	return systeminfo


data = json.dumps({
	'temperatures' : get_temperatures(),
	'messages' : get_messages(),
	'systeminfo' : get_systeminfo()})
	
encrypted_data_as_json = simplecrypto.encrypt_data(simplecrypto.import_key(public_key_path), data)

# Build POST variable 'data'
params = urllib.parse.urlencode({'data': encrypted_data_as_json }).encode('UTF8') 
try:
	handle = urllib.request.urlopen(api_url, params)
	clean_temperatures()
	clean_messages()
except urllib.error.HTTPError as e:
	add_message('Unable to deliver payload, error: ' + repr(e.code))
	print(e.code)
db_connection.close()
