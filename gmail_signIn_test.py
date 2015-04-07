# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time


class GmailSignIn(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        #alternative webdriver.Chrome
        #self.driver = webdriver.Chrome(executable_path='/Users/bartoszkabik/Development/myenv/testy selenium/chromedriver')
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.google.pl/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_gmail_sign_in(self):
        driver = self.driver
        driver.get(self.base_url + "/?gws_rd=ssl")
        driver.find_element_by_id("gb_70").click()
        driver.find_element_by_id("link-signup").click()
        self.assertEqual(u"Utwórz konto Google", driver.find_element_by_css_selector("h1").text)

        # test blank from
        driver.find_element_by_id("submitbutton").click()
        self.assertEqual(u"To pole nie może być puste.", driver.find_element_by_id("errormsg_0_LastName").text)
        self.assertEqual(u"To pole nie może być puste.", driver.find_element_by_id("errormsg_0_GmailAddress").text)
        self.assertEqual(u"To pole nie może być puste.", driver.find_element_by_id("errormsg_0_Passwd").text)
        self.assertEqual(u"To pole nie może być puste.", driver.find_element_by_id("errormsg_0_PasswdAgain").text)
        self.assertEqual(u"To pole nie może być puste.", driver.find_element_by_id("errormsg_0_BirthDay").text)
        self.assertEqual(u"To pole nie może być puste.", driver.find_element_by_id("errormsg_0_Gender").text)
        self.assertEqual(u"Aby korzystać z naszych usług, musisz się zgodzić na Warunki korzystania z usług Google.",
                         driver.find_element_by_id("errormsg_0_TermsOfService").text)

        # refresh page, waiting for load page
        driver.set_page_load_timeout(60)

        #  Alternative for waiting for load page
        # driver.refresh()
        # for i in range(60):
        #     try:
        #         if u"Utwórz konto Google" == driver.title: break
        #     except:
        #         pass
        #     time.sleep(1)
        # else:
        #     self.fail("time out")


        # test illegals characters in First Name nad Last Name fields
        driver.find_element_by_id("FirstName").clear()
        driver.find_element_by_id("FirstName").send_keys("--!@#_WRF-fs2")
        driver.find_element_by_id("LastName").clear()
        driver.find_element_by_id("LastName").send_keys(u"$-@1Wsdśśśśśśśśśś")

        # test illegals type of characetrs in Adress@ field
        driver.find_element_by_id("GmailAddress").clear()
        driver.find_element_by_id("GmailAddress").send_keys("-!@#wsdof")
        driver.find_element_by_id("GmailAddress").send_keys(Keys.TAB)
        self.assertEqual(u"Używaj tylko liter (a–z), cyfr i kropek.",
                         driver.find_element_by_id("errormsg_0_GmailAddress").text)
        # test illegals lenght of characetrs in Adress@ field
        driver.find_element_by_id("GmailAddress").clear()
        driver.find_element_by_id("GmailAddress").send_keys("A")
        driver.find_element_by_id("GmailAddress").send_keys(Keys.TAB)
        self.assertEqual(u"Użyj od 6 do 30 znaków.", driver.find_element_by_id("errormsg_0_GmailAddress").text)

        # test illegals lenght of characters in Password field
        driver.find_element_by_id("Passwd").clear()
        driver.find_element_by_id("Passwd").send_keys("123")
        driver.find_element_by_id("PasswdAgain").clear()
        driver.find_element_by_id("PasswdAgain").send_keys("123")
        driver.find_element_by_id("PasswdAgain").send_keys(Keys.TAB)
        self.assertEqual(u"Krótkie hasła łatwo odgadnąć. Spróbuj ponownie, używając co najmniej 8 znaków.",
                         driver.find_element_by_id("errormsg_0_Passwd").text)
        # test Password == Reapeted password
        driver.find_element_by_id("Passwd").clear()
        driver.find_element_by_id("Passwd").send_keys("Q!W@E#R$")
        driver.find_element_by_id("PasswdAgain").clear()
        driver.find_element_by_id("PasswdAgain").send_keys("Q!W@E#R$123")
        driver.find_element_by_id("PasswdAgain").send_keys(Keys.TAB)
        self.assertEqual(u"Te hasła nie pasują do siebie. Spróbuj ponownie.",
                         driver.find_element_by_id("errormsg_0_PasswdAgain").text)

        # test not allowed type of characters in Brith Day field
        driver.find_element_by_id("BirthDay").clear()
        driver.find_element_by_id("BirthDay").send_keys("99")
        driver.find_element_by_id("BirthDay").send_keys(Keys.TAB)

        # test not allowed type of characters in Birth Year field
        driver.find_element_by_id("BirthYear").clear()
        driver.find_element_by_id("BirthYear").send_keys("012f")


        # Select birth month from dropdown menu alternative
        # ALTERNATYWA
        # element=driver.find_element_by_xpath("//span[@id='BirthMonth']/div")
        # action = webdriver.common.action_chains.ActionChains(driver)
        # action.move_to_element_with_offset(element, 5, 5)
        # action.click()
        # action.perform()

        #select birth month from dropdown menu
        driver.find_element_by_xpath("//span[@id='BirthMonth']/div").click()
        driver.find_element_by_xpath("//div[@id=':2']/div").click()

        driver.find_element_by_id("BirthDay").send_keys(Keys.TAB)
        self.assertEqual(
            u"Dzień nie wygląda na prawidłowy. Pamiętaj, aby użyć 2-cyfrowej liczby oznaczającej dzień miesiąca.",
            driver.find_element_by_id("errormsg_0_BirthDay").text)


        # test select gender field
        element = driver.find_element_by_xpath("//div[@id='Gender']/div")
        action = webdriver.common.action_chains.ActionChains(driver)
        action.move_to_element_with_offset(element, 5, 5)
        action.click()
        action.send_keys(Keys.ARROW_DOWN, Keys.ENTER)
        action.perform()
        self.assertNotEqual(u"To pole nie może być puste.", driver.find_element_by_id("errormsg_0_Gender").text)

        #joke :-)
        driver.find_element_by_id("recaptcha_response_field").send_keys("JESTEM ROBOTEM :)")

        #test select check box in Terms field
        driver.find_element_by_id("TermsOfService").click()
        self.assertNotEqual(u"Aby korzystać z naszych usług, musisz się zgodzić na Warunki korzystania z usług Google.",
                         driver.find_element_by_id("errormsg_0_TermsOfService").text)

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
