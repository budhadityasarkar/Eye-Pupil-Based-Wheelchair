import serial
import time




def sendData(dir):
	print("Start")
	# port="/dev/tty.HC-06-DevB" #This will be different for various devices and on windows it will probably be a COM port.
	bluetooth=serial.Serial('COM4', 9600)  # Start communications with the bluetooth unit
	print("Connected")
	bluetooth.flushInput()  # This gives the bluetooth a little kick

	# send 5 groups of data to the bluetooth
	print("Ping")
	d=dir
	if d== "forward":
		i=1
		bluetooth.write(b"BOOP "+str.encode(str(i)))  # These need to be bytes not unicode, plus a number
	elif d== "left":
		i=2
		bluetooth.write(b"BOOP "+str.encode(str(i)))
	elif d== "right":
		i=3
		bluetooth.write(b"BOOP "+str.encode(str(i)))
	elif d== "stop":
		i=4
		bluetooth.write(b"BOOP "+str.encode(str(i)))
	input_data=bluetooth.readline()  # This reads the incoming data. In this particular example it will be the "Hello from Blue" line
	print(input_data.decode('ascii'))  # These are bytes coming in so a decode is needed
	time.sleep(3)  # A pause between bursts
	#bluetooth.close() # Otherwise the connection will remain open until a timeout which ties up the /dev/thingamabob
	#print("Done")
