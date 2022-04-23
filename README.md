# cotps_script

Script by Ryan Briggs, with LOTS of mods by Francis. Be nice and reward your dev, send your USDT to TRON wallet:
    Ryan: TSD656HMENSsdaSU6QZhyS9xyiicAZ37kv
    Francis: TT63rNP6fwH6f7fJD1EYCnFMJz7U5nXYw9

Francis COTP ref: https://www.cotps.com#/pages/login/register?invite=822569

Source is on https://github.com/Francis-I-Am/cotps_script/

Overview
----------------------------
This script is to simply create orders when no money is currently in transaction. It will also keep track of all orders within a csv file in the same directory as the cotps.py script file.

Program requirements
----------------------------
* Chrome - Tested on Version 100.0.4896.127 (Official Build) (64-bit)
* Chrome Driver - Tested on ChromeDriver Version 100.0.4896.60
    https://sites.google.com/chromium.org/driver/downloads
* Python - Version 3.6.8
* Edited config.cfg file with location of chromedriver file, username (ie phone number), and password.


Python Modules Needed
----------------------------
* selenium (needs to be installed)
* configparser
* time
* datetime
* pytz (needs to be installed)
* csv
* os
* requests
* discord


Program logic
----------------------------
1) Starts by reading in config.cfg file in same directory as the script and declares all needed variables.
2) Checks if there is already a csv file already created with the name from the config file. If there is one, it will append to it. If there is not, it will create one.
3) Get current program start time.
4) Starts chrome browser with the chromedriver file. The location of the chromedriver file needs to be provided in the config.cfg file.
5) Begins to login to cotps using the username and password from the config.cfg file.
6) Once it authenticates, it will goto the referral rewards page and will click the button to claim. Then it will go to the transaction hall (referral claiming will be done every wait cycle). Depending on the speed of the internet or the webpage, the variable "refreshtime", may need to be increased. This variable is how long the program will wait for the webpage or actions to load. If you have a lot of errors with this program, I recommend to increase this number. I have gotten it to work with as low as 8, but I found my sweet spot to be 10.
7) The program will then get the current wallet information.
8) If the "In Transaction" below the set percentage, it will wait. This time between wallet checks can be modified by changing the "timebetweenchecks" variable of the config.cfg file.
9) If the "In Transaction" is 0, the program will attempt to get an order by clicking the "immediate competition for orders" button and then the "Sell" button.
10) The program will then gather the order details and then click the "Confirm" button.
11) It will continue steps 10 and 11 until there is less than $5 left in the wallet.
12) It will then start the "timebetweenchecks" wait until the "In Transaction" reaches the set up amount or percentage again.

Starting the Program
----------------------------
First, open a command prompt and type "pip install selenium"

This will install the selenium webdriver for python.

Also do this for other Python modules mentioned before.
