#Build to load pyspark library 
#

#Us of findsparkto find the pyspark location
import findspark

#load the pyspark module path
findspark.init()

#import the pyspark class
import pyspark


#importing the pyspark sql class
from pyspark.sql import SparkSession

#create a spark object
spark = SparkSession \
    .builder \
    .appName("Python Spark SQL basic example") \
    .config("spark.some.config.option", "some-value") \
    .getOrCreate()

#create a spark context object
sc = spark.sparkContext

sc.setLogLevel("ERROR")
