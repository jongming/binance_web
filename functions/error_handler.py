import datetime
import traceback

class Error_Handler:
    def __init__(self, error, sys_exc_info):
        self.error = error
        self.sys_exc_info = sys_exc_info
        
    def save_to_errorlog(self, message):
        _sTime = datetime.datetime.now().strftime("%Y/%m/%d, %H:%M:%S")
        _exc_type, _exc_value, _exc_tb = self.sys_exc_info
        _traceback = traceback.format_exception(_exc_type, _exc_value, _exc_tb)
        _exception_text = (" \n" + "-"*50 + "\n" + _sTime + " \n" + message +  "\n Exception class: " + str(self.error.__class__) + 
                "\n Exception: " + str(self.error.args) + "\n Traceback: " + str(_traceback) + "\n" + "="*50 + "\n")
        print(_exception_text)
        errorlog = open("log/errorlog.txt", "a")
        errorlog.write(_exception_text)

    def error_from_yahoo_import(self, ticker):
        _sTime = datetime.datetime.now().strftime("%Y/%m/%d, %H:%M:%S")
        errorlog = open("error_yahoo.txt", "a")
        errorlog.write(_sTime + "\t" + ticker)