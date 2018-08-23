
from modules.spamodule.sparkHandler import *
import json

user="Aagaard"

hour_interval=2

try:

    spark_handler=sparkHandler(user)
    
    spark_handler.set_hour_interval(hour_interval)
    
    print(spark_handler.view_transaction())
    
    #print(spark_handler.get_transaction().get_list_column())

    #print((json.dumps(spark_handler.view_transaction())))
    
    
    #print(spark_handler.get_sum_transaction())
    
   # spark_handler.save_transaction()

except Exception as ex:
    print(ex)
    print("No record found for user:'"+user+"'")
    
