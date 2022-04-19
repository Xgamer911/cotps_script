# Import modules
#Controlling chrome modules
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#Configuration
import configparser
#For Sleep functions
import time
#To get current date and time
from datetime import date
from datetime import datetime
#Get eastern timezon
import pytz
#The ability to write CSV
import csv
#The ability to check if file exists
import os.path
#END IMPORT

def pleasedonate():
    print('COTPS Script')
    print('------------')
    print('Written by: Ryan Briggs')
    print('')
    print('Please consider donating or tipping')
    print('Cotps TRC20 wallet: TSD656HMENSsdaSU6QZhyS9xyiicAZ37kv')
    print('FTX ERC-20 wallet:  0x37F6fFF40705120b5Ed81200FAD4142aa9962cE1')
    print('FTX TRX wallet:     TUAGnw4wQXqCbsx5XWsn2mR7RVjcqDetkW')
    print('')

def startchrome(chromedriver):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument('--log-level=3')

    print("Open Browser")
    #Where is chromedriver present on your system.
    driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)
    driver.set_window_size(1920,1080)
    return driver
#END DEF
   
def logintocotps(driver,refreshtime):
    driver.get('https://cotps.com/#/pages/login/login')
    time.sleep(refreshtime)

    #Checks if phone extension is anything other than one. IE different country
    if phoneext != '1':
        #opens phone extension area 
        varphoneext=driver.find_element_by_xpath('/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[5]/uni-text')
        varphoneext.click()
        time.sleep(refreshtime/2)
        #Clicks input field and types extension
        varphoneext=driver.find_element_by_xpath('/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[1]/uni-view/uni-input/div/input')
        varphoneext.send_keys(phoneext)
        time.sleep(refreshtime/2)
        #Clicks confrim button
        confirmbutton=driver.find_element_by_xpath('/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[1]/uni-button')
        confirmbutton.click()
        time.sleep(refreshtime/2)

    #find phone and password fields
    ele = driver.find_elements_by_class_name('uni-input-input')
    print("Inputting phone number")
    ele[0].send_keys(username)
    time.sleep(refreshtime/2)
    print("Inputting password")
    ele[1].send_keys(password)
    time.sleep(refreshtime/2)
    print("Finding and clicking login")
    loginbutton=driver.find_elements_by_class_name('login')
    loginbutton[0].click()
    time.sleep(refreshtime)
#END DEF

def gototransactionhall(driver,refreshtime):
    driver.get('https://cotps.com/#/pages/transaction/transaction')
    time.sleep(refreshtime)
#END DEF

def getwalletinfo(driver,walletinfo,refreshtime):
    try:
        #get current wallet
        testvar=driver.find_element_by_xpath('/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[3]/uni-view[2]/uni-view[2]')
        currentwallet=float(testvar.text)
        walletinfo[0]=currentwallet

        #get current amount in transactions
        testvar=driver.find_element_by_xpath('/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[3]/uni-view[1]/uni-view[2]')
        currentintransaction=float(testvar.text)
        walletinfo[1]=currentintransaction
    except:
        print('Error getting wallet, refreshing page')
        gototransactionhall(driver,refreshtime)
    #END TRY
    return walletinfo
#END DEF

def getandsellorder(driver,refreshtime):
    try:
        varorder=driver.find_element_by_xpath('/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[4]/uni-button')
        varorder.click()
        time.sleep(refreshtime)
    except:
        varorder=driver.find_element_by_xpath('/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[4]/uni-button')
        varorder.click()
        time.sleep(refreshtime)

    try:
        varsell=driver.find_element_by_xpath('/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[7]/uni-view/uni-view/uni-view[6]/uni-button[2]')
        varsell.click()
        time.sleep(refreshtime)
    except:
        varsell=driver.find_element_by_xpath('/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[7]/uni-view/uni-view/uni-view[6]/uni-button[2]')
        varsell.click()
        time.sleep(refreshtime)
#END DEF

def getorderdetails(driver,refreshtime,orderdict):
    try:
        varordernumber=driver.find_element_by_xpath('/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[8]/uni-view/uni-view/uni-view[2]/uni-text[2]/span').text
        vartranactionamount=driver.find_element_by_xpath('/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[8]/uni-view/uni-view/uni-view[3]/uni-text[2]/span').text
        varprofit=driver.find_element_by_xpath('/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[8]/uni-view/uni-view/uni-view[4]/uni-text[2]/span').text
        vartotal=driver.find_element_by_xpath('/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[8]/uni-view/uni-view/uni-view[5]/uni-text[2]/span').text
        orderdict.update({"ordernum": varordernumber})
        orderdict.update({"transactionamount": vartranactionamount})
        orderdict.update({"profit": varprofit})
        orderdict.update({"total": vartotal})
        time.sleep(refreshtime)
    except:
        print('Error getting wallet, refreshing page')
        gototransactionhall(driver,refreshtime)
    #END TRY  
    return orderdict
#END DEF

