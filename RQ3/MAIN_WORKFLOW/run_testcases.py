#!/usr/bin/env python3

###########################################################################
# Main function
# Orchestrates the whole process and logs progress
# to web database through the provided api
#
# Usage:
# python run_testcases.py executions_per_variant test_case [-nowait]
#
###########################################################################

# Change this if you do not want to compile the java code at runtime
COMPILE_JAVA = True

###########################################################################


import sys
import random
import time
import os
import uuid
from TestAPI import *


# Common file parameters
COMMON_BASE_PATH = os.getcwd()
WORKFLOW_DIR = "selenium_runner_java"
LOG_OUTPUT_DIR = "power-logfiles"
OUT_FILE_PREFIX = "run"
MANIFEST_FILE = "manifest.json"

# Common test setup
PL_RESOLUTION = 500
SLEEP_POST_COMPILE = 10
SLEEP_BETWEEN_TESTS = 30

if len(sys.argv) > 3:
	if sys.argv[3] == "-nowait":
		SLEEP_POST_COMPILE = 0
		SLEEP_BETWEEN_TESTS = 1



# -------------------------------
# Import manifest
# -------------------------------
def import_manifest() -> dict:
	with open(MANIFEST_FILE, "r") as json_file:
		manifest = json.load(json_file)
	return manifest



# -------------------------------
# Collect and verify test patterns
# -------------------------------
def collect_patterns(manifest: dict, pattern: str) -> list:
	patterns_to_run = []
	
	if pattern is not None:
		patterns_to_run = [pattern]
		if pattern not in manifest:
			print(f"ERROR: Unknown pattern '{pattern}'!")
			print("Valid patterns are:")
			for t in manifest.keys():
				print("- " + t)
			exit()
	else:
		# Run all patterns
		for t in manifest.keys():
			patterns_to_run.append(t)
	
	return patterns_to_run	




# ---------------------------------------------------
# Compile test code
# ---------------------------------------------------
def compile_testcode(workflow_path):
	# compile java
	print("Compiling java and building package...")
	os.system("mvn package")
	print("... done.")
	print()



# ---------------------------------------------------
# Create output folders and prepare variant record
# ---------------------------------------------------
def prepare_pattern_variants(manifest: dict, pattern: str, log_output_base_path: str) -> list:
	create_folder_if_not_exists(log_output_base_path)
	
	variants = []
	for var in manifest[pattern]['variants']:
		output_path = f"{log_output_base_path}/{var['shortname']}"
		var_info = {
			"path": output_path,
			"fullname" : var['fullname'],
			"count": 0
		}
		variants.append(var_info)
		create_folder_if_not_exists(output_path)
	
	return variants

			


# -------------------------------
# Create running order
# -------------------------------
def create_running_order(manifest: dict, testcase: str, executions: int) -> list:
	running_order = []
	
	project_variants = len(manifest[testcase]['variants'])
	
	for variant in range(project_variants):
		for i in range(executions):
			running_order.append(variant)
			
	random.shuffle(running_order)
	
	return running_order



# ---------------------------------------------------
# Create a new folder if it does not already exist
# ---------------------------------------------------
def create_folder_if_not_exists(path):
	if not os.path.exists(path):
		os.mkdir(path)



# ---------------------------------------------------
# Sleep to cool down
# ---------------------------------------------------
def cool_down(duration):
	print(f"waiting for {duration} seconds to cool down...", end="", flush=True)
	time.sleep(duration)
	'''
	for i in range(duration):
		time.sleep(1)
		print(".", end="", flush=True)
	'''
	print("done")
	



# -------------------------------
# MAIN
# -------------------------------
def main():
	
	# Verify arguments
	if len(sys.argv) < 2:
		print("Usage: run_testcases.py executions_per_variant pattern")
		exit()
	
	if(sys.argv[1].isdigit()):
		executions_per_project = int(sys.argv[1])
	else:
		print(f"'{sys.argv[1]}' is not a number")
		exit()
	
	manifest = import_manifest()
	
	if len(sys.argv) > 2:
		patterns_to_run = collect_patterns(manifest, sys.argv[2])
	else:
		patterns_to_run = collect_patterns(manifest, None)
	
	# Define workflow path
	workflow_path = f"{COMMON_BASE_PATH}/{WORKFLOW_DIR}"
	
	# change to workflow directory
	os.chdir(workflow_path)
	
	# Compile java
	if (COMPILE_JAVA):
		compile_testcode(workflow_path)
		cool_down(SLEEP_POST_COMPILE)
		print()
	
	# Test all provided patterns
	for pattern in patterns_to_run:
		pattern_id = str(uuid.uuid4())
		print("***********************************************************")
		print(f"* Testing pattern '{manifest[pattern]['name']}'")
		print(f"* uuid = {pattern_id}")
		print("***********************************************************")
		print()
		
		# Compose paths and counters
		log_output_base_path = f"{COMMON_BASE_PATH}/{LOG_OUTPUT_DIR}/{pattern}"
		variants = prepare_pattern_variants(manifest, pattern, log_output_base_path)
		running_order = create_running_order(manifest, pattern, executions_per_project)
		
		# Prepare for running test case
		command_base = f"java -cp \"target/classes:target/dependency/*\" org.ese.Main {pattern} "
		counter = 1
		zero_fill = executions_per_project // 10 + 1
		
		# Submitting testcase info to testmonitor API
		api = TestAPI(pattern_id, manifest[pattern]['name'])
		api.start_new_testrun()
		
		
		# run code
		for variant in running_order:
			print(f"Running test {counter} of {len(running_order)}:")
			print()
			
			variants[variant]['count'] += 1
			var_info = variants[variant]
			
			log_file_path = f"{var_info['path']}/{OUT_FILE_PREFIX}-{str(var_info['count']).zfill(zero_fill)}.csv"
			java_command = command_base + str(variant)
			powerlog_command = f"powerlog -resolution {PL_RESOLUTION} -file \"{log_file_path}\" -cmd {java_command}"
			
			# It's getting hot in here...
			cool_down(SLEEP_BETWEEN_TESTS)
			
			
			# PRESS THE RED BUTTON => EXECUTE!
			os.system(powerlog_command)
			
			
			# Submitting variant info to testmonitor API
			api.run_variant(variant, var_info['fullname'])
			
			print("---")
			
			counter += 1
		
		
		# Submitting completion to testmonitor API
		api.end_testrun()
		
		print("***********************************************************")
		print("*                          DONE                           *")
		print("***********************************************************")
		print()
	

	# Done with everything
	
	print("DONE!")



# MAIN

main()