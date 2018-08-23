from modules.e_sock import e_sock
from modules.e_object import e_object
from modules.e_file import File
from modules.e_array import e_array
import logging
import os

import threading
import time

class Card:
    
    def __init__(self):
        self.number= e_object.gen_rand_int(16)
        self.expired_data=None
        
        
class User:
    def __init__(self):
        self.name=None
        
    def set_name(self,name):
        self.name=name

    
class Reciever(Card,User):
    
    def __init__(self):
        Card.__init__(self)
        User.__init__(self)
    
class Sender(Card,User,e_object):
    
    reciever=Reciever()
    
    def __init__(self,card_number,action,funds_note=None):
        Card.__init__(self)
        User.__init__(self)
        self.number=card_number
        self.amount=self.gen_rand_int(6)
        self.action=action
        self.source_of_funds_note=funds_note
        
    def generate_transation_data(self):
        """Generate the transaction data"""
        token=e_object.gen_rand_int(11)
        number=str(e_object.gen_rand_int(16))
        
        transaction_data={
            "token":token,
            "action":self.action,
            "SenderAccountNumber": self.number,
            "SenderName":self.name,
            "SenderCountryCode": "USA",
            "TransactionCurrency": "USD",
            "RecipientCardPrimaryAccountNumber": number,
            "Amount": self.amount,
            "SourceOfFundsNote":self.source_of_funds_note
            }
        
        return transaction_data
    
    def transfer(self):
        return self.generate_transation_data()
    


class Emitter:
    
    def __init__(self,card_number,sender_name,trans_note=None):
        self.sender_name=sender_name
        self.trans_note=trans_note
        self.card_number=card_number
    

    def emmit_trans(self):
        
        clientsocket = e_sock()

        is_connect=clientsocket.connect()

        sender=Sender(self.card_number,"trans",self.trans_note)

        sender.set_name(self.sender_name)

        transfer_data=sender.transfer()

        if(is_connect):
            
            clientsocket.set_data(transfer_data)

            clientsocket.sendall("json")

        
def start_transaction(transaction_delay):
    
    try:
        file=File()
        hsbc_home=e_object.get_env("HSBC_MINNING_HOME")
        list_card_holder=(file.json(hsbc_home+"/examples/data/account_holder.json").card_holder)
        print("Start the stream client")

        while True:
            for card_holder in list_card_holder:
                name=card_holder["sender_name"]
                card_number=str(card_holder["card_number"])
                if len(card_number) == 0:
                    card_number=e_object.gen_rand_int(16)
                    card_holder["card_number"]=card_number
                emmitter=Emitter(card_number,name)
                trans_thread = threading.Thread(name=name, target=emmitter.emmit_trans)
                trans_thread.start()
                time.sleep(transaction_delay)
            time.sleep(transaction_delay)
    except KeyboardInterrupt as ex:
        pass

start_transaction(2)



