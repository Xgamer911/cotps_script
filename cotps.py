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
#Discord
from discord import Webhook, RequestsWebhookAdapter
import requests
#END IMPORT

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

def startchrome(chromedriver):
    options = webdriver.ChromeOptions()

    sendlogmessage("Open browser")

    options.add_argument('--window-size=1024,768')
    options.add_argument('--log-level=3')

    # Run Chrome invisible or not
    if(int(runheadless) == 1):
        sendlogmessage("Running Chrome headless")
        options.add_argument("--headless")
        options.add_argument("--start-maximized");
    #END IF

    #Where is chromedriver present on your system.
    driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)

    return driver
#END DEF

def dologincheck(driver,refreshtime):
    #sendlogmessage('Logged in: ' + str(driver.execute_script("return localStorage['IS_LOGIN']")))
    if driver.execute_script("return localStorage['IS_LOGIN']") != 'Y':
        sendlogmessage('Not logged in')
        setcountrycode(driver,refreshtime)
        logintocotps(driver,refreshtime)
        gototransactionhall(driver,refreshtime)
    #else:
        #sendlogmessage('Still logged in')
    #END IF
#END DEF

def logintocotps(driver,refreshtime):
    sendlogmessage("Logging into COTPS")
    driver.get('https://cotps.com/#/pages/login/login')
    time.sleep(refreshtime)
    ele = driver.find_elements_by_class_name('uni-input-input')
    #sendlogmessage("Inputting phone number")
    ele[0].send_keys(username)
    time.sleep(1)
    #sendlogmessage("Inputting password")
    ele[1].send_keys(password)
    time.sleep(1)
    #sendlogmessage("Finding and clicking login")
    loginbutton=driver.find_elements_by_class_name('login')
    loginbutton[0].click()
    time.sleep(refreshtime)
#END DEF

def setcountrycode(driver,refreshtime):
    driver.get('https://cotps.com/#/pages/phonecode/phonecode?from=login')
    time.sleep(refreshtime)
    ele = driver.find_elements_by_class_name('uni-input-input')
    #sendlogmessage("Inputting country code")
    ele[0].send_keys(countrycode)
    time.sleep(1)
    #sendlogmessage("Finding and clicking confirm")   
    varcommit=driver.find_element_by_xpath('/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[1]/uni-button')
    varcommit.click()
    time.sleep(refreshtime)
#END DEF

def gototransactionhall(driver,refreshtime):
    driver.get('https://cotps.com/#/pages/transaction/transaction')
    time.sleep(refreshtime)
#END DEF

def gotoreferralrewards(driver,refreshtime):
    driver.get('https://cotps.com/#/pages/userCenter/myTeam')
    time.sleep(refreshtime)
#END DEF

def claimreferralfees(driver,refreshtime):
    try:
        # Claim LV1
        varfees=float(driver.find_element_by_xpath('/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[2]/uni-view/uni-view[1]/uni-view[2]/uni-view[2]').text)
        varconfirm=driver.find_element_by_xpath('/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[2]/uni-view/uni-button')
        varconfirm.click()
        sendlogmessage('Fees LV1: $' + str(varfees))
        time.sleep(refreshtime)

        # Claim LV2
        varfees=float(varfees) + float(driver.find_element_by_xpath('/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[2]/uni-view/uni-view[1]/uni-view[2]/uni-view[2]').text)
        varconfirm=driver.find_element_by_xpath('/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[1]/uni-view[2]')
        varconfirm.click()
        time.sleep(refreshtime/2)
        varconfirm=driver.find_element_by_xpath('/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[2]/uni-view/uni-button')
        varconfirm.click()
        sendlogmessage('Fees LV2: $' + str(varfees))
        time.sleep(refreshtime)

        # Claim LV3
        varfees=float(varfees) + float(driver.find_element_by_xpath('/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[2]/uni-view/uni-view[1]/uni-view[2]/uni-view[2]').text)
        varconfirm=driver.find_element_by_xpath('/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[1]/uni-view[3]')
        varconfirm.click()
        time.sleep(refreshtime/2)
        varconfirm=driver.find_element_by_xpath('/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[2]/uni-view/uni-button')
        sendlogmessage('Fees LV3: $' + str(varfees))
        varconfirm.click()

        sendlogmessage('Claimed fees: $' + str(varfees))

        time.sleep(refreshtime)
    except:
        sendlogmessage('Error claiming referrals, back to the hall..')
        return False
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
        sendlogmessage('Error getting wallet, refreshing page')
        gototransactionhall(driver,refreshtime)
    #END TRY
    return walletinfo
