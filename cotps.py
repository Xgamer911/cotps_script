# cotps_script
# v1.3
# Script by Ryan Briggs, with LOTS of mods and code cleanup by Francis.
#Import modules
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
#Get timezone
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

def dologincheck(driver,refreshtime,errorsthatoccured):
    #Had issues with this section hard crashing, so adding try except
    try:
        if driver.execute_script("return localStorage['IS_LOGIN']") != 'Y':
            sendlogmessage('Not logged in')
            setcountrycode(driver,refreshtime)
            logintocotps(driver,refreshtime)
            gototransactionhall(driver,refreshtime)
        #END IF
    except:
        sendlogmessage("Error 3 - Login check failed")
        restartprogram(driver, errorsthatoccured)
    #END TRY
#END DEF

def logintocotps(driver,refreshtime):
    #send group discord message if enabled
    if groupdiscord==1:
        sendgroupmessage("Logging into COTPS")
    else:
        sendlogmessage("Logging into COTPS")

    driver.get('https://cotps.com/#/pages/login/login')
    time.sleep(refreshtime)
    #Check if Login button is loaded yet
    while True:
        try:
            if driver.find_element_by_xpath('/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-button').is_displayed() == True:
                break
        except:
            sendlogmessage("Error - Login Button not found")
            time.sleep(refreshtime/2)

    ele = driver.find_elements_by_class_name('uni-input-input')
    sendlogmessage("Inputting phone number")
    ele[0].send_keys(username)
    time.sleep(1)
    sendlogmessage("Inputting password")
    ele[1].send_keys(password)
    time.sleep(1)
    #sendlogmessage("Finding and clicking login")
    loginbutton=driver.find_elements_by_class_name('login')
    loginbutton[0].click()
    time.sleep(refreshtime)
    sendlogmessage("Logging in")
#END DEF

def setcountrycode(driver,refreshtime):
    driver.get('https://cotps.com/#/pages/phonecode/phonecode?from=login')
    time.sleep(refreshtime)

    #Check if confirm button is loaded yet
    while True:
        try:
            if driver.find_element_by_xpath('/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[1]/uni-button').is_displayed() == True:
                break
        except:
            sendlogmessage("Error - Confirm Button not found")
            time.sleep(refreshtime/2)

    sendlogmessage("Setting Country Code")
    ele = driver.find_elements_by_class_name('uni-input-input')
    #sendlogmessage("Inputting country code")
    ele[0].send_keys(countrycode)
    time.sleep(1)
    #sendlogmessage("Finding and clicking confirm")   
    varcommit=driver.find_element_by_xpath('/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[1]/uni-button')
    varcommit.click()
    time.sleep(refreshtime)
    sendlogmessage("Set Country Code")
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
        varfees1=float(driver.find_element_by_xpath('/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[2]/uni-view/uni-view[1]/uni-view[2]/uni-view[2]').text)
        varconfirm=driver.find_element_by_xpath('/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[2]/uni-view/uni-button')
        varconfirm.click()
        sendlogmessage('Fees LV1: $' + str(varfees1))
        time.sleep(refreshtime)

        # Claim LV2
        varfees2=float(driver.find_element_by_xpath('/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[2]/uni-view/uni-view[1]/uni-view[2]/uni-view[2]').text)
        varconfirm=driver.find_element_by_xpath('/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[1]/uni-view[2]')
        varconfirm.click()
        time.sleep(refreshtime/2)
        varconfirm=driver.find_element_by_xpath('/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[2]/uni-view/uni-button')
        varconfirm.click()
        sendlogmessage('Fees LV2: $' + str(varfees2))
        time.sleep(refreshtime)

        # Claim LV3
        varfees3=float(driver.find_element_by_xpath('/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[2]/uni-view/uni-view[1]/uni-view[2]/uni-view[2]').text)
        varconfirm=driver.find_element_by_xpath('/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[1]/uni-view[3]')
        varconfirm.click()
        time.sleep(refreshtime/2)
        varconfirm=driver.find_element_by_xpath('/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[2]/uni-view/uni-button')
        sendlogmessage('Fees LV3: $' + str(varfees3))
        varconfirm.click()
        varfeetotal=varfees1+varfees2+varfees3

        sendlogmessage('Claimed fees: $' + str(varfeetotal))

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

        sendlogmessage('Getting Wallet: '+ str(currentwallet) + '| In transactions: '+ str(currentintransaction))
    except:
        sendlogmessage('Error getting wallet, refreshing page')
        gototransactionhall(driver,refreshtime)
    #END TRY
    return walletinfo
#END DEF

