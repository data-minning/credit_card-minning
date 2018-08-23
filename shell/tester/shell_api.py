from  modules.e_sock import *
import time

trans_info={
  "action": "trans",
  "username": "Aagaard",
  "time_inter":2
    
}

clientsocket = e_sock("localhost",8085)

is_connect=clientsocket.connect()

try_in_sec=1
while not is_connect:
    is_connect=clientsocket.connect()
    print("Waiting for the server to be alive")
    time.sleep(try_in_sec)
    try_in_sec*=3
print("Connect to the server")    
    
clientsocket.set_data(trans_info)

clientsocket.sendall("json")

data_rec=clientsocket.getall("json")

print(data_rec)
