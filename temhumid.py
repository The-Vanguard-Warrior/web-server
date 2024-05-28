import time
import serial

ser = serial.Serial('/dev/cu.usbmodem21101', 9600)

time.sleep(2)

def temp():
    """
    Get temperature from serial and print it.
    """
    ser.write('t'.encode())
    s = str(ser.readline())

    s = s[2:]

    s = s.split("\\", maxsplit=1)[0]
    return s

def humidity():
    """
    Get humidity from serial and print it.
    """
    ser.write('h'.encode())
    s = str(ser.readline())

    s = s[2:]

    s = s.split("\\", maxsplit=1)[0]
    return s
    

def main():
    """
    Main function to handle user input and call appropriate functions.
    """
    while True:
        temp()
        humidity()
        time.sleep(1)

if __name__ == "__main__":
    main()
