#!/usr/bin/env python3

###########################################################################
# Merge test data into one file per test case
#
# Usage:
# python combine_testdata.py
#
###########################################################################

import os
import pandas as pd

# DEFINE GLOBAL PARAMETERS
measurement_folder = "power-logfiles"

# Read csv file of variant and extract data
# Returns extracted data as 1-row dataframe
def collect_data(variant):
	var_name = variant[0]
	var_file = variant[1]
	
	# read csv file
	df = pd.read_csv(var_file)
	
	# Divide dataframe into upper and lower part
	df_u = df[~df['RDTSC'].isna()]
	df_l = df[df['RDTSC'].isna()]['System Time']
	
	# Convert System Time of upper part to datetime
	df_u['System Time'] = df_u['System Time'].apply(lambda t : t[::-1].replace(':','.',1)[::-1])
	df_u['System Time'] = pd.to_datetime(df_u['System Time'])
	
	# Split lower part into key => value
	df_l = df_l.str.split(' = ', expand=True)
	
	# Extract temperature values
	avg_temp = df_u["Package Temperature_0(C)"].mean()
	median_temp = df_u["Package Temperature_0(C)"].median()
	min_temp = df_u["Package Temperature_0(C)"].min()
	max_temp = df_u["Package Temperature_0(C)"].max()
	ex_time = df_u["System Time"].mean()
	
	# Set values to numeric
	df_l[1] = pd.to_numeric(df_l[1])
	
	# Add cumulative data to dataframe
	data1 = [['System Time', ex_time],
			['Variant', var_name]]
	data2 = [['Average Package Temperature_0(C)', avg_temp],
			['Median Package Temperature_0(C)', median_temp],
			['Minimum Package Temperature_0(C)', min_temp],
			['Maximum Package Temperature_0(C)', max_temp]]
	
	df_l = pd.concat([pd.DataFrame(data1), df_l, pd.DataFrame(data2)], ignore_index=True)
	
	# Return transposed dataframe
	dft = df_l.T
	dft.columns = dft.iloc[0]
	dft = dft[1:]
	
	return dft


#==========================
# MAIN
#==========================

rootfolder = f"./{measurement_folder}"
if os.path.exists(rootfolder):
	patterns = [d for d in next(os.walk(rootfolder))[1] if d[0] != '.']
else:
	print(f"ERROR: No measurement folder '{measurement_folder}' found!")
	exit()

# Loop over all test patterns
for pattern in patterns:
	# Collect variant folders for provided test case
	testfolder = f"{rootfolder}/{pattern}"
	if os.path.exists(testfolder):
		variants = [d for d in next(os.walk(testfolder))[1] if d[0] != '.']
	else:
		print(f"ERROR: No test folder for pattern '{pattern}' found!")
		exit
			
	# Prepare combined dataframe
	pattern_dataset = pd.DataFrame()
		
	# Read all files, extract and combine data
	manifest = []
	for var in variants:
		var_folder = f"{testfolder}/{var}"
		for filename in os.scandir(var_folder):
			if filename.is_file():
				dft = collect_data((var, filename.path))
				pattern_dataset = pd.concat([pattern_dataset, dft], ignore_index=True)
		
	# Sort final dataset
	pattern_dataset = pattern_dataset.sort_values(by=['System Time'])
	
	# Write collected data into csv file
	outfile_path = f"{testfolder}/pattern_dataset.csv"
	pattern_dataset.to_csv(outfile_path)

print("DONE")