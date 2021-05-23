from selenium import webdriver
import pyautogui
import time
from settings import upstox_username, upstox_password, year_of_birth

options = webdriver.ChromeOptions()
options.add_argument('user-data-dir=C:\\Users\\Harnoor singh\\AppData\\Local\\Google\\Chrome\\User Data')
options.add_argument('profile-directory=Profile 2')
driver = webdriver.Chrome(options=options, executable_path="C:\Permanent files\chromedriver.exe")
driver.maximize_window()

driver.implicitly_wait(10)
driver.get(
    "https://login.upstox.com/?client_id=PW3-6Agd37PB52Q6B6DDpYWLuT7b&platform_id=PW3&redirect_path=%2F&redirect_uri=https%3A%2F%2Fpro.upstox.com")
driver.implicitly_wait(10)

pyautogui.click(x=605, y=444, clicks=3, interval=1, button='left')
driver.implicitly_wait(10)
pyautogui.typewrite(f'{upstox_password}', interval=0.1)
driver.implicitly_wait(10)

driver.find_element_by_id('userCode').send_keys(upstox_username)
driver.find_element_by_xpath('//*[@id="submit-btn"]/div/div[1]').click()
driver.implicitly_wait(10)

DOB = driver.find_element_by_xpath('//*[@id="yob"]')
DOB.send_keys(year_of_birth)
driver.implicitly_wait(10)

#pyautogui.click(x=168, y=248, clicks=2, interval=1, button='left')  ALSO WORK


def buy_order():
    # click on icici bank
    driver.find_element_by_xpath('/html/body/main/div[1]/aside/div[2]/div/div/div[2]/div/div[1]').click()
    driver.find_element_by_xpath('/html/body/main/div[1]/aside/div[2]/div/div/div[2]/div/div[1]/div[2]/div[2]/div/div[1]/div[1]').click()
    time.sleep(2)

    # filling the quantity
    driver.find_element_by_xpath('//*[@id="quantity"]').send_keys(1)
    time.sleep(2)

    # two clicks for confirmation
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="root"]/div[1]/div/div[2]/div/div/div/form/div[2]/button').click()
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="root"]/div[1]/div/div[2]/div/div/div/form/div/div/button/div/div[2]').click()


def sell_order():
    driver.find_element_by_xpath('/html/body/main/div[1]/aside/div[2]/div/div/div[2]/div/div[1]').click()
    driver.find_element_by_xpath(
        '/html/body/main/div[1]/aside/div[2]/div/div/div[2]/div/div[1]/div[2]/div[2]/div/div[1]/div[1]').click()
    time.sleep(2)

    driver.find_element_by_xpath('//*[@id="sellBtn"]').click()

    # filling the quantity
    driver.find_element_by_xpath('//*[@id="quantity"]').send_keys(1)
    time.sleep(2)

    # two clicks for confirmation
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="root"]/div[1]/div/div[2]/div/div/div/form/div[2]/button').click()
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="root"]/div[1]/div/div[2]/div/div/div/form/div/div/button/div/div[2]').click()

# RUNNING TEST TO MAKE SURE EVERYTHING IS ALL RIGHT


user_confirmation = str
while user_confirmation != 'y':
    print('TESTING')
    niftybank_change_intial = driver.find_element_by_xpath('//*[@id="NSE_INDEX-Nifty Bank"]/div[3]/div[2]').text
    niftybank_change = float(niftybank_change_intial[-7:-2])
    icici_bank_change_intial = driver.find_element_by_xpath('//*[@id="NSE_EQ-4963"]/div[3]/div[2]').text
    icici_bank_change = float(icici_bank_change_intial[-7:-3])
    print(f'niftybank_change_intial = {niftybank_change_intial}')
    print(f'niftybank_change = {niftybank_change}')
    print(f'icici_bank_change_intial = {icici_bank_change_intial}')
    print(f'icici_bank_change = {icici_bank_change}')

    user_confirmation = input("Does the result match the number in you upstox dashboard, if yes then type 'y' = ")

    if user_confirmation == 'y':
        print()
        print("Please edit the code and don't forget to implement in main calculation part of code!")
        break
    else:
        pass

# main calculation start here------------------

time.sleep(5)

tries = 1
order = 0

while tries > 0:
    print(f'{tries} try')
    niftybank_change_intial = driver.find_element_by_xpath('//*[@id="NSE_INDEX-Nifty Bank"]/div[3]/div[2]').text
    niftybank_change = float(niftybank_change_intial[-7:-2])
    icici_bank_change_intial = driver.find_element_by_xpath('//*[@id="NSE_EQ-4963"]/div[3]/div[2]').text
    icici_bank_change = float(icici_bank_change_intial[-7:-3])

    if niftybank_change_intial[0] == '-' and icici_bank_change_intial[0] == '-':
        change_in_percent = icici_bank_change - niftybank_change
        print('Nifty bank is Negative')
        print('ICICI Bank is Negative')
    elif niftybank_change_intial[0] == '+' and icici_bank_change_intial[0] == '+':
        change_in_percent = niftybank_change - icici_bank_change
        print('Nifty bank is Positive')
        print('ICICI Bank is Positive')
    elif niftybank_change_intial[0] == '-' and icici_bank_change_intial[0] == '+':
        change_in_percent = - niftybank_change - icici_bank_change
        print('Nifty bank is Negative')
        print('ICICI Bank is Positive')
    else:   # niftybank_change_intial[0] == '+' and icici_bank_change_intial[0] == '-'
        change_in_percent = niftybank_change + icici_bank_change
        print('Nifty bank is Positive')
        print('ICICI Bank is Negative')

    print(f'change in percent is {change_in_percent}')

    # - 0.20% to 0.20% = NO action
    # no of order shouldn't exceed 3
    # if percent is between 0.05 to -0.05, EXIT all the positions

    if 0.05 > change_in_percent > -0.05:
        while order != 0:
            if order < 0:
                buy_order()
                print('Exiting the BUY position')
            else:
                sell_order()
                print('Exiting the SELL position')
        print('EXIT zone, No action taken')

    elif 0.05 <= change_in_percent < 0.20 or - 0.05 >= change_in_percent > - 0.20:
        print("No order is placed [NO Action Zone] ")

    elif 0.30 >= change_in_percent >= 0.20:
        if order < 1:
            buy_order()
            order += 1
            print(' 1 share is bought')
        else:
            print('Buy order limit is exceeded')

    elif 0.35 >= change_in_percent > 0.30:
        if order < 2:
            buy_order()
            order += 1
            print(' 1 share is bought')
        else:
            print('Buy order limit is exceeded')

    elif 0.50 >= change_in_percent > 0.35:
        if order < 3:
            buy_order()
            order += 1
            print(' 1 share is bought')
        else:
            print('Buy order limit is exceeded')

    elif -0.30 <= change_in_percent <= -0.20:
        if order > -1:
            sell_order()
            order -= 1
            print('1 share is sold')
        else:
            print('sell order limit is exceeded')

    elif -0.35 <= change_in_percent < -0.30:
        if order > -2:
            sell_order()
            order -= 1
            print('1 share is sold')
        else:
            print('sell order limit is exceeded')

    elif -0.50 <= change_in_percent < -0.35:
        if order > -3:
            sell_order()
            order -= 1
            print('1 share is sold')
        else:
            print('sell order limit is exceeded')

    else:
        pass

    print(f'Number of orders = {order}')
    print()
    tries += 1
    time.sleep(7)
