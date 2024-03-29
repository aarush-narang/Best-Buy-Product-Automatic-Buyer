import time
import random
from selenium import webdriver
from datetime import datetime
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select

color = {
    'RED': '\033[91m',
    'YELLOW': '\033[93m',
    'GREEN': '\033[92m',
    'CYAN': '\033[96m',
    'DARKCYAN': '\033[36m',
    'BLUE': '\033[94m',
    'PURPLE': '\033[95m',
}

EMAIL = ''
PHONENUMBER = ''  # only the 10 digits of your phone number, not the +1 or whatever
CREDITCARDNUMBER = ''
CREDITCARDEXPDATEMONTH = ''  # make sure to put it as a 0 padded number (ex: 01 not 1, or 02 not 2)
CREDITCARDEXPDATEYEAR = ''  # full year (ex: 2022 not 22, or 2019 not 19)
CREDITCARDCVV = ''
FIRSTNAME = ''
LASTNAME = ''
ADDRESSANDSTREET = ''  # make sure to put only the address and street (ex: 1234 Python St) in that exact form
CITY = ''
STATE = ''  # make sure to put abbreviated form (ex: CA not ca or california or California, TX not tx or texas or Texas)
ZIP = ''
PRODUCTLINK = ''
LOCATIONOFCHROMEDRIVER = ''  # LOCATION OF YOUR CHROMEDRIVER AND MAKE SURE TO INSTALL SELENIUM --> INFO HERE: (https://www.youtube.com/watch?v=7R5n0sNSza8)
SENDTEXTUPDATES = False  # 'True' or 'False' only; if True, the number entered above will receive texts on the status of their orders
TESTMODE = False  # 'True' or 'False' only; if True, product will not be bought and text updates will be off


def findDateTime(textColor):
    now = datetime.now()
    dt_string = now.strftime("%m/%d/%Y %H:%M:%S:%f")
    return f'\033[1m\033[4m{textColor}{dt_string}\033[0m'
    #       BOLD (1m) UNDERLINE (4m)             END (0m)


def clickBuyButton(browser):
    while True:
        try:
            # If this comes out true then item is not in stock
            browser.find_element_by_class_name('c-button-disabled')

            # button was not ready so refresh browser and check again after 1 sec
            print(f'Add to cart button not ready.  {findDateTime(color["RED"])}')
            time.sleep(random.randint(1, 3))
            browser.refresh()
        except NoSuchElementException:
            # if button is found, it gets clicked
            browser.find_element_by_class_name('c-button-primary').click()
            print(f'Add to cart button was clicked.  {findDateTime(color["GREEN"])}')
            return


def clickCheckoutButton(browser):
    checkoutBtnCount = 1
    while True:
        try:
            # If this comes out true then button is loaded
            checkoutBtn = browser.find_element_by_class_name('checkout-buttons__checkout')
            checkoutBtn.click()
            print(f'Checkout button was clicked.  {findDateTime(color["GREEN"])}')
            return True, f'Checking out.  {findDateTime(color["GREEN"])}'
        except NoSuchElementException:
            # if button is not loaded:
            if checkoutBtnCount >= 30:
                return False, f'Failed to find checkout button.  {findDateTime(color["RED"])}'
            print(f'Checkout button was not found, retrying.  {findDateTime(color["RED"])}')
            checkoutBtnCount += 1
            time.sleep(0.1)
            continue


def continueAsGuest(browser):
    contasguestcount = 1
    while True:
        try:
            browser.find_element_by_class_name('cia-guest-content__continue').click()
            print(f'Clicked continue as guest button.  {findDateTime(color["GREEN"])}')
            return True, f'Continued as guest.  {findDateTime(color["GREEN"])}'
        except NoSuchElementException:
            if contasguestcount >= 30:
                return False, f'Failed to click continue as guest.  {findDateTime(color["RED"])}'
            print(f'Unable to find continue as guest button, retrying.  {findDateTime(color["RED"])}')
            contasguestcount += 1
            time.sleep(0.1)
            continue


def contactInfoAndLocation(browser):
    contactinfocount = 1
    while True:
        try:
            browser.find_element_by_id('user.emailAddress').send_keys(EMAIL)
            browser.find_element_by_id('user.phone').send_keys(PHONENUMBER)
            if SENDTEXTUPDATES and not TESTMODE:
                browser.find_element_by_id('text-updates').click()
            browser.find_element_by_class_name('btn-secondary').click()  # enter info submit button
            print(f'Inputted contact info.  {findDateTime(color["GREEN"])}')
            return True, f'Inputted contact info.  {findDateTime(color["GREEN"])}'
        except NoSuchElementException:
            if contactinfocount >= 30:
                return False, f'Failed to input contact info.  {findDateTime(color["RED"])}'
            print(f'Unable to input contact info, retrying.  {findDateTime(color["RED"])}')
            contactinfocount += 1
            time.sleep(0.1)
            continue


