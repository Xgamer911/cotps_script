# cotps_script

Overview
----------------------------
This script is to simply create orders when no money is currently in transaction. It will also keep track of all orders within a csv file in the same directory as the cotps.py script file.

Please consider donating or tipping
----------------------------
Cotps TRC20 wallet: TSD656HMENSsdaSU6QZhyS9xyiicAZ37kv

FTX ERC-20 wallet:  0x37F6fFF40705120b5Ed81200FAD4142aa9962cE1

FTX TRX wallet:     TUAGnw4wQXqCbsx5XWsn2mR7RVjcqDetkW

Use the github issues for any problems with the script or feature requests. If you have an issue, please provide your current versions of the required programs provided below, the error you received, and any python traceback that might have occured.

Program requirements
----------------------------
* Chrome - Tested on Version 100.0.4896.127 (Official Build) (64-bit)
* Chrome Driver - Tested on ChromeDriver Version 100.0.4896.60
    https://sites.google.com/chromium.org/driver/downloads
* Python - Version 3.6.8
* Edited config.cfg file with location of chromedriver file, username (ie phone number), and password.


Python Modules Needed
----------------------------
* selenium 
* configparser
* time
* datetime
* pytz
* csv
* os


Program logic
----------------------------
1) Starts by reading in config.cfg file in same directory as the script and declares all needed variables.
2) Checks if there is already a csv file already created with the name from the config file. If there is one, it will append to it. If there is not, it will create one.
3) Get current program start time.
4) Please donate :D
5) Starts chrome browser with the chromedriver file. The location of the chromedriver file needs to be provided in the config.cfg file.
6) Begins to login to cotps using the username and password from the config.cfg file.
7) Once it authenticates, it will goto the transaction hall page. Depending on the speed of the internet or the webpage, the variable "refreshtime", may need to be increased. This variable is how long the program will wait for the webpage or actions to load. If you have a lot of errors with this program, I recommend to increase this number. I have gotten it to work with as low as 8, but I found my sweet spot to be 10.
8) The program will then get the current wallet information.
9) If the "In Transaction" is not 0, it will wait. This time between wallet checks can be modified by changing the "timebetweenchecks" variable of the config.cfg file.
10) If the "In Transaction" is 0, the program will attempt to get an order by clicking the "immediate competition for orders" button and then the "Sell" button.
11) The program will then gather the order details and then click the "Confirm" button.
12) It will continue steps 10 and 11 until there is less than $5 left in the wallet.
13) It will then start the "timebetweenchecks" wait until the "In Transaction" reaches 0 again.

Starting the Program
----------------------------
Open command line, goto cotps.py location and type "python cotps.py"

or

double clicking on cotps.py