#END DEF

def getandsellorder(driver,refreshtime):
    try:
        varorder=driver.find_element_by_xpath('/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[4]/uni-button')
        varorder.click()
        time.sleep(refreshtime)
        try:
            varsell=driver.find_element_by_xpath('/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[7]/uni-view/uni-view/uni-view[6]/uni-button[2]')
            varsell.click()
            time.sleep(refreshtime)
        except:
            sendlogmessage('Sell button 2 not found, breaking off')
            return False
    except:
        sendlogmessage('Sell button 1 not found, breaking off')
        return False
    return True
#END DEF

def getorderdetails(driver,refreshtime,orderdict):
    try:
        varordernumber=driver.find_element_by_xpath('/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[8]/uni-view/uni-view/uni-view[2]/uni-text[2]/span').text
        vartransactionamount=driver.find_element_by_xpath('/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[8]/uni-view/uni-view/uni-view[3]/uni-text[2]/span').text
        varprofit=driver.find_element_by_xpath('/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[8]/uni-view/uni-view/uni-view[4]/uni-text[2]/span').text
        vartotal=driver.find_element_by_xpath('/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[8]/uni-view/uni-view/uni-view[5]/uni-text[2]/span').text
        orderdict.update({"ordernum": varordernumber})
        orderdict.update({"transactionamount": vartransactionamount})
        orderdict.update({"profit": varprofit})
        orderdict.update({"total": vartotal})
        time.sleep(refreshtime)
    except:
        sendlogmessage('Error getting wallet, refreshing page')
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
    if int(usecsvfile) == 1:
        try:
            with open(csvfile, 'a') as f:
                sendlogmessage("Writing Order to CSV")
                writer = csv.writer(f,lineterminator='\n')
                writer.writerow([orderdict.get("ordernum"), orderdict.get("timeofsale"), orderdict.get("transactionamount"), orderdict.get("profit"), orderdict.get("total")])
                return True
        except:
            return False
    #END IF
#END DEF

def sendlogmessage(message):
    try:
        webhook = Webhook.from_url(discordwebhookurl, adapter=RequestsWebhookAdapter())
        webhook.send(message)
        print(message)
    except:
        print(message)
#END DEF

