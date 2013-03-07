import logging, sys

class SingleLevelFilter(logging.Filter):
    def __init__(self, passlevel, reject):
        self.passlevel = passlevel
        self.reject = reject

    def filter(self, record):
        if self.reject:
            return (record.levelno != self.passlevel)
        else:
            return (record.levelno == self.passlevel)

class Logger:
	def __init__(self, dest):	
		self.h1 = logging.FileHandler(dest)
		f1 = SingleLevelFilter(logging.INFO, False)
		self.h1.addFilter(f1)
		self.rootLogger = logging.getLogger()
		self.rootLogger.addHandler(self.h1)
		
		self.h2 = logging.FileHandler(dest)
		f2 = SingleLevelFilter(logging.INFO, True)
		self.h2.addFilter(f2)
		self.rootLogger.addHandler(self.h2)

	def start(self):
		return self.rootLogger

	def stop(self):
		self.h1.close()
		self.h2.close()
	
