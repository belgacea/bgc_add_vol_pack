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
"""
import sys
import logging
import time
import argparse
# pip3 install --user selenium
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# pip3 install --user pyvirtualdisplay
from pyvirtualdisplay import Display

log = logging.getLogger("proximus_add_volumes")
log.setLevel(logging.INFO)


def main(args):
    if args.log == 1:
        console_log()
    display = None
    if args.headless:
        display = Display(visible=0, size=(1920, 1080))
        display.start()

    log.info("Starting..")
    browser = webdriver.Firefox()
    # TODO https://stackoverflow.com/questions/34164831/selenium-crashing-chrome-automation-extension-has-crashed
    # browser = webdriver.Chrome(args.driver)
    wait = WebDriverWait(browser, args.timeout)
    browser.get('https://www.proximus.be/login')

    # TODO find out if possible to set timeout per wait call

    try:
        # Accepting cookies
        wait.until(lambda browser: browser.find_element_by_xpath(
            '//iframe[contains(@src,"https://consent-pref.trustarc.com/") and contains(@title, "TrustArc Cookie Consent Manager")]'))  # TODO merge with l59 in case of long loading
        frame = browser.find_element_by_xpath('//iframe[contains(@src,"https://consent-pref.trustarc.com/") and contains(@title, "TrustArc Cookie Consent Manager")]')

        browser.switch_to.frame(frame)
        log.info("Switching to cookie frame..")

        wait.until(lambda browser: browser.find_element_by_xpath(
            '//a[contains(@class, "call") and contains(@role, "button") and contains(text(), "Accepter")]'))
        browser.find_element_by_xpath('//a[contains(@class, "call") and contains(@role, "button") and contains(text(), "Accepter")]').click()
        log.info("Cookies accepted..")

        browser.switch_to.default_content()
        time.sleep(3)
    except TimeoutException as e:
        log.warning("Issue with GDPR cookie frame..", e)
        pass

    # wait.until(lambda browser: browser.find_element_by_xpath('//a[@id="gwt-debug-close_id"]'))
    # browser.find_element_by_xpath('//a[@id="gwt-debug-close_id"]').click()
    # log.info("Closing GDPR popup..")

    # Login
    log.info("Waiting login fields..")
    wait.until(lambda browser: browser.find_element_by_xpath('//input[@id="username"]'))

    # TODO find out how to delete this shit without waiting
    # wait.until(lambda browser: browser.find_element_by_id('_hj_feedback_container'))
    # remove_feedback_button(browser)

    log.info("Login..")
    browser.find_element_by_xpath('//input[@id="username"]').send_keys(args.login)
    # browser.find_element_by_xpath('//button[@id="logincredentials"]').click() # No longer needed

    wait.until(lambda browser: browser.find_element_by_xpath('//input[@id="password"]'))
    browser.find_element_by_xpath('//input[@id="password"]').send_keys(args.password)
    wait.until(lambda browser: EC.element_to_be_clickable(browser.find_element_by_xpath('//button[@id="signin"]')))
    browser.find_element_by_xpath('//button[@id="signin"]').click()

    # Entering customer dashboard
    wait.until(EC.url_to_be("https://www.proximus.be/myproximus/fr/Personal/services/My-overview__"))
    log.info("Logged in !")

    real_url = "https://www.proximus.be/myproximus/fr/Personal/services/My-Products__/details/Internet/{0}".format(args.product)
    browser.get(real_url)

    # Ordering volume packs
    for i in range(args.repeat):
        log.info("Step {0}".format(i + 1))
        wait.until(lambda browser: browser.find_element_by_xpath(
            '//button[contains(@data-mp-analytics-element-clicked, "Extra Volume Free")]'))
        browser.find_element_by_xpath(
            '//button[contains(@data-mp-analytics-element-clicked, "Extra Volume Free")]').click()
        log.info("Ordering pack..")

        wait.until(lambda browser: browser.find_element_by_xpath('//input[@id="termsAndconditionsCheckBox"]'))
        browser.find_element_by_xpath('//input[@id="termsAndconditionsCheckBox"]').click()
        log.info("Terms agreement..")

        wait.until(lambda browser: EC.element_to_be_clickable(browser.find_element_by_xpath(
            '//button[@data-ng-click="confirm()"]')))
        browser.find_element_by_xpath('//button[@data-ng-click="confirm()"]').click()
        log.info("Activation")

    log.info("Done !")
    browser.quit()

    if args.headless == "yes":
        display.stop()


def remove_feedback_button(browser):
    js = "var shit=document.getElementById('_hj_feedback_container');shit.remove()"
    browser.execute_script(js)
    log.info("Removing feedback button..")


def console_log():
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    log.addHandler(ch)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Add extra data volume pack to Proximus subscription')
    parser.add_argument('login', type=str, help='Proximus login email')
    parser.add_argument('password', type=str, help='Proximus password')
    parser.add_argument('--repeat', type=int, default=1, help='Number of volume packs to add (1 pack by default)')
    parser.add_argument('--headless', type=int, default=1,
                        help='Headless mode (enabled by default ; using xvfb)')
    parser.add_argument('--product', type=str, help='Product number (eg: 105487628394)')
    parser.add_argument('--driver', type=str, help='DriverPath')
    parser.add_argument('--timeout', type=int, default=120, help='Time out in seconds') # Huge time out because proximus servers are not so good
    parser.add_argument('--log', type=int, default=0, help='Console log')

    arguments = parser.parse_args()
    main(arguments)
