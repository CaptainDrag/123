import socket
import os
import sys
import threading

# Constants
SERVER_IP = 'localhost'  # Change this to the IP address of the server
SERVER_PORT = 12345      # Port for file sharing
BUFFER_SIZE = 1024
CHUNK_SIZE = 1024

# Function to send a file to the server
def send_file(server_socket, filename):
    with open(filename, 'rb') as file:
        data = file.read(BUFFER_SIZE)
        while data:
            server_socket.send(data)
            data = file.read(BUFFER_SIZE)
def HELP():
	help = ("\HELP: for the help menu\n\Register Request: Tells the server what files the peer wants to share with the network. Takes in the IP address and port for the endpoint to accept peer connections for download; the number of files to register; and for every file, a file name and its length.\n\File List Request: Asks the server for the list of files.\n\File Locations Request: Asks the server for the IP endpoints of the peers containing the requested file.\n\Chunk Register Request: Tells the server when a peer receives a new chunk of the file and becomes a source (of that chunk) for other peers.\n\File Chunk Request: Asks the peer to return the file chunk. Reads in a file name, chunk indicator.\n\Download File: Download File from peers\n\Disconnect: disconnect from server")
	print(help)
	

def RR(client_socket):
	#print("1111111111111")
	client_socket.send("\Register Request".encode())
	numFile = input("Enter the number of files to register: \n")
	try:
		int(numFile)
	except Exception as e:
		print(f"Error handling client {address}: {str(e)}")
		client_socket.close()
		return
	client_socket.send(numFile.encode())
	for i in range(int(numFile)):
		file_name = input("Enter the filename to send: \n")
		directory = os.getcwd()
		
		file_path = os.path.join(directory, file_name)
		print(file_path)


		if os.path.exists(file_path):
			file_size = os.path.getsize(file_path)
			print(file_size)
			temp = file_name+","+str(file_size)
			print(temp)
			print(f'The file {file_path} exists.')
			client_socket.send(temp.encode())
					
			print(f"File '{file_name}' sent to the server")
		else:
			client_socket.send(" ".encode())
			print(f'The file {file_path} does not exist.')
		
		
		
		
		
		
		
		
					
				
def FLR(client_socket):
	#print("CALL SOME FUNC") 
	client_socket.send("\File List Request".encode())
	while True:
		try:
			filename = client_socket.recv(BUFFER_SIZE).decode()
			return filename
			break
		except BlockingIOError:
			pass
		except Exception as e:
			print(f"Error handling client {address}: {str(e)}")
			client_socket.close()
			break
			
def FLsR(client_socket, indicator):
	client_socket.send("\File Locations Request".encode())
	if not indicator:
		fileName = input("Please enter the name of file to request: \n")
	else:
		fileName = indicator
	client_socket.send(fileName.encode())
	while True:
		try:
			fileLocations = client_socket.recv(BUFFER_SIZE).decode()
			return fileLocations
			break
		except BlockingIOError:
			pass
		except Exception as e:
			print(f"Error handling client {address}: {str(e)}")
			client_socket.close()
			break
		
		

def GFS(client_socket,file_name):
	#print("CALL SOME FUNC") 
	client_socket.send("\Get File Size".encode())
	client_socket.send(file_name.encode())
	while True:
		try:
			fileSize = client_socket.recv(BUFFER_SIZE).decode()
			return fileSize
			break
		except BlockingIOError:
			pass
		except Exception as e:
			print(f"Error handling client {address}: {str(e)}")
			client_socket.close()
			break
				
def DF(client_socket):
	fileList = FLR(client_socket)
	print(fileList)
	file_name = input("Enter the file you want to download: \n")
	if file_name not in fileList:
		print("No Such File Exist!")
		return
	fileSize = GFS(client_socket,file_name)
	print(fileSize)
	fileLocations = FLsR(client_socket, file_name).split("\n")
	temp = []
	for i in fileLocations:
		t1, t2 = i.split(",")
		temp.append([t1.strip("\'\""),t2.strip("\'\"")])
	fileLocations = temp
	print(fileLocations)
	
	
	
def CRR(client_socket):
	#print("1111111111111")
	client_socket.send("\Chunk Register Request".encode())

	fileName = input("Enter the file name to register: \n")
	Chunk_num = input("Enter the chunk number of file to register:\n")
	
	
	
	file_name = fileName+"_"+str(Chunk_num)
	directory = os.getcwd()
	
	file_path = os.path.join(directory, file_name)
	print(file_path)


	if os.path.exists(file_path):
		file_size = os.path.getsize(file_path)
		print(file_size)
		if file_size != CHUNK_SIZE:
			client_socket.send(" ".encode())
			print('The chunk size does not fit.')
			return
		temp = fileName+","+str(Chunk_num)
		print(temp)
		print(f'The chunk {file_path} exists.')
		client_socket.send(temp.encode())
				
		print(f"Chunk '{file_name}' sent to the server")
	else:
		client_socket.send(" ".encode())
		print('The chunk does not exist.')
		

		
