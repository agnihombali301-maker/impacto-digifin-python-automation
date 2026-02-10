"""
API Client module for the automation framework.

This file is the central place for all API communication. Tests use this client
to talk to the REST API (default: jsonplaceholder.typicode.com). If the API
address or how we send requests changes, we only need to edit this file.
"""


import requests					#Library for sending GET and POST HTTP requests to API.
import sys						#For finding the path to src when we run the tests.
import os						#For finding the path to src when we run the tests.

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))				#It adds the project folder to the list of places Python looks when you import something, so from src.config import Config works.

from src.config import Config	#To import the settings from the Config class in config.py in src.



class APIError(Exception):												#creating our own error exception class inheriting from Exception class
	def __init__(self,message,status_code=None,response=None):			#message is our custom message, status code is the error code (404, 401 etc), response contains the actual error response from the server.
		self.message = message											
		self.status_code = status_code
		self.response = response
		super().__init__(self.message)									#This makes this class behave exactly like how the Exception class would behave.

class APIClient:														#The class that knows "how" to call the API
	def __init__(self,base_url=None,timeout=None):						
		self.base_url = base_url or Config.get_base_url()				#Either the base url that comes to this function or the base url from config.py in src.
		self.timeout = timeout or Config.get_timeout()					#Either the timeout that comes to this function or the timeout from config.py in src.
		self.session = requests.Session()								#requests.Session() makes one session to make multiple requests rather than making many connections every time a request has to be made.
		# Set User-Agent header so requests look like they come from a browser. Helps when an API (e.g. reqres.in) is behind Cloudflare and may block scripted requests.
		self.session.headers.update({
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
		})

	def _build_url(self,path):											#Glues the base url with the path.
		path = path.strip('/')											#Removes leading/trailing '/' from the path.
		base = self.base_url.rstrip('/')								#Removes the trailing '/' from the base url (e.g. https://jsonplaceholder.typicode.com).
		return f"{base}/{path}"											#Returns the full URL (e.g. https://jsonplaceholder.typicode.com/users).

	def get(self,path,params=None):															#This method is asking for resources from the API and returns what that API has responded.
		url = self._build_url(path)															#This is an attempt to make the complete URL with the proper path and keep it ready and stored in url.
		try:																				#Try block is for attempting to execute certain code. If the code fails or gives an error then the except block after the try block will take over and convey what error has happened.
			response = self.session.get(url,params=params,timeout=self.timeout)				#There is a request made to the API here in the form of get request and that response is stored in response variable.
			self._raise_for_error(response,url)												#This method is defined below. Raises APIError if status code >= 400.
			return response																	#This returns the response which is the outcome of this get method defined here.
		except requests.RequestException as e:												#If there was a challenge in the try block (e.g. network error, timeout) then this will get executed.
			raise APIError(f"GET request failed: {e}", response=None)						#The 'e' holds the details of the potential error and that will be displayed in the output.
	
	def post(self,path,json=None,data=None):												#This method is for giving information either in the form of JSON or data.
		url = self._build_url(path)															#This is an attempt to make the complete URL with the proper path and keep it ready and stored in url.
		try:																				#Try block is for attempting to execute certain code. If the code fails or gives an error then the except block after the try block will take over and convey what error has happened.
			response = self.session.post(url,json=json,data=data,timeout=self.timeout)		#There is a request made to the API here in the form of post request and that response is stored in response variable.
			self._raise_for_error(response,url)												#This method is defined below. Raises APIError if status code >= 400.
			return response																	#This returns the response which is the outcome of this post method defined here.
		except requests.RequestException as e:												#If there was a challenge in the try block (e.g. network error, timeout) then this will get executed.
			raise APIError(f"POST request failed: {e}",response=None)						#The 'e' holds the details of the potential error and that will be displayed in the output.

	def _raise_for_error(self,response,url):																		#Defining the _raise_for_error method for catching the error and providing the proper error message so that the output is not ugly and it does not crash.
		if response.status_code >= 400:																				#HTTP status codes 400+ indicate client or server errors (e.g. 404 Not Found, 403 Forbidden, 500 Internal Server Error).
			raise APIError(																							#Invoking the APIError custom exception that we created above.
				message=f"API returned error: {response.status_code} for {url}. Response: {response.text}",			#Making our custom error message that needs to be displayed when the error occurs.
				status_code=response.status_code,																	#Storing the status code for future use (e.g. in tests we assert error_info.value.status_code == 404).
				response=response																					#Storing the full response object for future inspection (e.g. response body, headers).
			)

	