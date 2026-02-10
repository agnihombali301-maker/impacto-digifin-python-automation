"""
This is the part that specifies the configuration of this project.
This part is responsible for the settings of this project.
It includes project settings for
	- API base URLs,
	- timeouts
	- environment specific variables
"""

import os     #This is for accessing the environment variables
from dotenv import load_dotenv     #This is for loading variables from a .env file.

load_dotenv()          #Loads environment variable from .env file.

class Config:       #This class is created to centralize all the settings required for this project.
	# Default API: jsonplaceholder.typicode.com (public test API; reqres.in was switched due to Cloudflare 403 blocking automated requests)
	BASE_URL = os.getenv("API_BASE_URL","https://jsonplaceholder.typicode.com") #Sets the base url as API_BASE_URL as first priority. If API_BASE_URL is empty then it uses this default.
	REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT","10"))  #Sets how long to wait for the API response. If the REQUEST_TIMEOUT is not available then request timeout defaults to 10.
	LOG_LEVEL = os.getenv("LOG_LEVEL","INFO")   #When the project runs, this decides the ammount of information provided about the status of the operation in real time. Defaults to INFO level if LOG_LEVEL is empty.
	LOG_FILE_PATH = os.getenv("LOG_FILE_PATH","logs/automation.log")      #This sets where the logging information is stored. Defaults to logs/automation.log is LOG_FILE_PATH has nothing.
	TEST_DATA_DIR = os.getenv("TEST_DATA_DIR","data")        #Place where the test files are kept to test automation.

	@classmethod				#For creating a method without creating an object. Provides a simpler way to access the setting.
	def get_base_url(cls):		
		return cls.BASE_URL		#Objective of this method is to return the base url.

	@classmethod						#For creating a method without creating an object. Provides a simpler way to access the setting.
	def get_timeout(cls):
		return cls.REQUEST_TIMEOUT		#Objective of this method is to return the time out value.




