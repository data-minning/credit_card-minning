import unittest
from modules.spamodule.sparkHandler import sparkHandler

class TestDriveDev(unittest.TestCase):
    """Test if the below method the their respective class"""
    def test_set_hour_interval(self):
        """Test if the method set_hour_interval exists"""
        spark_handler=sparkHandler()
        spark_handler.set_hour_interval(6)
        
    def test_get_hour_interval(self):
        spark_handler=sparkHandler()
        spark_handler.get_hour_interval()
        
class TestSparkHandler(unittest.TestCase):
    
    def test_hour_interval(self):
        spark_handler=sparkHandler()
        """test if the hourly interval is set to 6"""
        spark_handler.set_hour_interval(6)
        self.assertEqual(spark_handler.get_hour_interval(),7)
        """test if the hourly interval request which is nown is 0"""
        spark_handler.set_hour_interval("Now")
        self.assertEqual(spark_handler.get_hour_interval(),1)
        spark_handler.set_hour_interval("nower")
        self.assertEqual(spark_handler.get_hour_interval(),1)
        
    
        

        
        
if __name__ == '__main__':
    unittest.main()

