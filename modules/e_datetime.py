import time
import datetime as dte

class Timer(object):


    def __init__(self):

        self.localtimer=time.localtime(time.time())
        self.start_timer=None
        self.end_timer=None

    def get_time(self):
        return "{}:{}".format(self.localtimer.tm_hour,self.localtimer.tm_min)

    def get_year(self):
        return "{}".format(self.localtimer.tm_year)

    def get_day(self):
        return "{}".format(self.localtimer.tm_mday)
    def get_month(self):
        return "{}".format(self.localtimer.tm_mon)
    def get_min(self):
        return "{}".format(self.localtimer.tm_min)
    def get_hour(self):
        return "{}".format(self.localtimer.tm_hour)
    def get_sec(self):
        return "{}".format(self.localtimer.tm_sec)


    def start_time(self):


        self.localtimer=time.localtime(time.time())
        self.start_timer=dte.datetime(int(self.get_year()),int(self.get_month()),int(self.get_day()),int(self.get_hour()),int(self.get_min()),int(self.get_sec()))

    def end_time(self):

        self.localtimer=time.localtime(time.time())
        self.end_timer=dte.datetime(int(self.get_year()),int(self.get_month()),int(self.get_day()),int(self.get_hour()),int(self.get_min()),int(self.get_sec()))


    def diff_btwn_date_in_sec(self):

        self.end_time()

        return ((self.end_timer - self.start_timer).total_seconds())






