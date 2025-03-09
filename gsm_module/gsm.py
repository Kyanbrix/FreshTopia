import serial
from serial import Serial

ser = Serial('/dev/ttyS0',baudrate=115200,timeout=1)

def send_command(command):
     ser.write(command + "\r\n".encode())

     while ser.in_waiting:
          print(ser.readline().decode().strip())


send_command("AT")  # Check communication
send_command("AT+CSQ")  # Check signal quality
send_command("AT+CREG?")  # Check network registration