import time
import datetime
import os,json
from modules.e_file import File
from modules.spamodule.spfinder import *
from pyspark.sql.types import *

class sparkHandler:
    
    def __init__(self,user_name=None):
        #The requested user name for the transaction
        self.username=user_name
        #The hourly interval requested, here set default 6
        self.hour_interval=6
        
        self.file_handler=File()
        
        self.list_file=None
        
        self.data_frame=None
        
        self.table_name=None
        
        self.data_frame_sql=None
        
        self.db_conn=None
        
        self.list_column=None
        
    def get_table_name(self):
        return self.table_name
        
    def set_username(self,username):
        self.username=username
        
    def get_username(self):
        return self.username
        
    def get_hour_interval(self):
        return (self.hour_interval+1)
    
    def get_env(self,env_name):
        """Get the environment variable"""
        return os.environ[env_name]
    
    def set_hour_interval(self,hour):
                
        if (hour in ["Now","now"]) or (not isinstance(hour,int)):
            
            self.hour_interval=0
        else:
            self.hour_interval=hour
        return self
            
    def get_current_dattime(self):
        """ Get the current datetime """
        return datetime.datetime.now()
    
    def get_datetime_difference_by_request_hour(self):
        """
        Get the last date by the given hour time interval from now  
        """
        if self.get_hour_interval()==1:
            return datetime.datetime.now()
        return self.get_current_dattime() - datetime.timedelta(hours=self.get_hour_interval())
    
    def get_list_of_save_json_file(self):
        i=0
        #set the list to hold all the file
        text=[]
        """

        """
        tmp_storage=self.get_env("HSBC_MINNING_DIR");

        hour_interval=self.get_hour_interval()

        current_interval_date_time=self.get_datetime_difference_by_request_hour()
        
        while i <= hour_interval:

            file_name=tmp_storage+"/"+str((current_interval_date_time+datetime.timedelta(hours=i)).strftime('%Y_%m_%d_%H'))
            if self.file_handler.is_file_exist(file_name+".json"):
                text.append(file_name+".json")

            i+=1
 
        self.list_file=",".join(text)

        if(len(self.list_file)==0):
            raise Exception("No transaction found")
        
    def get_list_file(self):
        """
        Call this method to get all the last edit file 
        """
        try:
            self.get_list_of_save_json_file()
            return self.list_file
        except Exception as ex:
            raise Exception(ex)
        
        
    def get_spark_data_frame(self,table_name="credit_transaction"):
        
        try:
            self.table_name=table_name

            list_file=self.get_list_file()

            user_last_transaction=sc.textFile(list_file)

            data_frame =spark.read.json(user_last_transaction)

            data_frame.createOrReplaceTempView(table_name)

            self.data_frame=data_frame

            return data_frame
        except Exception as ex:
            raise Exception(ex)
    
        
    def load_transaction(self):
        self.get_spark_data_frame()
        
        
    
    def count_transaction_by_interval_hour(self):
        try:
            if self.data_frame==None:
                self.get_spark_data_frame()

            return self.data_frame.count()
        except Exception as ex:
            raise Exception(ex)
    
    def get_transaction(self,user=None):
        try:
            if user !=None:
                username=user            
            else:
                username=self.get_username()
            if self.data_frame==None:
                self.get_spark_data_frame()
            data_frame_sql=spark.sql("select * from credit_transaction where SenderName='"+username+"'")

            self.data_frame_sql=data_frame_sql
            self.list_column=(self.data_frame_sql.drop("token").columns)
            return self
        except Exception as ex:
            raise Exception(ex)
            
    def get_list_column(self):
        return self.list_column
        
    def view_transaction(self,display=False):
        try:
            number_of_transaction=self.count_transaction_by_interval_hour()

            if self.data_frame_sql ==None:
                self.get_transaction()

            if display:
                self.data_frame_sql.show(number_of_transaction,False)
            else:
                return (self.data_frame_sql.drop("token").collect())
        except Exception as ex:
            raise Exception(ex)
        
    def get_sum_transaction(self,display=False,column="Amount"):
        try:
            number_of_transaction=self.count_transaction_by_interval_hour()
            if self.data_frame_sql ==None:
                self.get_transaction()

            if display :
                self.data_frame_sql.groupBy().sum(column).show()
            else:
                result=self.data_frame_sql.groupBy().sum(column).collect()
                return result[0].__getitem__("sum(Amount)")
        except Exception as ex:
            raise Exception(ex)
        
    def db_config(self,username="spark",password="spark",dbname="spark",host="localhost",dbtype="mysql",drivertype="jdbc"):
        try:
            driver="com."+dbtype+"."+drivertype+".Driver"
            url=drivertype+":"+dbtype+"://"+host+"/"+dbname

            self.db_conn=self.data_frame_sql.write.format('jdbc').options(
            url=url,
            driver=driver,
            dbtable=self.table_name,
            user=username,
            password=password)
        except Exception as ex:
            raise Exception(ex)
        
        
        
    def save_transaction(self,mode="append"):
        
        try:
            if self.data_frame_sql ==None:
                self.get_transaction()
            if self.db_conn ==None:
                self.db_config()
            self.db_conn.mode(mode).partitionBy("token").saveAsTable(self.table_name)
            return True
        except Exception as ex:
            return False
    
    
    
    
        
    
        
        
        
    
        
    