def orderconfirm():
    time.sleep(refreshtime)
    varconfirm=driver.find_element_by_xpath('/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[8]/uni-view/uni-view/uni-button')
    varconfirm.click()
#END DEF

def clearorderdict():
    orderdict={
        "ordernum": "",
        "timeofsale": "",
        "transactionamount": "",
        "profit": "",
        "total": ""
    }
    return orderdict
#END DEF

def writecsvheader(csvfile):
    with open(csvfile, 'w',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Order Number", "Time of Sale", "Transaction Amount", "Profit", "Total"])
#END DEF

def writedicttocsv(csvfile,orderdict):
    print("Writing Order to CSV")
    with open(csvfile, 'a') as f:
        writer = csv.writer(f,lineterminator='\n')
        writer.writerow([orderdict.get("ordernum"), orderdict.get("timeofsale"), orderdict.get("transactionamount"), orderdict.get("profit"), orderdict.get("total")])
#END DEF

# Main Function
if __name__ == '__main__':
    config=configparser.ConfigParser()
    config.sections()
    
    config.read('config.cfg')

    #Provide chromedriver location
    chromedriver=config['DEFAULT']['chromedriverfile']
    #Provide the extension for phone number for login
    phoneext=config['DEFAULT']['phoneext']
    #Provide the email and password
    username=config['DEFAULT']['username']
    password=config['DEFAULT']['password']
    #How long for each page refresh
    refreshtime=int(config['DEFAULT']['refreshtime'])
    #How long to wait between each check to see if in transaction went to 0
    timebetweeneachcheck=int(config['DEFAULT']['timebetweenchecks'])
    #Setting Timezone
    est=pytz.timezone(config['DEFAULT']['timezone'])
    #setting CSV file location
    csvfile=config['DEFAULT']['csvfile']

    #initializating variable
    walletinfo=[0,0]

    #Begin order dict
    orderdict=clearorderdict()

    #Checks if csv exists
    file_exists = os.path.exists(csvfile)
    if file_exists == False:
        writecsvheader(csvfile)

    #Gets current time and sets timezone
    today=date.today()
    now = datetime.now(est)
    currentdate=today.strftime("%m-%d")
    currenttime=now.strftime("%H:%M")

    #Please Donate or Tip
    pleasedonate()

    #start browser
    driver=startchrome(chromedriver)
    print('Program start time: ' + currentdate + ' ' + currenttime + ' EST')
    #Login to cotps
    logintocotps(driver,refreshtime)
    #Goto Transaction Hall
    gototransactionhall(driver,refreshtime)
    print("Open transaction hall")

    #Begin in transaction watch cycle
    while True:
        today=date.today()
        now = datetime.now(est)
        currentdate=today.strftime("%m-%d")
        currenttime=now.strftime("%H:%M")       
        #Refresh page
        gototransactionhall(driver,refreshtime)
        print('Refreshing Page: ' + currentdate + ' ' + currenttime + ' EST')

        #get wallet info and see if anything is in tranaction
        walletinfo=getwalletinfo(driver,walletinfo,refreshtime)
        
        #Get in transaction amount
        intranswallet=float(walletinfo[1])
        print('In Transactions: ' + str(intranswallet))

        #Did all my money come back yet     
        if intranswallet == 0:
            while True:
                today=date.today()
                now = datetime.now(est)
                currentdate=today.strftime("%m-%d")
                currenttime=now.strftime("%H:%M")
                walletinfo=getwalletinfo(driver,walletinfo,refreshtime)
                currentwallet=float(walletinfo[0])
                intranswallet=float(walletinfo[1])
                print('Buying order at: ' + currentdate + ' ' + currenttime + ' EST')
                print('Current Wallet: ' + str(currentwallet))
                print('In Transactions: ' + str(intranswallet))

                #Buy an Order
                getandsellorder(driver,refreshtime)

                #Get order details
                orderdict=getorderdetails(driver,refreshtime,orderdict)

                #Click Confirm button
                orderconfirm()
                today=date.today()
                now = datetime.now(est)
                currentdate=today.strftime("%m-%d")
                currenttime=now.strftime("%H:%M")
                timestamp=currentdate + ' ' + currenttime                
                print('Order Confirmed at: ' + str(timestamp) + ' EST')
                orderdict.update({"timeofsale": str(timestamp)})

                #Write current Order to CSV
                writedicttocsv(csvfile,orderdict)

                #Clear dictionary for next order
                orderdict=clearorderdict()

                #Get current wallet
                walletinfo=getwalletinfo(driver,walletinfo,refreshtime)

                #What is my current wallet
                currentwallet=float(walletinfo[0])

                #If less than $5, stop purchasing
                if currentwallet <= 5:
                    #breaks out of loop when money is to low
                    break
                #END IF
            #END WHILE
        #END IF
        print('Waiting ' + str(timebetweeneachcheck) + ' seconds to begin next wallet check')
        time.sleep(timebetweeneachcheck)
    #END WHILE
#END DEF
