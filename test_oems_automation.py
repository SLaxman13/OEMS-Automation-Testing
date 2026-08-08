import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

class OEMSTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        chrome_options = Options()
        #chrome_options.add_argument("--headless=new")  # Runs quietly in background
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.implicitly_wait(5)

    def test_login_and_autosave(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000")

        # 1. Login
        driver.find_element(By.ID, "username").clear()
        driver.find_element(By.ID, "username").send_keys("student101")
        driver.find_element(By.ID, "password").clear()
        driver.find_element(By.ID, "password").send_keys("pass")
        driver.find_element(By.ID, "login-btn").click()

        # 2. Check if logged in
        timer = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "time-display")))
        self.assertTrue(timer.is_displayed())

        # 3. Test Auto Save by clicking first radio option
        radios = driver.find_elements(By.XPATH, "//input[@type='radio']")
        radios[0].click()

        status = WebDriverWait(driver, 5).until(
            EC.text_to_be_present_in_element((By.ID, "save-status"), "All changes saved")
        )
        self.assertTrue(status)

        # 4. Test Tab Switch Warning
        driver.execute_script("window.dispatchEvent(new Event('blur'));")
        warning_box = driver.find_element(By.ID, "warning-box")
        self.assertTrue(warning_box.is_displayed())
        print("\n--> ALL AUTOMATED TESTS PASSED SUCCESSFULLY!")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()