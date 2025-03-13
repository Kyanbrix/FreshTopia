from serial import Serial

import time


class SMS:

    def __init__(self,serial_port,phone_number):

        self.port = serial_port
        self.phone_number = phone_number

    def send_sms(self,text_msg):        
        ser = Serial(self.port, baudrate=115200, timeout=1)
        ser.write(b'AT+CMGF=1\r\n')
        time.sleep(1)
        ser.write(f'AT+CMGS="{self.phone_number}"\r\n'.encode())
        time.sleep(1)
        ser.write((text_msg + "\x1A".encode()))



