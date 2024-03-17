import serial
import threading

def receive_uid(ser, uid_var):
    global uid
    while True:
        data = ser.readline().decode('utf-8').strip().split(',')
        uid, doorName = data[0], data[1]  # Parse UID and door name from serial input
        if uid:
            uid_var.set(uid)
            break