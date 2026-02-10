"""

This file is for logging set up and for storing helper functions.

"""

import logging   #This allows for displaying whatever is happening.
import os		 #This is for creating paths and folders.
import sys		 #For allowing for importing from the src folder.

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))		#This line is for enabling the import from src folder.

from src.config import Config

def setup_logger(name=None,level=None,log_file=None):		#This method is for setting up a logger. It receives and uses 3 pieces of inputs. name - This will be the name of the logger, level - The level of innformation given for each log (DEBUG,INFO,WARNING,ERROR), log_file - this is the place where to write the log output.
	
	logger = logging.getLogger(name or "automation")		#Gets a logger using the logging.getLogger function. The name of the logger passed in the parameter is considered. If the name does not exist then it will default to the 'automation' logger.

	logger.setLevel(level or getattr(logging,Config.LOG_LEVEL.upper(),logging.INFO))	#This sets up the level of information to be displayed when logging is done. If the level parameter is None then the getattr is used for getting the logging level from the Config file. If even from the Config file, the level does not exist then the third parameter logging.INFO in the getattr will be used.

	if logger.handlers:	
		return logger	#This if condition is in place to return the logger object if the logger is already initialized. This avoids logger to be initialized again and again.

	formatter = logging.Formatter(	#Using the Formatter in-built function to design how the log messages are to be displayed. The variable formatter is the object created to hold that design for displaying the message.
		"%(asctime)s - %(name)s - %(levelname)s - %(message)s"	#This is the format in which the log message is supposed to come out.
	)

	console_handler = logging.StreamHandler()	#A handler is created to send the messages to the console. The StreamHandler is a handler in-built method in logging library. I am storing that handler into the console_handler.

	console_handler.setFormatter(formatter)		#Applying the format we created above to the console_handler so that messages appear in that format in the console.
	
	logger.addHandler(console_handler)			#This establishes the connection between the logger and the console_handler. In other words, I am telling the logger, when you create and log a message, I want you to send the same message to the console_handler so that the console_handler can display that message in the console.

	log_path = log_file or Config.LOG_FILE_PATH #log_path will get the path of the file where the logs are to be written. It will get it from log_file parameter passed in this method, failing which it will default to the LOG_FILE_PATH in the Config class in config.py.

	log_dir = os.path.dirname(log_path)			#This is the part where the directory of the log file where logging file is will be stored inside log_dir.

	if log_dir and not os.path.exists(log_dir): #This if condition is created to deal with a situation where there is no dedicated folder to contain the logging file.
		os.makedirs(log_dir)					#If there is no folder for the logging file then a new folder will be created for that purpose.

	file_handler = logging.FileHandler(log_path,encoding="utf-8")	#I created a second handler with the help of FileHandler in-built method in the logging library to write the logs inside the logging file at the log_path path in the form of utf-8. That file handler is stored inside file_handler variable.

	file_handler.setFormatter(formatter)		#I am applying the design I created inside the formatter we created earlier to the file_handler so that I can see the messages exactly like how it is designed in the formatter.
	
	logger.addHandler(file_handler)				#This establishes the connection between the logger and the file_handler. In other words, I am telling the logger, when you create and log a message, I want you to send the same message to the file_handler so that the file_handler can store that message inside the logging file.

	return logger								#This returns the logger.


def get_test_data_path(filename):				#In simple language, this method is for taking a file name and finding and returning the path to that file name.
	data_dir = Config.TEST_DATA_DIR				#Retrieves the test data directory path from config (e.g. "data") and stores it in data_dir.
	return os.path.join(data_dir,filename)		#This will glue the directory path of the file with the file name and return the complete path.



		