def paymentInfo(browser):
    paymentinfocount = 1
    while True:
        try:
            # PAYMENT AND CONTACT INFO
            browser.find_element_by_id('optimized-cc-card-number').send_keys(CREDITCARDNUMBER)
            Select(browser.find_element_by_name('expiration-month')).select_by_visible_text(CREDITCARDEXPDATEMONTH)
            Select(browser.find_element_by_name('expiration-year')).select_by_visible_text(CREDITCARDEXPDATEYEAR)
            browser.find_element_by_id('credit-card-cvv').send_keys(CREDITCARDCVV)

            browser.find_element_by_id('payment.billingAddress.firstName').send_keys(FIRSTNAME)
            browser.find_element_by_id('payment.billingAddress.lastName').send_keys(LASTNAME)

            browser.find_element_by_id('payment.billingAddress.street').send_keys(ADDRESSANDSTREET)
            # click on random part of page to remove autocomplete suggestions of addresses
            browser.find_element_by_class_name('order-summary__label').click()
            browser.find_element_by_id('payment.billingAddress.city').send_keys(CITY)
            Select(browser.find_element_by_id('payment.billingAddress.state')).select_by_visible_text(STATE)
            browser.find_element_by_id('payment.billingAddress.zipcode').send_keys(ZIP)

            # PLACE ORDER
            if not TESTMODE:
                browser.find_element_by_class_name('btn-primary').click()  # place order button
                # CHECK IF MODAL ABOUT ADDRESS APPEARS (AFTER 1 SECOND BECAUSE IT TAKES TIME TO POP UP)
                time.sleep(1)
                try:
                    browser.find_element_by_xpath('/html/body/div[4]/div[2]/div/div/div')
                    try:
                        browser.find_element_by_xpath('/html/body/div[4]/div[2]/div/div/div/button[1]').click()
                    except NoSuchElementException:
                        return False, f'Failed to find keep address button, restarted.  {findDateTime(color["RED"])}'
                except NoSuchElementException:
                    print(f'Modal not found.  {findDateTime(color["DARKCYAN"])}')

                # IF MODAL WAS THERE, KEEP ADDRESS BUTTON WAS CLICKED, IF MODAL WASNT THERE, ORDER WAS PLACED (MODAL SHOULD NOT APPEAR)
                print(f'Inputted payment info and ordered item(s).  {findDateTime(color["GREEN"])}')
            else:
                print(f'Inputted all info, order was not placed {findDateTime(color["DARKCYAN"])}')
                time.sleep(10000)

            return True, f'Inputted payment info.  {findDateTime(color["GREEN"])}'
        except NoSuchElementException:
            if paymentinfocount >= 60:
                return False, f'Failed to input payment info.  {findDateTime(color["RED"])}'
            print(f'Unable to input payment info, retrying.  {findDateTime(color["RED"])}')
            paymentinfocount += 1
            time.sleep(0.1)
            continue


def main():
    # chromedriver
    browser = webdriver.Chrome(LOCATIONOFCHROMEDRIVER)

    browser.get(PRODUCTLINK)

    clickBuyButton(browser)
    browser.get('https://bestbuy.com/cart')
    print(f'Inside Cart.  {findDateTime(color["GREEN"])}')
    clickcheckoutbuttonresponse = clickCheckoutButton(browser)
    if not clickcheckoutbuttonresponse[0]:
        browser.close()
        print(clickcheckoutbuttonresponse[1])
        return main()
    signinresponse = continueAsGuest(browser)
    if not signinresponse[0]:
        browser.close()
        print(signinresponse[1])
        return main()
    contactinforesponse = contactInfoAndLocation(browser)
    if not contactinforesponse[0]:
        browser.close()
        print(contactinforesponse[1])
        return main()
    paymentinforesponse = paymentInfo(browser)
    if not paymentinforesponse[0]:
        browser.close()
        print(paymentinforesponse[1])
        return main()
    time.sleep(100) # delay here to make sure order goes through in case of extreme traffic through their webpage

if __name__ == '__main__':
    main()
