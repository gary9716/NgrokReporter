import configparser
import subprocess
import time
import signal
import threading

# 建立 ConfigParser
config = configparser.ConfigParser()
config.read('config.ini')

ngrok = config['ngrok']['path']
port = config['ngrok']['port']
protocol = config['ngrok']['protocol']
auth = config['ngrok']['auth']
curProc = None

def handler(signum, frame):
    if curProc:
        curProc.terminate()
    exit(1)

signal.signal(signal.SIGINT, handler)

def read_output(pipe, target):
    while True:
        output_line = pipe.readline()
        if output_line:
            target(output_line.strip())
        else:
            break

curProc = subprocess.Popen([ngrok, "authtoken", auth])
curProc.wait()

curProc = subprocess.Popen([ngrok, protocol, port], stdout=subprocess.PIPE, text=True)
stdout_thread = threading.Thread(target=read_output, args=(curProc.stdout, print))
stdout_thread.start()
stdout_thread.join()

#
# while True:
#     curProc.stdout.flush()
#     output_line = curProc.stdout.readline()
#     if output_line:
#         print(output_line.strip())
#     else:
#         break