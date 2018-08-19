#!/usr/local/bin/python3 
# /usr/bin/python3
# -*- coding: utf-8 -*-

"""
Copyright (C) 2016   Tuxicoman

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for more details.
You should have received a copy of the GNU Affero General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.

---

Script modified by : 
  Francois B. (Makotosan/Shakasan)

Github : 
  https://github.com/shakasan/bgc_add_vol_pack

Changelog :
    - Updated for Python3
    - Any volume pack sizes
    - WebDriverWait increased up to 20 to try to avoid login failures
    - Headless mode added as optional parameter
    - repeat and packSize are optional with default value to 1 pack of 150 GB
"""
import logging
import time
import argparse
# pip3 install --user selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
# pip3 install --user pyvirtualdisplay
from pyvirtualdisplay import Display

log = logging.getLogger("proximus_add_volumes")


def main(args):
    display = None
    if args.headless:
        display = Display(visible=0, size=(1920, 1080))
        display.start()

    log.info("Starting ...")
    browser = webdriver.Firefox()
    # browser = webdriver.Chrome(args.driver)
    # https://stackoverflow.com/questions/34164831/selenium-crashing-chrome-automation-extension-has-crashed

    browser.get('https://www.proximus.be/login')
    time.sleep(3)
    wait = WebDriverWait(browser, 30)

    wait.until(lambda browser: browser.find_element_by_xpath('//a[text()="Accepter"]'))
    browser.find_element_by_xpath('//a[text()="Accepter"]').click()
    log.info("Cookies accepted mthfckr..")

    wait.until(lambda browser: browser.find_element_by_xpath('//a[text()="Fermer"]'))
    browser.find_element_by_xpath('//a[text()="Fermer"]').click()
    log.info("Closing GDPR fckng popup..")

    wait.until(lambda browser: browser.find_element_by_xpath('//input[@id="username"]'))
    log.info("Login...")
    browser.find_element_by_xpath('//input[@id="username"]').send_keys(args.login)
    browser.find_element_by_xpath('//input[@id="logincredentials"]').click()

    wait.until(lambda browser: browser.find_element_by_xpath('//input[@id="password"]'))
    browser.find_element_by_xpath('//input[@id="password"]').send_keys(args.password)
    browser.find_element_by_xpath('//input[@id="signin"]').click()

    wait.until(lambda browser: browser.find_element_by_xpath('//a[text()="Mes produits"]'))
    log.info("Logged in !")
    browser.find_element_by_xpath('//a[text()="Mes produits"]').click()

    real_url = "https://www.proximus.be/myproximus/fr/Personal/services/My-Products__/details/Internet/{0}".format(args.product)
    browser.get(real_url)

    for i in range(args.repeat):
        log.info("Step ", i + 1)
        wait.until(lambda browser: browser.find_element_by_xpath('//button[text()="Commander"]'))
        browser.find_element_by_xpath('//button[text()="Commander"]').click()
        log.info("Ordering pack..")

        wait.until(lambda browser: browser.find_element_by_xpath('//input[@id="termsAndconditionsCheckBox"]'))
        browser.find_element_by_xpath('//input[@id="termsAndconditionsCheckBox"]').click()
        log.info("Terms agreement..")
        wait.until(lambda browser: browser.find_element_by_xpath('//button[text()="Activer" and not(@disabled)]'))
        browser.find_element_by_xpath('//button[text()="Activer"]').click()
        log.info("Activation !")

    browser.quit()

    if args.headless == "yes":
        display.stop()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Add extra data volume pack to Proximus subscription')
    parser.add_argument('login', type=str, help='Proximus login email')
    parser.add_argument('password', type=str, help='Proximus password')
    parser.add_argument('--repeat', type=int, default=1, help='Number of volume packs to add (1 pack by default)')
    parser.add_argument('--packSize', type=str, default='150',
                        help='Volume size of the pack to add (150 GB by default)')
    # NB : 150GB is now the only available pack size
    parser.add_argument('--headless', type=int, default=1,
                        help='Headless mode (enabled by default ; using xvfb)')  # , action='store_true'
    parser.add_argument('--product', type=str, help='Product number (eg: 105487628394)')  # , action='store_true'
    parser.add_argument('--driver', type=str, help='DriverPath')

    arguments = parser.parse_args()
    main(arguments)
