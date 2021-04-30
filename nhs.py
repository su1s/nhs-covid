#! /usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import time 
from datetime import datetime
import smtplib
import sys
import argparse

# Application Settings 
url = "https://www.nhs.uk/book-a-coronavirus-vaccination/do-you-have-an-nhs-number"
driver_path = './chromedriver.exe' # Path to Chrome driver 
headless = True # Headless browser window 
sleepdelay = 60 # Seconds between scrapping attempts 
delay = 5 # Max time to wait for web pages to load 
logfile ="covid.log" # Log file to write results to
booking = False # Booking flag, if true, browser will be visable, logs will not be written and application will exit at the results page

# Peronsal settings, amend to suit 
firstname = "Joe"
surname= "Bloggs"
dob_day = "01"
dob_month = "01"
dob_year = "1980"
postcode_registered = "SW1A 1AA"
postcode_search = "SW1A 1AA"
access_needs_accessible_toilets = False
access_needs_braille_translation = False
access_needs_disabled_car_parking = False
access_needs_induction_loop = False
access_needs_sign_language_service = False
access_needs_step_free_access = False
access_needs_text_relay = False
access_needs_wheelchair_access = False
access_needs_none_of_the_above = True

# Alert settings 
send_email_alerts = False
alert_distance = 20 # Alert if available vaccinations are within this range (miles)

# SMTP settings, required for email alerts 
smtp_username ="user@outlook.com"
smtp_password = "password"
smtp_send_to = "your@email.co.uk"
smtp_send_from = "user@outlook.com"
smtp_server = "smtp-mail.outlook.com"
smtp_port = 587 
smtp_use_tls = True 

def getdriver():
    options = Options()
    options.headless = headless
    options.add_argument("--window-size=800,600")
    options.add_argument("--log-level=3")
    options.add_argument("--silent")
    browser = webdriver.Chrome(executable_path=driver_path, options=options)
    return browser

def scrapsite(browser):
    try:
        browser.get(url)
        # Page 1 - Decline cookies and select no nhs number 
        try:
            myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'submit-button')))
        except TimeoutException:
            printLog("ERROR: Page 1 timed out")
            browser.quit()
            return None
        browser.find_element_by_id('nhsuk-cookie-banner__link_accept').click()
        browser.find_element_by_id('selectedoption_No_input').click()
        browser.find_element_by_id('submit-button').click()
        # Page 2 - Enter Name 
        try:
            myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'submit-button')))
        except TimeoutException:
            printLog("ERROR: Page 2 timed out")
            browser.quit()
            return None
        browser.find_element_by_id('Firstname').send_keys(firstname)
        browser.find_element_by_id('Surname').send_keys(surname)
        browser.find_element_by_id('submit-button').click()
        # Page 3 - Enter Dob 
        try:
            myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'submit-button')))
        except TimeoutException:
            printLog("ERROR: Page 3 timed out")
            browser.quit()
            return None
        browser.find_element_by_id('Date_Day').send_keys(dob_day)
        browser.find_element_by_id('Date_Month').send_keys(dob_month)
        browser.find_element_by_id('Date_Year').send_keys(dob_year) 
        browser.find_element_by_id('submit-button').click()
        # Page 4 - Enter postcode (Registered address)
        try:
            myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'submit-button')))
        except TimeoutException:
            printLog("ERROR: Page 4 timed out")
            browser.quit()
            return None
        browser.find_element_by_id('Postcode').send_keys(postcode_registered)
        browser.find_element_by_id('submit-button').click()
        # Page 5  - You need to book both of your appointments again (May need error handling) 
        try:
            myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'submit-button')))
        except TimeoutException:
            printLog("ERROR: Page 5 timed out")
            browser.quit()
            return None
        #browser.find_element_by_id('page_h1_title')
        browser.find_element_by_id('submit-button').click()
        # Page 6 - Flu Jab 
        try:
            myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'submit-button')))
        except TimeoutException:
            printLog("ERROR: Page 6 timed out")
            browser.quit()
            return None
        browser.find_element_by_id('option_No_input').click() 
        browser.find_element_by_id('submit-button').click()
        # Page 7 - Flu Jab 2
        try:
            myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'submit-button')))
        except TimeoutException:
            printLog("ERROR: Page 7 timed out")
            browser.quit()
            return None
        browser.find_element_by_id('option_No_input').click() 
        browser.find_element_by_id('submit-button').click()
        # Page 8 - Enter postcode (Search for Vaccine centers)
        try:
            myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'next-button')))
        except TimeoutException:
            printLog("ERROR: Page 8 timed out")
            browser.quit()
            return None
        browser.find_element_by_id('StepControls_0__Model_Value').send_keys(postcode_search)
        browser.find_element_by_class_name('next-button').click()
        # Page 9 - Access needs
        try:
            myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'next-button')))
        except TimeoutException:
            printLog("ERROR: Page 9 timed out")
            browser.quit()
            return None
        if access_needs_accessible_toilets:
            browser.find_element_by_id('Value_AccessibleToilets').click()
        if access_needs_braille_translation:
            browser.find_element_by_id('Value_BrailleTranslation').click()
        if access_needs_disabled_car_parking:
            browser.find_element_by_id('Value_DisabledCarParking').click()
        if access_needs_induction_loop:
            browser.find_element_by_id('Value_InductionLoop').click()
        if access_needs_sign_language_service:
            browser.find_element_by_id('Value_SignLanguageService').click()
        if access_needs_step_free_access:
            browser.find_element_by_id('Value_StepFreeAccess').click()
        if access_needs_text_relay:
            browser.find_element_by_id('Value_TextRelay').click()
        if access_needs_wheelchair_access:
            browser.find_element_by_id('Value_WheelchairAccess').click()
        if access_needs_none_of_the_above:
            browser.find_element_by_id('Value_none').click()
        browser.find_element_by_class_name('next-button').click()
        # Parse Results
        soup=BeautifulSoup(browser.page_source, 'html.parser')
        if not booking:
            browser.quit() 
        return soup 
    except:
        printLog("ERROR: General Scrapping error occured")
        browser.quit()
        return None

