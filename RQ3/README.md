# Energy Patterns for Web: A Preliminary Study

## Code Source

### DATABASE

The api that keeps track of running test cases needs an SQL database in order to run. You can use the provided sql dump file to create the database and necessary tables:
energy_patterns.sql

### WEB

Contains all files that simulate the websites with energy patterns.
Contains also the api to take track of running test cases:
	/ese/api/v1/testrun

Important: Keep the paths consistent

TO DO:
- Change the parameters in /ese/middleware/class.DBhandler.php according to your database setup

### MAIN_WORKFLOW/selenium_runner_java

Contains the selenium workflows

TO DO:
- Adjust website urls in properties file: /src/main/resources/websites.xml


#### To Compile the code:
`mvn clean package`

To run the code:
`java -cp "target/classes:target/dependency/*" org.ese.Main [testcase] [browser/variant]`

Example:
`java -cp "target/classes:target/dependency/*" org.ese.Main lazyLoading 3`

### MAIN_WORKFLOW

All other files are for running all test cases and plotting the measurement data:

- **run_testcases.py** => Main script
- TestAPI.py => Helper for main script. Do not run this directly.
- manifest.json => Defines the patterns and test cases
- power-logfiles => Folder where the measurement data csv files are saved to. Do not rename!

After-running tasks
- **combine_testdata.py** => Use this to merge all test run data into one single file
- **show_plots.py** => Shows plots of the measurement data
- PLOT_COMMANDS.txt => Here you can find all commands you need to run the former script (show_plots.py)