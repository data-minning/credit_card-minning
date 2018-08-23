from http.server import HTTPServer, BaseHTTPRequestHandler
from  modules.e_sock import *
import time
import cgi
from socket import error as socket_error
from lxml import etree
from urllib.parse import *

urls = (
    '/(.*)', 'index'
)


class MiniRequester(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        try:
            self._set_headers()
            query = urlparse(self.path).query
            data = parse_qs(query)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            request_time=None
            try:
                request_time=int(data["time_inter"])
                
            except Exception as ex:
                request_time=data["time_inter"]

            trans_info={
            "action": str(data["action"]),
            "username": str(data["username"]),
            "time_inter":request_time
            }

            clientsocket = e_sock("localhost",8085)

            is_connect=clientsocket.connect()

            try_in_sec=1
            while not is_connect:
                is_connect=clientsocket.connect()
                time.sleep(try_in_sec)
                try_in_sec*=3
                if try_in_sec==9:
                    raise socket_error("Cannot connect to the host server")
                    return False
            print(trans_info)
            clientsocket.set_data(trans_info)
            
            clientsocket.sendall("json")

            data_rec=clientsocket.getall("json")
            
            #print(data_rec)
            
            if "message" in data_rec:
                if data_rec["message"]=="Object of type 'Decimal' is not JSON serializable":
                    self.out("There is an error processing your request")
                else:
                    self.out(str(data_rec["message"]))
            else:
                if data["action"]=="trans":
                    self.out("<h1>Number of record found:<strong style='color:red;'>"+str(len(data_rec))+"</strong></h1><br>")
                    s = "<table text-align='center'><tr><th>Amount</th><th>Date Time Transaction</th><th>Recipient Card Primary Account Number</th><th>Sender Account Number</th><th>Sender Country Code</th><th>Sender Name</th><th>Source Of Funds Note</th><th>Transaction Currency</th><th>Action</th></tr>"
                    self.out(s)
                    for row in data_rec:
                        self.out("<tr>")
                        for data_store in row:
                            self.out("<td>"+str(data_store)+"</td>")
                    #elf.out(data_rec[str(data["action"])])
                        self.out("</tr>")
                    self.out("</table>")
                elif data["action"]=="sum":
                    self.out("<h1><p style='text-align:center;'>Sum of record found:<strong style='color:red;'>"+str(data_rec[str(data["action"])])+"</strong></p></h1><br>")
        except KeyboardInterrupt as e:
            pass
        except socket_error as ex:
            self.out(ex)
        except KeyError as ex:
            self.out("There is an error proccessing your request")
            print(ex)
        except Exception as ex:
            print(ex)

    def do_HEAD(self):
        self._set_headers()
        
   
        
    def out(self,str_data):
        if isinstance(str_data,int) or isinstance(str_data,str):
            self.wfile.write(str(str_data).encode("utf-8"))
        
def run(server_class=HTTPServer, handler_class=MiniRequester, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