def getandsellorder(driver,refreshtime):
    try:
        #Check if Sell button 1 is loaded yet
        while True:
            try:
                if driver.find_element_by_xpath('/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[4]/uni-button').is_displayed() == True:
                    break
            except:
                sendlogmessage("Error - Confirm Button not found")
                time.sleep(refreshtime/2)

        varorder=driver.find_element_by_xpath('/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[4]/uni-button')
        varorder.click()
        time.sleep(refreshtime)
        sendlogmessage('Sell Order 1')
        try:
            #Check if Sell button 2 is loaded yet
            while True:
                try:
                    if driver.find_element_by_xpath('html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[7]/uni-view/uni-view/uni-view[6]/uni-button[2]').is_displayed() == True:
                        break
                except:
                    sendlogmessage("Error - Confirm Button not found")
                    time.sleep(refreshtime/2)

            varsell=driver.find_element_by_xpath('/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[7]/uni-view/uni-view/uni-view[6]/uni-button[2]')
            varsell.click()
            time.sleep(refreshtime)
            sendlogmessage('Sell Order 2')
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
        sendlogmessage('Got Order Details')
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
    sendlogmessage('Confirmed Order')
#END DEF

def clearorderdict():
    orderdict={
        "ordernum": "",
        "timeofsale": "",
        "transactionamount": "",
        "profit": "",
        "total": ""
    }
    sendlogmessage("Cleared order dictionary")
    return orderdict
#END DEF

