import os
import socket



def send_command(command):
	#OPEN OUTPUT SOCKET ON MAYA
	
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect(("localhost",60965))
	sock.sendall(command.encode("utf-8"))

	response = sock.recv(4096)
	print(response)
	return


while True:
	command = input("...")
	send_command(command)
