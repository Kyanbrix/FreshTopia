from serial import Serial

import time
ser = Serial('/dev/ttyS0', baudrate=115200, timeout=1)

def send_sms(text, phone_number):
    ser.write(b'AT+CMGF=1\r\n')
    time.sleep(1)
    ser.write(f'AT+CMGS="{phone_number}"\r\n'.encode())
    time.sleep(1) # Blocking change to async or thread
    ser.write((text + "\x1A".encode()))
    

send_sms('HI POTA','+639777520095')

