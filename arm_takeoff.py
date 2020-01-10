from dronekit import connect,VehicleMode,LocationGlobalRelative,APIException
import time
import socket
import exceptions
import math
import argparse

def connectMyCopter():
	
	parser = argparse.ArgumentParser(description='commands')
	parser.add_argument('--connect')
	args = parser.parse_args()

	connection_string = args.connect

	if not connection_string:
		import dronekit_sitl
		sitl = dronekit_sitl.start_default()
		connection_string = sitl.connection_string()

	vehicle = connect(connection_string,wait_ready=True)

	return vehicle

def arm_takeoff(targetheight):
	
	while vehicle.is_armable!=True:
		print("waiting for vehicle to be armable")
		time.sleep(1)
	print("vehicle is now armable")

	vehicle.mode = VehicleMode("GUIDED")
	
	while vehicle.mode != 'GUIDED':
		print("waiting for drone to  enter guided mode")
		time.sleep(1)
	print("vehicle is now in GUIDED Flight mode")

	vehicle.armed = True

	while vehicle.armed!=True:
		print("requesting to arm")
		time.sleep(1)
	print("Vehicle is ARMED")

	vehicle.simple_takeoff(targetheight) ##in meters

	while True:
		print(vehicle.location.global_relative_frame.alt)
		if vehicle.location.global_relative_frame.alt >= .95*targetheight:
			break
		time.sleep(1)

	print("alt reached")
	return None

vehicle = connectMyCopter()
arm_takeoff(10)
