import configparser
import subprocess
import time
import signal
import requests

# 建立 ConfigParser
config = configparser.ConfigParser()
config.read('config.ini')

ngrok = config['ngrok']['path']
port = config['ngrok']['port']
protocol = config['ngrok']['protocol']
auth = config['ngrok']['auth']
apiToken = config['ngrok']['api-token']
curProc = None

def handler(signum, frame):
    if curProc:
        curProc.terminate()
    exit(1)
signal.signal(signal.SIGINT, handler)

def queryTunnelsInfo():
    url = 'https://api.ngrok.com/tunnels'
    headers = {
        'Authorization': f'Bearer {apiToken}',
        'Ngrok-Version': '2'
    }
    response = requests.get(
        url,
        headers=headers,
        timeout=30
    )
    result = response.json()
    print(result)


try:
    curProc = subprocess.Popen([ngrok, "authtoken", auth], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    curProc.wait()

    curProc = subprocess.Popen([ngrok, protocol, port], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, text=True)
    time.sleep(3)
    queryTunnelsInfo()

    curProc.wait()
finally:
    if curProc:
        curProc.kill()