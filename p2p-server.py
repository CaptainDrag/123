import socket
import threading
import os
import sys
import random 

# Constants

BUFFER_SIZE = 1024
fileList = set()
fileLocation = dict()
fileSize = dict()
fileChunk = dict()
CHUNK_SIZE = 1024
# List to store connected clients
connected_clients = []
client_data = {}
server = None
# Function to send a file to a client
def ServerClear(address):
	print(fileList)
	print(fileLocation)
	print(fileSize)
	print(fileChunk)
	for File in fileLocation:
		fileLocation[File].discard(address)
	temp = []
	for File in fileLocation:
		if fileLocation[File] == set():
			temp.append(File)
	for i in temp:
		del fileLocation[i]
	temp = []
	for File in fileList:
		if File not in fileLocation:
			temp.append(File)
	for i in temp:
		fileList.discard(i)
	temp = []
	for File in fileSize:
		if File not in fileLocation:
			temp.append(File)
	for i in temp:
		del fileSize[i]
	temp = []
	for File in fileChunk:
		for chunki in fileChunk[File]:
			fileChunk[File][chunki].discard(address)
	for File in fileChunk:
		if File not in fileLocation:
			temp.append(File)
	for i in temp:
		del fileChunk[i]
	
	print(fileList)
	print(fileLocation)
	print(fileSize)
	print(fileChunk)
			
			
