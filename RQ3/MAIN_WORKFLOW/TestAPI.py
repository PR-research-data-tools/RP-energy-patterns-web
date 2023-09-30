#!/usr/bin/env python3

###########################################################################
#
# Helper methods to communicate with web api that logs progress
#
###########################################################################

# TODO: Adjust url of api that tracks progress
API_URL = 'https://YOURDOMAIN/ese/api/v1/testrun/'

###########################################################################

import json, requests

class TestAPI:
	
	apiUrl = API_URL
	apiHeaders = {'Content-type': 'application/json'}
	
	def __init__(self, id, name):
		self.id = id
		self.name = name
	
	def _post_request(self, jsonData):
		return False #requests.post(self.apiUrl, data=jsonData, headers=self.apiHeaders)
	
	
	# Send http request
	def _sendRequest(self, method: str, rawData: dict):
		jsonData = json.dumps(rawData)
		if method == 'post':
			response = requests.post(self.apiUrl, data=jsonData, headers=self.apiHeaders)
		elif method == 'put':
			response = requests.put(self.apiUrl, data=jsonData, headers=self.apiHeaders)
		elif method == 'get':
			response = requests.get(self.apiUrl)
		else:
			response = False
		
		if response:
			print("Success.")
		else:
			print("Error: could not handle request, reason:", response.json())
		
		print("--")
		return response

	
	def start_new_testrun(self):
		rawData = {
			"id": self.id,
			"name": self.name
		}
		print(f"Submitting new testrun with id={self.id} and name='{self.name}' to api...")
		return self._sendRequest('post', rawData)
	
	
	def run_variant(self, variant, name):
		rawData = {
			"id": self.id,
			"action" : "run",
			"variant" : variant,
			"name": name
		}
		print(f"Submitting new run of variant {variant} ({name}) for testrun id={self.id} to api...")
		return self._sendRequest('put', rawData)
	
	
	def end_testrun(self):
		rawData = {
			"id": self.id,
			"action" : "end"
		}
		print(f"Submitting completion of testrun id={self.id} to api...")
		return self._sendRequest('put', rawData)
	