def writecsvheader(csvfile):
    with open(csvfile, 'w',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Order Number", "Time of Sale", "Transaction Amount", "Profit", "Total"])
#END DEF

def writedicttocsv(csvfile,orderdict):
    sendlogmessage("Starting CSV tracking")
    if int(usecsvfile) == 1:
        try:
            with open(csvfile, 'a') as f:
                sendlogmessage("Writing Order to CSV")
                writer = csv.writer(f,lineterminator='\n')
                writer.writerow([orderdict.get("ordernum"), orderdict.get("timeofsale"), orderdict.get("transactionamount"), orderdict.get("profit"), orderdict.get("total")])
                sendlogmessage("Wrote Order to CSV")
                return True
        except:
            return False
    #END IF
#END DEF

def sendlogmessage(message):
    try:
        #creating timestamp for discord message
        today=date.today()
        now = datetime.now(est)
        currentdate=today.strftime("%m-%d")
        currenttime=now.strftime("%H:%M")
        #adding timestamp to discord message
        sendingmessage = currentdate + ' ' + currenttime + ' - ' + message
        print(sendingmessage)
    except:
        print(message)
#END DEF

def sendgroupmessage(message):
    try:
        #creating timestamp for discord message
        today=date.today()
        now = datetime.now(est)
        currentdate=today.strftime("%m-%d")
        currenttime=now.strftime("%H:%M")
        #adding timestamp to discord message
        #send group discord message if enabled
        if groupdiscord == 1:
            sendingmessage = groupbotname + ' - ' + currentdate + ' ' + currenttime + ' - ' + message
        else:
            sendingmessage = currentdate + ' ' + currenttime + ' - ' + message
        webhook = Webhook.from_url(discordwebhookurl, adapter=RequestsWebhookAdapter())
        webhook.send(sendingmessage)
        print(sendingmessage)
    except:
        print('ERROR - ' + message)
#END DEF

def restartprogram(driver,errorsthatoccured):
    sendlogmessage('ERROR - ' + str(errorsthatoccured) + ' have occured, restarting program')
    driver.quit()
    os.startfile(__file__)
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
    # Keep this percentage of your funds in the wallet (calculates of total funds)
    reservepercentage=config['DEFAULT']['reservepercentage']
    claimreferrals=config['DEFAULT']['claimreferrals']
    # Will restart program if so many errors occur
    errorsuntilrestart=int(config['DEFAULT']['errorsuntilrestart'])
    errorsthatoccured=0
    # if you have more than one bot going to the same discord channel (IE checkin)
    groupdiscord=int(config['DEFAULT']['groupdiscord'])
    groupbotname=str(config['DEFAULT']['groupbotname'])
    # this will send a periodic checkin. This number will be multipled by the timebetweeneachcheck time
    groupcheckin=int(config['DEFAULT']['groupcheckin'])
    # This variable will claim referrals at the beginning of each cycle or at the beginning of a trade cycle
    # 1 for each cycle and 0 for before each trade cycle
    claimtime=int(config['DEFAULT']['claimtime'])

    #Counter variable that will increment each cycle, once it reaches the groupcheckin it will send a group message
    groupcheckincounter=0
    #This variable will skip the timebetweeneachcheck if a trade button errored out. This is to go right back into trading and not wait another 5 minutes.
    sellbuttonmissingerror=0

    sendlogmessage('Claiming referrals: ' + claimreferrals)
    sendlogmessage('Keeping ' + reservepercentage + '% of funds for easy claiming')

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
    #send group discord message if enabled
    if groupdiscord==1:
        sendgroupmessage('Program start time: ' + currentdate + ' ' + currenttime)
    else:
        sendlogmessage('Program start time: ' + currentdate + ' ' + currenttime)

    #start browser
    driver=startchrome(chromedriver)

    #set countrycode
    setcountrycode(driver,refreshtime)

    #Login to cotps
    logintocotps(driver,refreshtime)

    #Begin in transaction watch cycle
    while True:

        #Claim referrals on each cycle
        if int(claimtime) == 1:
            if int(claimreferrals) == 1:
            #check and claim referral rewards
                sendlogmessage('Opening referrals page and claiming fees')
                gotoreferralrewards(driver,refreshtime)
                claimreferralfees(driver,refreshtime)
            #END IF   
        #END IF         

        # Checks if errors have occured and program needs to be restarted
        if errorsthatoccured==errorsuntilrestart:
            sendlogmessage("Error 2 - Error Amount")
            restartprogram(driver, errorsthatoccured)
            break

        dologincheck(driver,refreshtime,errorsthatoccured)

        today=date.today()
        now = datetime.now(est)
        currentdate=today.strftime("%m-%d")
        currenttime=now.strftime("%H:%M")

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

        #start transactions when wallet percentage reaches at least the % set in config OR the amount set to start or if previous cycle had a sellbutton error
        if (float(walletbalancepercentage) >= float(walletpercentagetostart) or (float(currentwallet) >= float(walletamounttostart)) or (sellbuttonmissingerror==1)):
            #setting error variable
            sellbuttonmissingerror=0

            #send group discord message if enabled
            if groupdiscord==1:
                sendgroupmessage('Starting trades')
            else:
                sendlogmessage('Starting trades')

            #Claim referrals before each trade cycle
            if int(claimtime) == 0:
                if int(claimreferrals) == 1:
                #check and claim referral rewards
                    sendlogmessage('Opening referrals page and claiming fees')
                    gotoreferralrewards(driver,refreshtime)
                    claimreferralfees(driver,refreshtime)
                #END IF   
            #END IF 

            #Goto Transaction Hall
            sendlogmessage('Back to transaction hall...')
            gototransactionhall(driver,refreshtime)

            while True:

                #Buy an Order
                if getandsellorder(driver,refreshtime) == True:
                    #Get order details
                    orderdict=getorderdetails(driver,refreshtime,orderdict)

                    if str(orderdict.get("transactionamount")) == '':
                        sendlogmessage('Error 1 - In transaction Blank')
                        break
                    #END IF

                    #Click Confirm button
                    orderconfirm()
                    today=date.today()
                    now = datetime.now(est)
                    currentdate=today.strftime("%m-%d")
                    currenttime=now.strftime("%H:%M")
                    timestamp=currentdate + ' ' + currenttime
                    sendlogmessage('Order $' + str(orderdict.get("transactionamount")) + ', profit $' + str(orderdict.get("profit")) + ' at ' + str(timestamp))
                    orderdict.update({"timeofsale": str(timestamp)})
                    if orderdict.get("transactionamount") != '':
                        orderdicttxthisrun = float(orderdicttxthisrun) + float(orderdict.get("transactionamount"))
                    #END IF
                    orderdictprofitthisrun = round(float(orderdictprofitthisrun) + float(orderdict.get("profit")), 2)

                    #Write current Order to CSV
                    writedicttocsv(csvfile,orderdict)

                    #Clear dictionary for next order
                    orderdict=clearorderdict()

                    #Get current wallet
                    walletinfo=getwalletinfo(driver,walletinfo,refreshtime)

                    #What is my current wallet
                    currentwallet=float(walletinfo[0])

                    #If wallet % is less than given %1 to keep in reserve, stop purchasing
                    assetpercentage = round(totalassets*(float(reservepercentage)/100), 2)
                    if currentwallet <= assetpercentage:
                        sendlogmessage('$' + str(currentwallet) + ' in wallet, which is smaller than $' + str(assetpercentage) + ' based on what to keep. Stopping cycle')
                        #breaks out of loop when money is to low
                        break
                    #END IF

                    #If less than $5, stop purchasing
                    if currentwallet <= 5:
                        sendlogmessage('Less than 5, Breaking out')
                        break;
                    #END IF
                else:
                    sendlogmessage("Error code increased")
                    #Will increment variable and if it reaches the errorsuntilrestart variable, the entire script will restart
                    errorsthatoccured=errorsthatoccured+1
                    #
                    sellbuttonmissingerror=1
                    #break out of loop when clicking sell buttons don't work
                    break
                #END IF
            #END WHILE
            sendlogmessage('Total tx amount: $' + str(orderdicttxthisrun) + ', total profit: $' + str(orderdictprofitthisrun))
        #END IF
        dologincheck(driver,refreshtime,errorsthatoccured)
        
        #checking if it is time to checkin
        if groupcheckincounter==groupcheckin:
            #send group discord message if enabled
            if groupdiscord==1:
                sendgroupmessage('Checking in')
            else:
                sendlogmessage('Checking in')
            groupcheckincounter=0

        # If sellbutton didnt error this should be 0, if error did occur this should be a 1 and skip the timebetweeneachcheck
        if sellbuttonmissingerror != 1:
            sendlogmessage('Waiting ' + str(timebetweeneachcheck) + ' seconds to begin next wallet check')
            time.sleep(timebetweeneachcheck)
            groupcheckincounter=groupcheckincounter+1
        else:
            sendlogmessage('Skipping cycle time due to sell button error')
            time.sleep(refreshtime)
    #END WHILE
#END DEF
