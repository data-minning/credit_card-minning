#!/usr/bin/python3.6

import sys,os
from data_handler import DataServer


def main():
    """Use as the main  start up of running the program.Just write anything here
    """
    try:
        """
        There is only one thing you can do to start the server
        you can call the class method server_thread on the class
        DataServer with argument or not.If no argument has been pass
        the server will use the current ipaddress with 8084 as the
        port number by default.
        """
        DataServer.server_thread(8084,"")
        #raise Exception("Server stop intantly")
    except (Exception,KeyboardInterrupt) as ex:
        pass


#check if the command line file called is the main file
if __name__=="__main__":

    #waiting for the keyboardInterrupt action issue by the user
    try:
        #called to start the program
        main()
    except KeyboardInterrupt:
        """if the program catch any key that request an interrupt
           immediate of the program.Print this message to the user. 
        """ 
        print("\nOperation cancel by the user")
        try:
            sys.exit(0)
        except (SystemExit,KeyboardInterrupt):
            os._exit(0)

