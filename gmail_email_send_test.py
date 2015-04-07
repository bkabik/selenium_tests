# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest,time


class GmailSendTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://accounts.google.com/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_gmail_send(self):
        driver = self.driver
        driver.get(
            self.base_url + "/ServiceLogin?service=mail&passive=true&rm=false&continue=https://mail.google.com/mail/&ss=1&scc=1&ltmpl=default&ltmplcache=2&emr=1&osid=1")
        #Login account
        driver.find_element_by_id("Email").clear()
        driver.find_element_by_id("Email").send_keys("jan.firmatest@gmail.com")
        driver.find_element_by_id("Passwd").clear()
        driver.find_element_by_id("Passwd").send_keys("k1k2k3k4")
        driver.find_element_by_id("signIn").click()
        driver.set_page_load_timeout(60)

        #send test email
        driver.find_element_by_xpath("//div[@id=':3c']/div/div").click()
        driver.find_element_by_name("to").send_keys("andrzej.firmatest@gmail.com")
        driver.find_element_by_name("subjectbox").send_keys("Testowy email selenium1")
        driver.find_element_by_xpath(".//*[@class='Am Al editable LW-avf']").send_keys(
            "Testowa zawartosc emaila selenium")
        driver.find_element_by_xpath(".//*[@class='T-I J-J5-Ji aoO T-I-atl L3']").click()


    def test_gmail_send_received(self):
        driver = self.driver
        driver.get(
            self.base_url + "/ServiceLogin?service=mail&passive=true&rm=false&continue=https://mail.google.com/mail/&ss=1&scc=1&ltmpl=default&ltmplcache=2&emr=1&osid=1")
        driver.find_element_by_id("Email").send_keys("andrzej.firmatest@gmail.com")
        driver.find_element_by_id("Passwd").send_keys("k1k2k3k4")
        driver.find_element_by_id("signIn").click()
        driver.set_page_load_timeout(60)

        #check if email was received
        self.assertEqual(u" - Testowa zawartosc emaila selenium",
                         driver.find_element_by_xpath(".//*[@class='y6']/span[2]").text)
        driver.find_element_by_css_selector("div.y6")
        driver.find_element_by_css_selector("div.y6").click()
        driver.title == "Testowy email selenium1 - andrzej.firmatest@gmail.com - Gmail"

        #deleted received email
        driver.find_element_by_xpath(".//*[@class='aeH']/div[2]/div[1]/div/div[2]/div[3]").click()
        self.assertNotEqual(u" - Testowa zawartosc emaila selenium", driver.find_element_by_xpath(
            ".//*[@class='y6']/span[2]").text)

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e:
            return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to_alert()
        except NoAlertPresentException, e:
            return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)


if __name__ == "__main__":
    unittest.main()
