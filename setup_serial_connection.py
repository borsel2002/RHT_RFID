import serial
import os

def setup_serial_connection():
    try:
        ser = serial.Serial('/dev/tty/USB0', baudrate=9600, timeout=None)
        time.sleep(0.01)  # Wait for the connection to establish
        return ser
    except serial.SerialException as e:
        messagebox.showerror("Error", f"Could not connect to serial device: {e}")
        return None