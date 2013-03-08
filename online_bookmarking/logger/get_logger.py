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
		self.file_handler = logging.FileHandler(dest)

		single_level_filter = SingleLevelFilter(logging.INFO, False)
		self.file_handler.addFilter(single_level_filter)
		
		self.rootLogger = logging.getLogger()
		self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		self.file_handler.setFormatter(self.formatter)
		self.rootLogger.addHandler(self.file_handler)
		
	def start(self):
		return self.rootLogger

	def stop(self):
		self.file_handler.close()

	