# Main Function
if __name__ == '__main__':
    config=configparser.ConfigParser()
    config.sections()

    config.read('config.cfg')

    #Provide chromedriver location
    chromedriver=config['DEFAULT']['chromedriverfile']
    #Provide the email and password
    username=config['DEFAULT']['username']
    password=config['DEFAULT']['password']
    countrycode=config['DEFAULT']['countrycode']
    #How long for each page refresh
    refreshtime=int(config['DEFAULT']['refreshtime'])
    #How long to wait between each check to see if in transaction went to 0
    timebetweeneachcheck=int(config['DEFAULT']['timebetweenchecks'])
    #Setting Timezone
    est=pytz.timezone(config['DEFAULT']['timezone'])
    #Use CSV file? True/False
    usecsvfile=config['DEFAULT']['usecsvfile']
    #setting CSV file location
    csvfile=config['DEFAULT']['csvfile']
    #setting wallet percentage to start new transaction
    walletpercentagetostart=config['DEFAULT']['walletpercentagetostart']
    # OR set an amount to start
    walletamounttostart=config['DEFAULT']['walletamounttostart']
    # Hide Chrome
    runheadless=config['DEFAULT']['runheadless']
    # Discord webhook URL
    discordwebhookurl=config['DEFAULT']['discordwebhookurl']

    #initializating variable
    walletinfo=[0,0]

    #Begin order dict
    orderdict=clearorderdict()

    #Checks if csv exists
    if int(usecsvfile) == 1:
        file_exists = os.path.exists(csvfile)
        if bool(file_exists) == False:
            sendlogmessage('CSV file ' + str(csvfile) + ' does not exist, trying to create it...')
            writecsvheader(csvfile)
        #END IF
    #END IF

    #Gets current time and sets timezone
    today=date.today()
    now = datetime.now(est)
    currentdate=today.strftime("%m-%d")
    currenttime=now.strftime("%H:%M")

    sendlogmessage('Program start time: ' + currentdate + ' ' + currenttime)

    #start browser
    driver=startchrome(chromedriver)

    #set countrycode
    setcountrycode(driver,refreshtime)

    #Login to cotps
    logintocotps(driver,refreshtime)

    #Begin in transaction watch cycle
    while True:

        dologincheck(driver,refreshtime)

        today=date.today()
        now = datetime.now(est)
        currentdate=today.strftime("%m-%d")
        currenttime=now.strftime("%H:%M")

        #check and claim referral rewards
        sendlogmessage('Opening referrals page and claiming fees')
        gotoreferralrewards(driver,refreshtime)
        claimreferralfees(driver,refreshtime)

        #Goto Transaction Hall
        sendlogmessage('Back to transaction hall...')
        gototransactionhall(driver,refreshtime)

        #get wallet info and see if anything is in tranaction
        walletinfo=getwalletinfo(driver,walletinfo,refreshtime)

        #Get in transaction amount
        currentwallet=float(walletinfo[0])
        intranswallet=float(walletinfo[1])
        sendlogmessage('In transactions: $' + str(intranswallet))
        sendlogmessage('Wallet balance: $' + str(currentwallet) + ' (needed for trading: $' + str(walletamounttostart) + ') OR')
        totalassets=intranswallet+currentwallet
        walletbalancepercentage=round(100/(totalassets/currentwallet), 2)
        sendlogmessage('Wallet balance percentage: ' + str(walletbalancepercentage) + '% (needed for trading: ' + str(walletpercentagetostart) + '%)')

        #Did all my money come back yet
        orderdicttxthisrun=0
        orderdictprofitthisrun=0

        #start transactions when wallet percentage reaches at least the % set in config OR the amount set to start
        if (float(walletbalancepercentage) >= float(walletpercentagetostart) or (float(currentwallet) >= float(walletamounttostart))):

            sendlogmessage('Starting trades')

            while True:

                #Buy an Order
                if getandsellorder(driver,refreshtime) == True:
                    #Get order details
                    orderdict=getorderdetails(driver,refreshtime,orderdict)

                    #Click Confirm button
                    orderconfirm()
                    today=date.today()
                    now = datetime.now(est)
                    currentdate=today.strftime("%m-%d")
                    currenttime=now.strftime("%H:%M")
                    timestamp=currentdate + ' ' + currenttime
                    sendlogmessage('Order $' + str(orderdict.get("transactionamount")) + ', profit $' + str(orderdict.get("profit")) + ' at ' + str(timestamp))
                    orderdict.update({"timeofsale": str(timestamp)})
                    orderdicttxthisrun = float(orderdicttxthisrun) + float(orderdict.get("transactionamount"))
                    orderdictprofitthisrun = round(float(orderdictprofitthisrun) + float(orderdict.get("profit")), 2)

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
                else:
                    #break out of loop when clicking sell buttons don't work
                    break
                #END IF
            #END WHILE
            sendlogmessage('Total tx amount: $' + str(orderdicttxthisrun) + ', total profit: $' + str(orderdictprofitthisrun))
        #END IF
        dologincheck(driver,refreshtime)
        sendlogmessage('Waiting ' + str(timebetweeneachcheck) + ' seconds to begin next wallet check')
        time.sleep(timebetweeneachcheck)
    #END WHILE
#END DEF
