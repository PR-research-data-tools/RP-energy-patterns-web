# Energy Patterns for Web:  An Exploratory Study

## Code Source

### DATABASE

The api that keeps track of running test cases needs an SQL database in order to run. You can use the provided sql dump file to create the database and necessary tables:
energy_patterns.sql

One can install MySQL and setup the localhost with the username and password by following steps:
```
    $ brew install mysql
    $ brew services start mysql
    $ mysql -u root -p
    "Enter the root password."
    $ mysql> create user 'username'@'localhost' IDENTIFIED BY 'pa55w0rd';
    $ mysql> CREATE DATABASE energy_patterns;
    $ mysql> GRANT ALL PRIVILEGES ON energy_patterns.* TO 'username'@'localhost';
    $ mysql> FLUSH PRIVILEGES;
    $ exit
```
Once the username and password is setup, one can import the SQL dump file by following the given steps. It will output the two tables \emph{ese_test_variants} and \emph{ese_testruns}.

```
    $ mysql -u username -p energy_patterns < /Path/to/DATABASE/energy_patterns.sql
    $ mysql -u username -p
    $ mysql> USE energy_patterns;
    $ mysql> SHOW TABLES;
+-------------------------------+
| Tables_in_energy_patterns |
+-------------------------------+
| ese_test_variants             |
| ese_testruns                  |
+-------------------------------+
```

### WEB

Contains all files that simulate the websites with energy patterns.
Contains also the API to take track of running test cases:
/ese/api/v1/testrun

Important: Keep the paths consistent

TO DO:
- Change the parameters in /ese/middleware/class.DBhandler.php according to your database setup

### MAIN_WORKFLOW/selenium_runner_java
- Versions: 
    - Java: openjdk 19.0.1
    - Maven: 3.9.0

- Contains the selenium workflows that run the simulations of pattern scenarios (visit website and interact with it)! The measurements are captured by powerlog and orchestrated by the python scripts, mainly `run_testcases.py`.

TO DO:
- Adjust demo website urls in properties file: `/src/main/resources/websites.xml`


#### To Compile the code:
`mvn clean package`

To run the code:
`java -cp "target/classes:target/dependency/*" org.ese.Main [testcase] [browser/variant]`

Example:
`java -cp "target/classes:target/dependency/*" org.ese.Main lazyLoading 3`

### MAIN_WORKFLOW

All other files are for running all test cases and plotting the measurement data:

- Versions: 
    - Python: 3.11
    - PowerLog: 3.7.0
    - Google Chrome: 113.0.5672.92 
    - Safari version 15.6.1.
    - MacOS: Catalina 10.15.7

- **requirements.txt** => requirement file for python virtual enviornment. 

- **run_testcases.py** => Main script. You can run it using the command 
`python3 run_testcases.py 3 lazyLoading`

- TestAPI.py => Helper for main Python script. Do not run this directly.

- manifest.json => Defines the patterns and test cases

- power-logfiles => Folder where the measurement data csv files are saved to. Do not rename!
We have provided the binary file for Powerlog tool (`intel-power-gadget.dmg`).

After-running tasks
- **combine_testdata.py** => Use this to merge all test run data into one single file.
You can run it using the command: 
`python3 combine_testdata.py`

- **show_plots.py** => Python scrip to shows plots of the measurement data. You can run it using the example command: 
`python3 show_plots.py 0 "Total Elapsed Time (sec)" " sec"`

- PLOT_COMMANDS.txt => Here you can find all commands you need to run the former script (show_plots.py)