import socketserver
import time
import datetime
import threading
import sys,os,json
import uuid
from decimal import *
from modules.e_object import e_object
from modules.e_datetime import Timer
from modules.e_file import File
from modules.e_sock import e_sock
from modules.spamodule.sparkHandler import sparkHandler
import struct

#initialize this global variable to handle the client data
data_queue={}

            
class DataHandler(socketserver.BaseRequestHandler,e_object):
    """This class has been declare to handle the request send by the client
    """
    
    def client_data_send(self,to_object=False):
        #recieve all the byte data send by the client and save it into
        #the data variable object
        self.data=self.recvall(self.request,1024)
        #Trasform the send data into requestData object
        if self.data!=None:
            
            if to_object:
                return requestData(**(json.loads(self.data.decode("utf-8"))))
            
            try:
                return json.loads(self.data.decode("utf-8"))
            
            except json.decoder.JSONDecodeError as ex:
                data={"action":"None","data":self.data.decode("utf-8")}
                return data
        
    def get_current_time(self):
        time_stamp=time.time()
        return datetime.datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')
    
    def get_env(self,env_name):
        """Get the environment variable"""
        return os.environ[env_name]
    
    def handle_transaction_data(self,recieve_data):
        pass
    
    def handler_requester(self,request_data):
        username=request_data.username
        hour_interval=request_data.time_inter
        spark_handler=sparkHandler(username)
        spark_handler.set_hour_interval(hour_interval)
        
        is_save=False
        
        request_action=request_data.action

        try:
            if request_data.action =="sum":
                trans_sum=spark_handler.get_sum_transaction()
                self.request.sendall((json.dumps({"sum":trans_sum}).encode("utf-8")))

            if request_data.action =="trans":
                print("In action")
                trans_data=spark_handler.view_transaction()
                print(trans_data)
                self.request.sendall((json.dumps(trans_data)).encode("utf-8"))
                
            if request_data.action =="data_frame":
                data_frame=spark_handler.get_transaction().get_list_column()
                self.request.sendall((json.dumps(data_frame)).encode("utf-8"))
                
            if request_data.action =="save_trans":
                status="success"
                message="Data successfuly saved"
                is_save=spark_handler.save_transaction()
                if not is_save:
                    status="failed"
                    message="There is an error saving the requested user data"
                    
                self.request.sendall((json.dumps({"message":message,"status":status}).encode("utf-8")))
                

            if request_action in ["sum","trans"]:
                print("data save")
                spark_handler.save_transaction()
        
                
        except Exception as ex:
            print(ex)
            self.request.sendall((json.dumps({"message":str(ex),"status":"failed"}).encode("utf-8")))
            #self.request.sendall((json.dumps({"Error_message":"There is an error proccesssing your request","status":"failed"}).encode("utf-8")))
        
    
        
    def handle(self):
            """The handle function get call every time a new client connect into 
               the server socket
            """
            recieve_data=self.client_data_send(True)
            
            is_requester=False
            is_action_requested=False
            
            if hasattr(recieve_data,"transaction_data"):
                is_requester=True
            elif hasattr(recieve_data,"action"):
                is_action_requested=True
            
            if is_requester:
                self.handle_transaction_data(recieve_data)
            elif (is_action_requested):
                self.handler_requester(recieve_data)
            else:
                """In case the request card number is invalid send
                   an error message to the client.
                """
                self.request.sendall((json.dumps({"Error_message":"An error has occured","status":"failed"}).encode("utf-8")))


    def recvall(self,request,recv_byte):
        """This method help to wait and get all the send data from the connected
           client
        """
        #initialize the buffer object to a binary
        buf=b''

        #wait untill all the data send by the client was retrieve
        while recv_byte:
            #start getting the data send by the client
            data_recv=request.recv(recv_byte)

            #if case there is no data send by the client return none
            if not data_recv: return None

            #keep appending the recieve data into buf object
            buf+=data_recv

            """remove the length of byte currently recieve from the
               total length of byte sent
            """
            recv_byte-=len(data_recv)

            #return the recieve data
            return buf
        return None


class requestData():
    """This class is use to store the data send by the client 
       as class object data, a small reminder is the data has been send as a json
       format.Every json key represent the object key
    """

    def __init__(self,**entities):
        self.__dict__.update(entities)


class ThreadTCPServer(socketserver.ThreadingMixIn,socketserver.TCPServer):

    """A void class that only inherite the ThreadingMixIn and socketserv.TCPServer
       class.
    """
    allow_reuse_address = True
    pass


class DataManager(object):
    """Declare to run the current server.
    """

    @staticmethod
    def server_thread(port=8085,host=""):
        """Static method use for starting the server thread.When called this
           method by the default the server will run on port 8084, but can be
           change to any port.And if the host leave empty it will use the current
           machine ip address to recieve a connection.	   
        """
        """Start the server ThreadTCPServer with the handler class
           This way the server will handle each client request
            in the separate thread process
        """
        server = ThreadTCPServer((host, port),DataHandler)

        #let us initialize the thread method with the THreadTCPServer
        #object		
        server_thread=threading.Thread(target=server.serve_forever)
        #allow_reuse_address=True
        #here we go start the thread
        server_thread.start()
        



