import socket,json
from modules.e_object import e_object
import logging
import struct


class e_sock:

    def __init__(self,host="localhost",port=8084):
        self.connect_sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.json=json
        self.host=host
        self.port=port
        self.send_data=None
        #super(socket)

    def set_data(self,data):
        self.send_data=data

    def connect(self):
        is_connect=True
        try:
  
            self.connect_sock.connect((self.host, self.port))

        except ConnectionRefusedError as ex:
            return False
        return is_connect
    
    def close(self):
        self.connect_sock.close()

    def sendall(self,data_type=None):

        if data_type=="json":
            json_data=(json.dumps(self.send_data))
            self.connect_sock.send(json_data.encode("utf-8"))
        else:
            self.connect_sock.send((self.send_data).encode("utf-8"))

            
    def getall(self,data_type=None,recv_byte=1024):

        try:
            self.receive_data=self.recvall()
            if data_type=="json":
                return json.loads(self.receive_data.decode("utf-8"))
            else:
                return (self.receive_data.decode("utf-8"))
        except Exception as ex:
            print(ex)
        
        
    def recvall(self,recv_byte=1024):
        """This method help to wait and get all the send data from the connected
           client
        """
        #initialize the buffer object to a binary
        buf=b''
        #wait untill all the data send by the client was retrieve
        
        while True:
            #start getting the data send by the client
            data_recv=self.connect_sock.recv(recv_byte)
            
            #if in case there is no data send by the server stop the loop
            if len(data_recv)==0: break

            #keep appending the recieve data into buf object
            buf+=data_recv

        return buf
         
