import socketserver
import time
import datetime
import threading
import sys,os,json
import uuid
from modules.e_object import e_object
from modules.e_datetime import Timer
from modules.e_file import File
from modules.e_sock import e_sock

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

    def stream_to_spark(self,transfer_data):
        
        clientsocket = e_sock("localhost",8085)

        is_connect=clientsocket.connect()
        
        if is_connect:
            
            clientsocket.set_data(transfer_data)
            
            clientsocket.sendall("json")
            
            clientsocket.close()

    
    def get_env(self,env_name):
        """Get the environment variable"""
        return os.environ[env_name]
    
    def save_transaction(self,transaction_data):
                time_stamp=time.time()
                file_data=json.dumps(transaction_data)
                current_date=datetime.datetime.fromtimestamp(time_stamp)
                current_date_as_folder_name=current_date.strftime('%Y_%m_%d')
                #current_hour_as_folder_name=current_date.strftime('%H')
                file_directory=self.get_env("HSBC_MINNING_DIR")
                File.mkdir(file_directory)
                current_date=datetime.datetime.fromtimestamp(time_stamp)
                file_name=str(current_date.strftime('%Y_%m_%d_%H'))+".json"
                #print(file_name)
                #file_name=str(transaction_data["token"])+".json"
                file_path=file_directory+"/"+file_name

                File.write_append_to(file_path,file_data)

                stream_data={"transaction_data":transaction_data,"store_file":file_path}
                
                self.stream_to_spark(stream_data)
                
 
    def handle(self):
            """The handle function get call every time a new client connect into 
               the server socket
            """
            request_data=self.client_data_send()
            
            
            if (request_data!=None) :
               
                """Check if the action request by the user is to authentication
                """
                token=None

                if(request_data["action"]=="trans"):
                    
                    #initialize a ditionary object with the token data send
                    #by the user as the key
                    token_exist=data_queue.get(request_data["SenderAccountNumber"],None)
                    
                    date_transaction=self.get_current_time()
                    
                    request_data["DateTimeTransaction"]=(date_transaction)
                    
                    self.save_transaction(request_data)

                    if not token_exist:
                        #token=request_data["SenderAccountNumber"]
                        data_queue[token]=[]
                        data_queue[token].append(request_data)
                    else:
                        #token=request_data["SenderAccountNumber"]
                        data_queue[token].append(request_data)
                        
                    #print(data_queue)

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


class DataServer(object):
    """Declare to run the current server.
    """

    @staticmethod
    def server_thread(port=8084,host=""):
        
        try:
            """Static method use for starting the server thread.When called this
               method by the default the server will run on port 8084, but can be
               change to any port.And if the host leave empty it will use the current
               machine ip address to recieve a connection.	   
            """
            """Start the server ThreadTCPServer with the handler class
               This way the server will handle each client request
                in the separate thread process
            """
            print("Start the data server on port: "+str(port))
            server = ThreadTCPServer((host, port),DataHandler)

            #let us initialize the thread method with the THreadTCPServer
            #object		
            server_thread=threading.Thread(target=server.serve_forever)
            #allow_reuse_address=True
            #here we go start the thread
            server_thread.start()
        except (KeyboardInterrupt,Exception) as ex:
            pass
        