def RR(client_socket, address):
	print("start Register Request")
	while True:	
		try:# Receive the filename and save the file
			numFile = client_socket.recv(BUFFER_SIZE).decode()
			#print("start accepting files2222222222222")
			for i in range(int(numFile)):
				print("start accepting files")
				while True:
					try:
						temp = client_socket.recv(BUFFER_SIZE).decode()
						if str(temp) == " ":
							print("No such file(file not exist")
							break
						idx = temp.rindex(",")
						filename,filesize = temp[:idx],temp[idx+1:]
						print(temp)
						print(filename)
						print(filesize)
						print(client_socket.getsockname())
						print(address)
						if str(filename) in fileList:
							fileLocation[filename].add(address)
							for i in fileChunk[filename]:
								i.append(address)
							fileChunk[filename][chunkNum].append(address)
						else:
							fileList.add(str(filename))
							fileLocation[str(filename)] = {address}
							fileSize[str(filename)] = filesize
							fileChunk[filename] = {}
							
							for i in range(-int(-int(filesize)//CHUNK_SIZE)):
								fileChunk[filename][str(i)] = {address}
						print(f"Sent file {filename}")
						#print("breaked add one file")
						break
						
					except BlockingIOError:
						pass
					except Exception as e:
						print(f"Error handling client {address}: {str(e)}")
						client_socket.close()
						return None
			#print("breaked add files")
			break
			
		except BlockingIOError:
			pass
		except Exception as e:
			print(f"Error handling client {address}: {str(e)}")
			client_socket.close()
			return None
			
def FLR(client_socket, address):
	# Send the list of available files
	file_list = fileList
	if not file_list:
		client_socket.send("None".encode())
	client_socket.send("\n".join(file_list).encode())
	print(f"\File List Request from client {address}")
	
def FLsR(client_socket, address):
	while True:
		try:
			filename = client_socket.recv(BUFFER_SIZE).decode()
			print(filename)
			#print("3.0000000000000001")
			
			if str(filename) in fileLocation:
				print(fileLocation[str(filename)])
				temp = []
				for i in fileLocation[str(filename)]:
					a,b = i
					temp.append("'"+str(a)+"'"+","+str(b))
				print("\n".join(temp))
				client_socket.send("\n".join(temp).encode())
			else:
				#print('33333333333333')
				client_socket.send("None".encode())
			break
		except BlockingIOError:
			pass
		except Exception as e:
			print(f"Error handling client {address}: {str(e)}")
			client_socket.close()
			break
	print(f"\File List Request from client {address}")
# Function to handle a client's requests

# Function to get file size
def GFS(client_socket, address):
	while True:
		try:
			filename = client_socket.recv(BUFFER_SIZE).decode()
			print(filename)
			#print("3.0000000000000001")
			
			if str(filename) in fileSize:
				print(fileSize[str(filename)])
				
				client_socket.send(fileSize[str(filename)].encode())
			else:
				#print('33333333333333')
				client_socket.send("None".encode())
			break
		except BlockingIOError:
			pass
		except Exception as e:
			print(f"Error handling client {address}: {str(e)}")
			client_socket.close()
			break
	print(f"\File List Request from client {address}")
	
def CRR(client_socket, address):
	print("start Chunk Register Request")

	while True:
		try:
			temp = client_socket.recv(BUFFER_SIZE).decode()
			if str(temp) == " ":
				print("No such file(file not exist")
				break
			idx = temp.rindex(",")
			filename,chunkNum = temp[:idx],temp[idx+1:]
			print(temp)
			print(filename)
			print(chunkNum)
			print(client_socket.getsockname())
			print(address)
			if str(filename) in fileChunk:
				fileChunk[filename][chunkNum].append(address)
			else:
				fileChunk[filename][chunkNum] = {address}
			print(f"Sent file {filename}")
			#print("breaked add one file")
			break
			
		except BlockingIOError:
			pass
		except Exception as e:
			print(f"Error handling client {address}: {str(e)}")
			client_socket.close()
			return None
			
def FCR(client_socket, address):

	print("start File Chunk Request")
	while True:
		try:
			temp = client_socket.recv(BUFFER_SIZE).decode()
			print("??????????")
			print(temp)
			idx = temp.rindex(",")
			print("1")
			filename,chunkNum = temp[:idx],temp[idx+1:]
			print("2")
			temp1, temp2 = list(random.choice(tuple(fileChunk[filename][chunkNum])))
			print("!!!!!!!!!")
			temp = temp1+","+str(temp2)
			print(temp)
			client_socket.send(temp.encode())
			break
		except BlockingIOError:
			pass
		except Exception as e:
			print(f"Error handling client {address}: {str(e)}")
			client_socket.close()
			return None


		
	
			
def handle_client(client_socket, address):
	print(f"Accepted connection from {address}")

	# Add the client to the list of connected clients
	connected_clients.append(client_socket)

	while True:
		try:
			# Receive the user's choice (SEND or RECEIVE)
			choice = client_socket.recv(BUFFER_SIZE).decode()
			print(choice)	
			if not choice:
				break

			if choice == "\Register Request":
				RR(client_socket, address)
			elif choice == "\File List Request":
				FLR(client_socket, address)
			elif choice == "\File Locations Request":
				FLsR(client_socket, address)
			elif choice == "\Get File Size":
				GFS(client_socket, address)
			elif choice == "\Chunk Register Request":
				CRR(client_socket, address)
			elif choice == "\File Chunk Request":
				FCR(client_socket, address)
				

		except BlockingIOError:
			pass
		except Exception as e:
			print(f"Error handling client {address}: {str(e)}")
			client_socket.close()
			break

	# Remove the client from the list of connected clients
	connected_clients.remove(client_socket)
	client_socket.close()
	print(f"Connection from {address} closed")
	ServerClear(address)

# Main function
def main(host, port):

				
				
	# Create a socket for listening
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	server_socket.close()
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#return None
	server_socket.setblocking(False)
	server_socket.bind((host, port))
	server_socket.listen()
	server = server_socket


	print(f"Server listening on {host}:{port}")

	while True:
		try:
			client_socket, client_address = server_socket.accept()
			print(f"Accepted connection from {client_address}")
			client_socket.setblocking(False)
			
			client_data[client_socket] = b""# Initialize client data buffer
			# Start a thread to handle the client
			client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
			client_thread.start()
		except BlockingIOError:
			pass
		except Exception as e:
			print(f"Error handling client : {str(e)}")
			
			server_socket.close()
			break

if __name__ == "__main__":
	host, port = sys.argv[1], int(sys.argv[2])
	main(host, port)

