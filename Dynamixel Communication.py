import serial
import time
import threading
import sys
import select

# Establish a serial connection with the Arduino
arduino = serial.Serial(port='/dev/tty.usbmodem1101', baudrate=57600, timeout=.1)

stop_serial_listening = False

def send_angles(theta_R, theta_W, theta_G1, theta_G2):
    # Format the angles as a comma-separated string
    angles = f"{theta_R},{theta_W},{theta_G1},{theta_G2}"
    
    # Send the data to the Arduino
    arduino.write(bytes(angles, 'utf-8'))

def listen_for_serial():
    global stop_serial_listening
    while True:
        if not stop_serial_listening:
            data = arduino.readline().decode('utf-8').strip()
            if data:
                print(f"Controller: {data}")
        time.sleep(0.1)  # Adjust the sleep time to your needs

def check_for_enter_key():
    global stop_serial_listening
    while True:
        # Check if Enter key is pressed
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            user_input = input()  # This will be empty if just Enter is pressed
            if user_input == "":
                stop_serial_listening = True
                get_user_input()
                stop_serial_listening = False

def get_user_input():
    global stop_serial_listening
    try:
        # Get user inputs
        theta_R = float(input("Enter theta_R: "))
        theta_W = float(input("Enter theta_W: "))
        theta_G1 = float(input("Enter theta_G1: "))
        theta_G2 = float(input("Enter theta_G2: "))

        # Send the angles to the Arduino
        send_angles(theta_R, theta_W, theta_G1, theta_G2)
    except ValueError:
        print("Invalid input. Please enter numerical values.")

# Create a thread for listening to serial data
serial_thread = threading.Thread(target=listen_for_serial)
serial_thread.daemon = True  # This ensures the thread will close when the main program exits
serial_thread.start()

# Create a thread for checking the Enter key press
input_thread = threading.Thread(target=check_for_enter_key)
input_thread.daemon = True
input_thread.start()

# Keep the main thread alive
while True:
    time.sleep(1)