def parse_results(soup):
    sites = soup.findAll(class_ = "SiteSelector")
    distances  = soup.findAll(class_ = "distance")
    a = []
    b = [] 
    alert = False
    for site in sites:
        soup.findAll(class_ = "SiteSelector") 
        a.append(site.contents[0].strip())
    for distance in distances:
        b.append(distance.contents[0].strip())
        # Check if we want to send an email 
        if (float(distance.contents[0].replace(" Miles away","").strip())) < alert_distance:
            alert = True
    results = zip(a,b)
    result_text = "\nAppointments found:\n"
    for result in results:
        result_text += (result[0] + ": " + result[1])+"\n"
    printLog(result_text)
    if alert and send_email_alerts:
        printLog("Sending alert E-Mail\n")
        sendemail(result_text)

def writeheader():
    printLog("\n*****************************************************")
    printLog("Scraping for NHS Covid Appointments: "+ datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    printLog("*****************************************************")

def printLog(*args, **kwargs):
    print(*args, **kwargs)
    if not booking:
        with open(logfile,'a') as file:
            print(*args, **kwargs, file=file)

def sendemail(body):
    body = 'Subject: ALERT: Potential NHS Covid Vaccine Appointment Available.\n\n' + body + '\n'
    try:
        smtpObj = smtplib.SMTP(smtp_server, smtp_port)
    except Exception as e:
        print(e)
    smtpObj.ehlo()
    if smtp_use_tls == True :
        smtpObj.starttls()
    smtpObj.login(smtp_username, smtp_password) 
    smtpObj.sendmail(smtp_send_from, smtp_send_to, body) 
    smtpObj.quit()
    pass

def run_loop():
    while 1 == 1 :
        writeheader()
        browser = getdriver()
        soup = scrapsite(browser)  
        if soup is not None:
            parse_results(soup) 
        else:
            printLog("ERROR: Scrapping failed")
        # If we are booking stop here 
        if booking:
            printLog("Search complete, please see browser window to book your appointment\n")
            input("Press enter to exit application, please note this will close the browser window..")
            printLog("Thanks for scrapping, bye!")
            sys.exit()
        else:
            print("Sleeping for "+ str(sleepdelay)+" seconds ....\n")
            time.sleep(sleepdelay)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--booking", help="Booking mode, show results in browser", action="store_true")
    args = parser.parse_args()
    if args.booking:
        print("\nBooking mode enabled")
        booking = True
        headless = False
    run_loop()