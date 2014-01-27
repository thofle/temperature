# temperatures

## Requisites
- Raspberry Pi or similar
- w1-gpio & w1-therm
- DS18B20 sensor(s)
- Python3

## Client installation

### Add modules
<pre><code>sudo echo w1-gpio >> /etc/modules
sudo echo w1-therm >> /etc/modules</code></pre>

### Install requirements

#### Python3-dev
You need the python3-dev package to compile PyCrypto
<pre><code>sudo apt-get install python3-dev</code></pre>

#### PyCrypto
Get the latest version from https://www.dlitz.net/software/pycrypto/

Note: If you're building on a Raspberry Pi or any other low powered device it may seem like it hangs on "Skipping implicit fixer: set_literal". Give it some time, my Pi used about 5 minutes on this step.
<pre><code>wget http://ftp.dlitz.net/pub/dlitz/crypto/pycrypto/pycrypto-2.6.1.tar.gz
tar xvf pycrypto-2.6.1.tar.gz
cd pycrypto-2.6.1/

sudo python3 setup.py build
sudo python3 setup.py install</code></pre>

Now you can clean up and remove the <code>pycrypto-2.6.1</code>-folder

### Copy scripts
Find a nice place for them...

### Set up crontab
I have register_temperatures.py fire every minute and upload_temperatures.py fire every 5 minutes.
<pre><code>* * * * * python3 /full/path/to/scripts/register_temperature.py
*/5 * * * * python3 /full/path/to/scripts/upload_temperatures.py</code></pre>
