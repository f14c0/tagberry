import logging
class LogWrapper():
    def __init__(self):
        """Initializes the root logger"""
        self._logger = logging.getLogger("EPCLogger")
        # create file handler which logs even debug messages
        self._fh = logging.FileHandler('EPCManager.log')
        self._ch = logging.StreamHandler()
        
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self._fh.setFormatter(formatter)
        self._ch.setFormatter(formatter)
        # add the handlers to the logger
        self._logger.addHandler(self._fh)
        self._logger.addHandler(self._ch)
        
    def debug(self,message,exception=None):
        self._logWriter(logging.DEBUG,message,exception)
    def info(self,message,exception=None):
        self._logWriter(logging.INFO,message,exception)
    def warning(self,message,exception=None):
        self._logWriter(logging.WARN,message,exception)
    def fatal(self,message,exception):
        self._logWriter(logging.FATAL,message,exception)
    def error(self,message,exception):
        self._logWriter(logging.ERROR,message,exception)
    def _logWriter(self,level,message,exception=None):
        
        self._logger.setLevel(level)
        self._fh.setLevel(level)
        self._ch.setLevel(level)
        if(exception!=None):
            exFormatted = self._formatException(exception)
            
        msg = "%s%s" % (message,exFormatted)
        
        if(level==logging.DEBUG):
           logging.debug(msg) 
        elif(level==logging.INFO):
           logging.info(msg) 
        elif(level==logging.WARN):
           logging.warn(msg) 
        elif(level==logging.FATAL):
           logging.fatal(msg) 
        if(level==logging.ERROR):
           logging.error(msg) 
           
    def _formatException(self,exception):
        pass       