from pynput import keyboard
import pyautogui as pag
import subprocess
import threading

trial = [1]
block = [False]

# starts the recording command for sub kinect for given time
def start_sub(time):
    # sub_cmd = f'"C:\Program Files\Azure Kinect SDK v1.4.1\tools\k4arecorder.exe" --device 0 --external-sync sub -l {time} -r 30 --imu OFF 5stest_sub.mkv'
    sub_cmd = f'k4arecorder.exe --device 0 --external-sync sub -l {time} -r 30 --imu OFF videos\HD01NB-{trial[0]}s.mkv'
    subprocess.call(sub_cmd, shell=True)

# starts the recording command for master kinect for given time
def start_master(time):
    # master_cmd = f'"C:\Program Files\Azure Kinect SDK v1.4.1\tools\k4arecorder.exe" --device 1 --external-sync master -l {time} -r 30 --imu OFF 5stest_master5.mkv'
    master_cmd = f'k4arecorder.exe --device 1 --external-sync master -l {time} -r 30 --imu OFF videos\HD01NB-{trial[0]}m.mkv'
    subprocess.call(master_cmd, shell=True)

def record_5():
    print('Starting 5 second run')
    # creating threads
    t1 = threading.Thread(target=start_sub, args=(5,))
    t2 = threading.Thread(target=start_master, args=(5,))
    # starting thread 1
    t1.start()
    # starting thread 2
    t2.start()
    # pag.click(5, 1075)
    # wait until thread 1 is completely executed
    t1.join()
    # wait until thread 2 is completely executed
    t2.join()
    trial[0] += 1
    print('5 second recording completed')
    block[0] = False

def record_10():
    print('Starting 10 second run')
    # creating threads
    t1 = threading.Thread(target=start_sub, args=(10,))
    t2 = threading.Thread(target=start_master, args=(10,))
    # starting thread 1
    t1.start()
    # starting thread 2
    t2.start()
    pag.click(20, 1060)
    # wait until thread 1 is completely executed
    t1.join()
    # wait until thread 2 is completely executed
    t2.join()
    trial[0] += 1
    print('10 second recording completed')
    block[0] = False

def on_press(key):
    try: 
        if key.char == '5' and not block[0]:
            block[0] = True
            record_5()
        elif key.char == '6' and not block[0]:
            block[0] = True
            record_10()
    except AttributeError:
        print(f'key {key} not a char')
        

def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener
        return False

with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()