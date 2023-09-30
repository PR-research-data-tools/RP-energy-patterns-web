#!/usr/bin/env python3

###########################################################################
# Show plotted data
#
# Usage:
# python show_plots.py [pattern] "[column]" " [units]"
#
# Example:
# python show_plots.py 0 "Total Elapsed Time (sec)" " sec"
#
# See PLOT_COMMANDS.txt for all available commands
#
###########################################################################

# Import
import os, sys
import pandas as pd
from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool
import bokeh.palettes as bp
from bokeh.transform import factor_cmap


# DEFINE GLOBAL PARAMETERS
measurement_folder = "power-logfiles"
dataset_filename = "pattern_dataset.csv"

# Variant will be color coded.
palette_colors = bp.Category10[4]

variant_colors = {
	'chrome_static' : palette_colors[3],
	'chrome_dynamic' : palette_colors[1],
	'safari_static' : palette_colors[0],
	'safari_dynamic' : palette_colors[2],
	'chrome_eager' : palette_colors[3],
	'chrome_lazy' : palette_colors[1],
	'safari_eager' : palette_colors[0],
	'safari_lazy' : palette_colors[2],
}	
	

show_param = {
	'header' : "[not specified]",
	'unit' : ""
}

# Verify arguments
if len(sys.argv) < 3:
	print("ERROR: Usage = show_plots.py pattern_index show_parameter")
	print()
	exit()
	
if(sys.argv[1].isdigit()):
	pattern_index = int(sys.argv[1])
else:
	print(f"ERROR: '{sys.argv[1]}' is not a number")
	print()
	exit()

show_param['header'] = sys.argv[2]

if len(sys.argv) > 3:
	show_param['unit'] = sys.argv[3]
	


#==========================
# MAIN
#==========================

rootfolder = f"./{measurement_folder}"
if os.path.exists(rootfolder):
	patterns = [d for d in next(os.walk(rootfolder))[1] if d[0] != '.']
else:
	print(f"ERROR: No measurement folder '{measurement_folder}' found!")
	exit()
	
pattern_datasets = {}
glyphs = []
# glyphs.append(p)


# Loop over all test patterns
for pattern in patterns:
	# Collect pattern dataset filepath for this test pattern
	filepath = f"{rootfolder}/{pattern}/{dataset_filename}"
	if os.path.exists(filepath):
		pattern_datasets[pattern] = filepath
		



pattern = list(pattern_datasets.keys())[min(pattern_index, len(pattern_datasets) -1)]

# Read csv file of variant and extract data
var_file = pattern_datasets[pattern]
df = pd.read_csv(var_file)

# Verify that provided header is in the dataframe
if show_param['header'] not in df.columns:
	print(f"ERROR: There is no header '{show_param['header']}' in the dataset.")
	print()
	exit()

# Convert data
df['System Time'] = pd.to_datetime(df['System Time'])

# Append different color to different variants. 
color = list()
for i in range(len(df.index)):
	color.append("#A9A9A9")	
df['Color'] = color

#Assign colors according to variant
for idx in df.index:
	idx_var = df.at[idx,'Variant']
	df.at[idx, 'Color'] = variant_colors[idx_var] if idx_var in variant_colors else df.at[idx, 'Color']
	
	
# Create color map
variants = sorted(df['Variant'].unique())
variant_cmap = factor_cmap('Variant', palette=bp.Category10[4], factors=variants)

#Create the ColumnDataSource by first creating a dictionary
data = {
	'Time': list(df['System Time']),
	'Param': list(df[show_param['header']]),
	'Variant': list(df['Variant']),
	'Color': list(df['Color'])
}
source_scatter = ColumnDataSource(data)

#For interaction we will use "Lasso Selection" and "Box Selection" tools.
TOOLS="lasso_select, box_select, reset"

#Create figure for scatterplot.
p = figure(plot_width=900, plot_height=400,
			x_axis_type="datetime",
			toolbar_location="above",
			active_drag="box_zoom",
			title=f"{pattern} - {show_param['header']}")

p.xaxis.axis_label = 'Test Run'
p.yaxis.axis_label = show_param['header']
p.sizing_mode = "stretch_both"

#Create hover tool.
hover = HoverTool(tooltips = [
	("Variant", "@Variant"),
	("Param", "@Param"+show_param['unit']),
	("Time", "@Time{%T.%3N}")
],
					formatters={'@Time': 'datetime'})
p.add_tools(hover)

#Create the scatterplot
scatter = p.scatter(x='Time', y='Param',
					# color=variant_cmap,
					color='Color',
					alpha=0.7,
					size=10,
					hit_dilation=3,
					source=source_scatter,
					legend_group='Variant')



show(p)





def create_single_plot(pattern_index):
	pattern = list(pattern_datasets.keys())[pattern_index]
	
	# Read csv file of variant and extract data
	var_file = pattern_datasets[pattern]
	df = pd.read_csv(var_file)
	
	# Verify that provided header is in the dataframe
	if show_param['header'] not in df.columns:
		print(f"ERROR: There is no header '{show_param['header']}' in the dataset.")
		print()
		exit()
		
	# Convert data
	df['System Time'] = pd.to_datetime(df['System Time'])
	
	# Append different color to different variants. 
	color = list()
	for i in range(len(df.index)):
		color.append("#A9A9A9")	
	df['Color'] = color
			
	#Assign colors according to variant
	for idx in df.index:
		idx_var = df.at[idx,'Variant']
		df.at[idx, 'Color'] = variant_colors[idx_var] if idx_var in variant_colors else df.at[idx, 'Color']
			
			
	# Create color map
	variants = sorted(df['Variant'].unique())
	variant_cmap = factor_cmap('Variant', palette=bp.Category10[4], factors=variants)
			
	#Create the ColumnDataSource by first creating a dictionary
	data = {
		'Time': list(df['System Time']),
		'Param': list(df[show_param['header']]),
		'Variant': list(df['Variant']),
		'Color': list(df['Color'])
	}
	source_scatter = ColumnDataSource(data)
			
	#For interaction we will use "Lasso Selection" and "Box Selection" tools.
	TOOLS="lasso_select, box_select, reset"
			
	#Create figure for scatterplot.
	p = figure(plot_width=900, plot_height=400,
				x_axis_type="datetime",
				toolbar_location="above",
				active_drag="box_zoom",
				title=f"{pattern} - {show_param['header']}")
			
	p.xaxis.axis_label = 'Test Run'
	p.yaxis.axis_label = show_param['header']
	p.sizing_mode = "stretch_both"
			
	#Create hover tool.
	hover = HoverTool(tooltips = [
		("Variant", "@Variant"),
		("Param", "@Param"+show_param['unit']),
		("Time", "@Time{%T.%3N}")
	],
						formatters={'@Time': 'datetime'})
	p.add_tools(hover)
			
	#Create the scatterplot
	scatter = p.scatter(x='Time', y='Param',
						# color=variant_cmap,
						color='Color',
						alpha=0.7,
						size=10,
						hit_dilation=3,
						source=source_scatter,
						legend_group='Variant')
			