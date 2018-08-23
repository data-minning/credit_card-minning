
from modules.e_object import e_object

class e_array(list):

    def __init__(self):
        super().__init__()
        self.e_array=[]
        self.index=None

    def size(self):
        return len(self)


    def get(self,index):
        self.index=index
        return self[index]	
