"""
Test file for user-related API endpoints.

Tests target the jsonplaceholder.typicode.com API (configured via Config; reqres.in
was replaced due to Cloudflare 403 blocking automated requests). This file includes:
  - GET all users
  - GET single user by ID
  - POST create user (name, username, email)
  - Negative test: GET non-existent user (expects APIError with status_code 404)
"""


import pytest	#This is for running tests.
import sys		#This is to find the src folder.
import os		#This is for fixing and creating proper paths.

sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))	#I want the APIClient class from the src/api_client. That's why I am adding the project root to Python's search path.

from src.api_client import APIClient,APIError		#I need the APIClient class and the custom error APIError here.
from src.utils import setup_logger					#For setting up logging.

logger = setup_logger("api_tests")					#Setting up a logger here using the function setup_logger from utils.py.

class TestAPIUsers:														#This class groups all the user tests in one place.

	def setup_method(self):												#Created a method what will start whenever the pytest will run a test.									
		self.client = APIClient()										#A new client will be created when a test is run by pytest.
		logger.info("Test setup: Created new APIClient instance")		#Logger object coming from utils.py will invoke it's .info function to display the message in the console and write that same message inside the logging file using the console_handler and file_handler respectively.

	def test_get_all_users(self):										#This test is designed to get the list of all the users.
		logger.info("Starting test: Get all users")						#This is to log and indicate the that the test to get all the users has started.
		response = self.client.get("users")								#The control will go to GET method in the api_client.py to get the response, failing which there will be an exception raised.

		assert response.status_code == 200								#Checks if the status code of the response received is 200 or not. If not then there will be an assertion error.

		data = response.json()											#This converts the JSON format of the users' data into the dictionary format and stores it in the data variable.

		#The small code below is just to see the data being retrieved from the API.

		

		print("\n=== LIST OF USERS ===")
		for user in data:
			print(f"\n{user['id']}------{user['name']}------{user['username']}------{user['email']}---\n")
		print("=========================\n")


		


		# jsonplaceholder.typicode.com returns an array directly (not wrapped in "data")
		assert isinstance(data,list)									#This checks that the response is a list (array of users). 
		assert len(data) > 0											#This checks that the list is not empty. 

		for user in data:												#This is for iterating through each and every user inside the list.
			assert "id" in user											#It checks if there is the key 'id' in the dictionary corresponding to the user in this iteration.
			assert "email" in user										#It checks if there is the key 'email' in the dictionary corresponding to the user in this iteration.
			assert "name" in user										#It checks if there is the key 'name' in the dictionary corresponding to the user in this iteration.
			assert "username" in user									#It checks if there is the key 'username' in the dictionary corresponding to the user in this iteration. 

		logger.info(f"Test passed: Retrieved {len(data)} users")		#This logs the message stating that the retrieval of the user data was successful.
		
	def test_get_single_user(self):										#This test is designed to Get only one specific user. 
		logger.info("Starting test: Get single user")
		user_id = 2														#I am specifying that I want the information of only user ID number 2. 
		response = self.client.get(f"users/{user_id}")					#The control will go to the GET method in the api_client.py to get the response, failing which there will be an exception raised. 

		assert response.status_code == 200, f"Expected 200, got {response.status_code}"								#Checks if the status code of the response received is 200 or not. If not, then there will be an assertion error. 

		data = response.json()																						#This converts the JSON format of the user data into a dictionary format and stores it in the data variable. 

		# jsonplaceholder.typicode.com returns the user object directly (not wrapped in "data")
		user = data																									#The response is the user object directly.


		#The small code below is just to see the data being retrieved from the API.

		

		print("\n=== SINGLE USER DETAILS ===")
		print(f"{user['id']}---{user['name']}---{user['username']}---{user['email']}---")
		print("==============================\n")

		


		assert "id" in user, "User should have 'id' field"												#This checks if there is a key called 'id' in the user dictionary.
		assert "email" in user, "User should have 'email' field"										#This checks if there is a key called 'email' in the user dictionary.
		assert "name" in user, "User should have 'name' field"											#This checks if there is a key called 'name' in the user dictionary.
		assert "username" in user, "User should have 'username' field"									#This checks if there is a key called 'username' in the user dictionary. 

		assert user["id"] == user_id, f"Expected user ID {user_id}, got {user['id']}"				#This checks if the user information extracted corresponds to the user ID number 2 or not. 
		logger.info(f"Test passed: Retrieved user {user_id} - {user.get('name')}")					#This logs that the test has been passed and the user ID number 2 has been retrieved with its information. 

	def test_create_user(self):																							#This test is designed to create a user.
		logger.info("Starting test: Create user")																		#Logs a message that the test has been started.

		user_data = {																									#I have created some data for the new user.
			"name":"John Doe",
			"username":"johndoe",
			"email":"john.doe@example.com"
		}

		response = self.client.post("users",json=user_data)																#The control will go to the POST method in the api_client.py to get the response. Failing which, there will be an exception raised. 												
		
		assert response.status_code == 201, f"Expected 201, got {response.status_code}"									#This checks if the status code is 201 or not. If it is not 201, then the appropriate message is displayed. 

		data = response.json()																							#The JSON format that is present in the response that is containing the new user information is converted to a dictionary and then passed on to the variable data.

		#The small code below is just to see the data being retrieved from the API.

																													

		print("\n=== CREATED USER DETAILS ===")
		print(f"{data['id']}---{data['name']}---{data['username']}---{data['email']}---")
		print("==============================\n")

		



		assert "name" in data,"Response should have 'name' field"														#This checks if there is a key called 'name' in the data dictionary.
		assert "username" in data,"Response should have 'username' field"												#This checks if there is a key called 'username' in the data dictionary or not. 
		assert "email" in data,"Response should have 'email' field"														#This checks if there is a key called 'email' in the data dictionary or not. 
		assert "id" in data,"Response should have 'id' field"															#This checks if there is a key called 'id' in the data dictionary or not. 

		assert data["name"] == user_data["name"],f"Expected name '{user_data['name']}', got '{data['name']}'"			#This checks if the user that we created is indeed the user we created or not. 
		assert data["email"] == user_data["email"],f"Expected email '{user_data['email']}', got '{data['email']}'"		#This checks if the email of the user that we created is indeed the email of the user that we created or not. 

		logger.info(f"Test passed: Created user '{data['name']}' with ID {data['id']}")									#This logs the message that the test has been passed. 

	def test_get_user_not_found(self):																					#This test is designed to check the negative test case whether the user is not found.
		logger.info("Starting test: Get user not found (negative test)")												#This is to log a message that the test has been started. 
		non_existent_id = 99999																							#I am creating an irrelevant and fake ID. 

		# jsonplaceholder.typicode.com returns 404 for non-existent users. Our client raises APIError for status >= 400.
		with pytest.raises(APIError) as error_info:																		#We expect APIError because the user does not exist. If no APIError is raised, the test fails.
			self.client.get(f"users/{non_existent_id}")																	#The control will go to the `get` method in the `api_client.py` to get the response, failing which there will be an exception raised. 

		assert error_info.value.status_code == 404,f"Expected 404, got {error_info.value.status_code}"					#I am expecting a 404 status code here because the user is not found. If I am not able to get the 404 error, then there is an alternative that says "Expected 404, got something else instead."
		
		logger.info(f"Test passed: Correctly raised APIError with status 404 for non-existent user {non_existent_id}")  #This will log the message that the test has been passed, and we have indeed got the API error with the status code of 404. 
		
		

		