from ctypes.wintypes import CHAR
from pynput import keyboard
import pyautogui as pag
import subprocess
import threading
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--name', type=str, default='test', help='output file name (automatically appends the camera and trial number) DEFAULT: test')
parser.add_argument('--five', type=str, default='5', help='hotkey for 5 second run DEFAULT: \'5\'')
parser.add_argument('--ten', type=str, default='6', help='hotkey for 10 second run DEFAULT: \'6\'')
parser.add_argument('-trial', '--trial', type=int, default=1 , help='trial number to start from DEFAULT: 1')
args = parser.parse_args()

values = {'x': 0, 'y': 0, 'block': False}

# starts the recording command for sub kinect for given time
def start_sub(time):
    sub_cmd = f'kinect\k4arecorder.exe --device 0 --external-sync sub -l {time} -r 30 --imu OFF videos\{args.name}-{str(args.trial).zfill(2)}-s.mkv'
    subprocess.call(sub_cmd, shell=True)
    print(f'video saved as videos\{args.name}-{str(args.trial).zfill(2)}-s.mkv')

# starts the recording command for master kinect for given time
def start_master(time):
    master_cmd = f'kinect\k4arecorder.exe --device 1 --external-sync master -l {time} -r 30 --imu OFF videos\{args.name}-{str(args.trial).zfill(2)}-m.mkv'
    subprocess.call(master_cmd, shell=True)
    print(f'video saved as videos\{args.name}-{str(args.trial).zfill(2)}-m.mkv')

def record_5():
    print('Starting 5 second run')
    # creating threads
    t1 = threading.Thread(target=start_sub, args=(5,))
    t2 = threading.Thread(target=start_master, args=(5,))
    # starting thread 1
    t1.start()
    # starting thread 2
    t2.start()
    pag.click(values['x'], values['y'])
    # wait until thread 1 is completely executed
    t1.join()
    # wait until thread 2 is completely executed
    t2.join()
    args.trial += 1
    print('\n5 second recording completed\n')
    values['block'] = False
    print_help()

def record_10():
    print('Starting 10 second run')
    # creating threads
    t1 = threading.Thread(target=start_sub, args=(10,))
    t2 = threading.Thread(target=start_master, args=(10,))
    # starting thread 1
    t1.start()
    # starting thread 2
    t2.start()
    pag.click(values['x'], values['y'])
    # wait until thread 1 is completely executed
    t1.join()
    # wait until thread 2 is completely executed
    t2.join()
    args.trial += 1
    print('\n10 second recording completed\n')
    values['block'] = False
    print_help()

def print_help():
    print(f'Press \'{args.five}\' to start a 5 second trial')
    print(f'Press \'{args.ten}\' to start a 10 second trial')
    print('Press Esc to quit this program')
    print()

def on_press(key):
    try: 
        if key.char == args.five and not values['block']:
            values['block'] = True
            record_5()
        elif key.char == args.ten and not values['block']:
            values['block'] = True
            record_10()
    except AttributeError:
        pass
        

def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener
        return False

print('Move mouse to start button and press Crtl + c to save the values')
try:
    while True:
        x, y = pag.position()
        positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
        print(positionStr, end='')
        print('\b' * len(positionStr), end='', flush=True)
        values['x'] = x
        values['y'] = y
except KeyboardInterrupt:
    print('\n')

print_help()
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()