def FCR(client_socket):
	
	fileList = FLR(client_socket)
	print(fileList)
	file_name = input("Enter the file you want to download: \n")
	if file_name not in fileList:
		print("No Such File Exist!")
		return
	fileSize = GFS(client_socket,file_name)
	#print(fileSize)
	chunkNum = input("Please enter the chunk indicator: \n")
	try:
		int(chunkNum)
	except Exception as e:
		print(f"Error handling client {address}: {str(e)}")
		client_socket.close()
		return
	if int(chunkNum) not in range(-int(-int(fileSize)//CHUNK_SIZE)):
		print("No Such Chunk Exist!")
		return
	client_socket.send("\File Chunk Request".encode())
	temp = file_name+","+str(chunkNum)
	client_socket.send(temp.encode())
	while True:
		try:
			addr = client_socket.recv(BUFFER_SIZE).decode()
			idx = addr.rindex(",")
			h,p = addr[:idx],addr[idx+1:]
			h,p = h,int(p)
			FCR_helper(h,p,file_name,chunkNum)
			print("4")
			print("CHUNK ADDR?")
			print(addr)
			return addr
		except BlockingIOError:
			pass
		except Exception as e:
			print(f"Error handling 111111111client : {str(e)}")
			client_socket.close()
			break
	
	
def FCR_helper(h,p,file_name,chunkNum):
	peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print(h,p)
	peer.connect_ex((h, p))
	print("connect succefful")
	print(peer.getsockname())
	peer.send(f"chunkDonwload {file_name} {chunkNum}".encode())
	print("1 after connect succefful")
	fileName = file_name+"_"+str(chunkNum)
	with open(fileName, "wb") as file:
		data = client_socket.recv(CHUNK_SIZE)
		file.write(data)
	peer.close()


def chunkDonwload(choice,client_socket):
	a,file_name,chunkNum = choice.split(" ")
	tempName = file_name+"_"+str(chunkNum)
	directory = os.getcwd()
	
	if os.path.exists(os.path.join(directory, tempName)):
		with open(os.path.join(directory, tempName), "rb") as file:
			data = file.read(CHUNK_SIZE)
			client_socket.send(data.encode())
	elif os.path.exists(os.path.join(directory, file_name)):
		with open(os.path.join(directory, file_name), "rb") as file:
			data = file.read(CHUNK_SIZE)
			for i in range(chunkNum):
				data = file.read(CHUNK_SIZE)
			client_socket.send(data.encode())
	else:
		print(f'The file {tempName} does not exist.')
		client_socket.send("".encode())
		
		
		
def handle_client( p2pSocket, p2pAddr):

	
	

	while True:
		try:
			choice = p2pSocket.recv(BUFFER_SIZE).decode()	
			if not choice:
				break
			# Receive the user's choice (SEND or RECEIVE)
			if choice.startswith("chunkDonwload"):
				chunkDonwload(choice,client_socket)
			

		except BlockingIOError:
			pass
		except Exception as e:
			print(f"Error handling client : {str(e)}")
			client_socket.close()
			break

	# Remove the client from the list of connected clients
	
	client_socket.close()
	
def peer_listening(host, port):
	
	peer_listen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	peer_listen.setblocking(False)
	#peer_listen.bind((host, port))
	peer_listen.listen()
	print(peer_listen.getsockname())
	
	while True:
		try:
			#print("Try to listen from peer")
			p2pSocket, p2pAddr = peer_listen.accept()
			print(f"Accepted connection from {p2pAddr}")
			p2pSocket.setblocking(False)
			
			
			p2p_listen = threading.Thread(target=handle_client, args=(p2pSocket, p2pAddr))
			p2p_listen.start()
		except BlockingIOError:
			pass
		except Exception as e:
			print(f"Error handling client : {str(e)}")
			
			peer_listen.close()
			break
		
	
# Main function
def main(host, port):
	# Create a socket to connect to the server
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client_socket.setblocking(False)
	print(client_socket.getsockname())
	client_socket.connect_ex((host, port))
	print(client_socket.getsockname())
	print(client_socket.getsockname())
	
	
	p2pListening = threading.Thread(target=peer_listening, args=(client_socket.getsockname()))
	p2pListening.start()
	HELP()
	
	while True:
		choice = input("Enter your choice: \n")
		match choice:
			case "\HELP":
				HELP()
			case "\Register Request":
				RR(client_socket)
			case "\File List Request": 
				print(FLR(client_socket))
			case "\File Locations Request": 
				print(FLsR(client_socket, None))
			case "\Chunk Register Request": 
				CRR(client_socket)
			case "\File Chunk Request":
				FCR(client_socket)
			case "\Download File":
				DF(client_socket)
			case "\Disconnect":
				client_socket.close()
				break
			case default:
				print("No such function exist!".encode())
		


if __name__ == "__main__":
	temp = input("Running Client... \nPlease enter server_addr you want to connet(host port)\n").split(" ")
	if len(temp) != 2:
		print("Wrong input size!")
		sys.exit()
	else:
		host, port = temp[0], int(temp[1])
	sys.exit(main(host, port))
