import json							#For dealing with JSON format.
import pytest						#For conducting tests on anything that starts with "test"
import sys							#This we are importing so that we can access the files that are there in another folder, which is a sibling folder.
import os							#This is for getting a clear and proper path.

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))				#This is so that test_data_driven.py can access the api_client.py file in the src folder to eventually get access to the APIClient class.

from src.api_client import APIClient															#Importing the APIClient class from the src folder's api_client.py file.
from src.utils import setup_logger,get_test_data_path											#Importing setup_logger and get_test_data_path methods from the src.utils.py file.

logger = setup_logger("data_driven_tests")														#I am creating a logger with the name data_driven_tests. 

class TestDataDrivenUsers:																		#I'm creating a class TestDataDrivenUsers.
	def setup_method(self):																		#The setup_method will be called in the beginning of every test.
		self.client = APIClient()																#For every test, a new object of the class APIClient will be created.
		logger.info("Test setup: Created new APIClient instance")								#This message will be logged on the console every time a new test is being done. This will indicate that I have created an new APIClient instance for every test. 

	def test_create_users_from_data_file(self):													#This method is created to test if I can create users from the data file which is users_to_create.json in the data folder.
		logger.info("Starting data-driven test: Create users from JSON file")					#This logs a statement in the console stating that creation of the user from the JSON file has been started. 

		data_file_path = get_test_data_path("users_to_create.json")								#This gives the path of the users_to_create.json file. It stores that path in the data_file_path.
		with open(data_file_path,'r',encoding='utf-8') as f:									#This line opens the users_to_create.json in read mode and in the encoding of UTF-8 so that special characters can be read properly.
			users_data = json.load(f)															#This reads the JSON from the file, then it converts it into a Python list of dictionaries, and then it stores it in users_data. 

		for user_data in users_data:															#Now I am going to iterate through the users_data.
			response = self.client.post("users",json=user_data)									#This is going to attempt to create the user by using the post method in the api_client.py under APIClient class. The acknowledgement is stored in the response variable. 

			assert response.status_code == 201,f"Expected 201, got {response.status_code}"		#This checks whether the response status code is 201 or not. If it is not, then it will show an appropriate message. 

			created_user = response.json()														#The API's reply, which is in JSON text, is converted to a Python dictionary and saved in the created user. 

			assert "id" in created_user, "Response should have 'id' field"						#This is to check if there is a key called 'ID' in the dictionary that is denoted by created_user.
			assert "name" in created_user, "Response should have 'name' field"					#This is to check if there is a key called 'name' in the dictionary that is denoted by the created_user.
			assert "username" in created_user, "Response should have 'username' field"			#This is to check if there is a key called 'username' in the created_user dictionary.
			assert "email" in created_user, "Response should have 'email' field"				#This is to check if there is a key called 'email' in the created_user dictionary. 

			assert created_user["name"] == user_data["name"]									#This is to verify that the user created in the API has the same name as the one we have given the API.
			assert created_user["username"] == user_data["username"]							#This is to verify that the user created in the API has the same username as the one we have given the API.
			assert created_user["email"] == user_data["email"]									#This is to verify that the user created in the API has the same email as the one we have given in the API. 

			logger.info(f"Created user: {created_user['name']} (ID: {created_user['id']})")		#This is to show on the console that the user with this name and this ID has been created, and it matches what we have sent to the API. 

		logger.info(f"Test passed: Successfully created {len(users_data)} users from data file")#This displays a log message stating that our test has passed and created the list of users that are there in the users_to_create.json. 