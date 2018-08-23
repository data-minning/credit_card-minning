from modules.e_datetime import Timer
from time import sleep
import sys,os
import uuid

class e_object(Timer):

    def __init__(self):
        super(Timer,self)
        self.exec_time=Timer()
        self.exec_time.start_time()


    def run_time(self):
        print("\nExecution time ({} seconds)".format(self.exec_time.diff_btwn_date_in_sec()))


    def get_runtime(self):
        return "({} seconds)".format(self.exec_time.diff_btwn_date_in_sec())


    def e_array(self):
        self.e_array=[]
        return self.e_array

    def progress_bar(self,*options):

        iteration,total,prefix,suffix,length= options
        decimals= 1

        fill= "{}".format(self.ascii_str(9608))

        percent=("{0:."+str(decimals) + "f}").format(100 * (iteration / float(total)))

        filled_length=int(length * iteration // total)

        bar = fill * filled_length + '_' * (length - filled_length)

        print('\r%s |%s| %s%% %s' %(prefix,bar,percent,suffix),end="\r")


        if iteration == total:
            print()

    def load_progress_bar(self,items):
        item_length=5
        self.progress_bar(0,item_length,"Progress:","Complete",50)
        i=0

        while i < item_length:

            sleep(0.1)

            self.progress_bar(i,item_length,"Progress:","Complete",50)
            item_length=len(items)
            i+=1
           
    @staticmethod
    def get_env(env_name):
        """Get the environment variable"""
        return os.environ[env_name]

    #9608 for fill horizontal bar

    def ascii_str(self,code):

        ascii_car_code=chr(code)
        return ascii_car_code		

    def sizeOf(self,_str):
        return sys.getsizeof(_str)

    def run_shell(self,command):

        os.system(command)

    def define_class(self,class_name):
        return type(class_name,(),{})

    def define_class_prop(self,class_obj,prop_name,prop_val=""):
        setattr(class_obj,prop_name,prop_val)
        
    def gen_rand_str(self):
        return uuid.uuid4().hex
    
    def gen_rand_int(self,length=25):
        str_data=str(uuid.uuid4().int)
        return int(str_data[:length])
    
    

