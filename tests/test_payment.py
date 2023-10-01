import pytest
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load test data from the configuration file
with open('config/config.json') as config_file:
    config = json.load(config_file)


class TestsCheckout:
    @pytest.fixture
    def setup(self):
        driver = webdriver.Chrome()
        yield driver
        driver.quit()

    @pytest.mark.parametrize("url", config['urls'])
    def test_automation_steps(self, setup, url):
        driver = setup
        driver.maximize_window()
        wait = WebDriverWait(driver, 10)

        # Navigate to the URL
        driver.get(url)

        # Accessing element locators from the configuration
        splash_page_loading_xpath = config['element_locators']['splash_page_loading_xpath']
        pay_now_button_xpath = config['element_locators']['pay_now_button_xpath']
        loading_wrapper_xpath = config['element_locators']['loading_wrapper_xpath']
        table_span_xpath = config['element_locators']['table_span_xpath']
        split_bill_button_css = config['element_locators']['split_bill_button_css']
        split_the_bill_menu_xpath = config['element_locators']['split_the_bill_menu_xpath']
        custom_amount_button_xpath = config['element_locators']['custom_amount_button_xpath']
        custom_amount_input_xpath = config['element_locators']['custom_amount_input_xpath']
        confirm_button_xpath = config['element_locators']['confirm_button_xpath']
        order_summary_container_xpath = config['element_locators']['order_summary_container_xpath']
        tip_button_xpath = config['element_locators']['tip_button_xpath']
        card_number_input_xpath = config['element_locators']['card_number_input_xpath']
        date_input_xpath = config['element_locators']['date_input_xpath']
        cvv_input_xpath = config['element_locators']['cvv_input_xpath']
        pay_button_css = config['element_locators']['pay_button_css']
        secure_authentication_input_xpath = config['element_locators']['secure_authentication_input_xpath']

        # Test steps using the element locators
        # Step 1: Wait for the splash page to close
        wait.until(EC.invisibility_of_element_located((By.XPATH, splash_page_loading_xpath)))
        time.sleep(3)

        # Step 2: Click on Pay The Bill
        button = wait.until(EC.element_to_be_clickable((By.XPATH, pay_now_button_xpath)))
        button.click()

        # Step 3: Wait for the loading page to close
        wait.until(EC.invisibility_of_element_located((By.XPATH, loading_wrapper_xpath)))
        time.sleep(3)

        # Step 4: Verify that the Table checkout menu is opened
        wait.until(EC.visibility_of_element_located((By.XPATH, table_span_xpath)))
        time.sleep(3)

        # Step 5: Verify that Let’s Split The Bill button clickable and click on it
        split_bill_button = driver.find_element(By.CSS_SELECTOR, split_bill_button_css)
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", split_bill_button)
        split_bill_button.click()
        time.sleep(3)

        # Step 6: Verify that Split the bill menu is opened
        wait.until(EC.presence_of_element_located((By.XPATH, split_the_bill_menu_xpath)))
        time.sleep(3)

        # Step 7: Verify that Custom amount button is clickable and click on it
        custom_amount_button = wait.until(EC.element_to_be_clickable((By.XPATH, custom_amount_button_xpath)))
        custom_amount_button.click()
        time.sleep(3)

        # Step 8: Verify that input area exists and enter 10 in that area
        input_area = wait.until(EC.presence_of_element_located((By.XPATH, custom_amount_input_xpath)))
        input_area.send_keys("10")
        time.sleep(3)

        # Step 9: Get the value of the input and verify that the value is '10'
        input_value = input_area.get_attribute('value')
        assert input_value == '10', f"Expected input value to be '10', but found: {input_value}"
        time.sleep(3)

        # Step 10: Verify Confirm button exists and click on it
        confirm_button = wait.until(EC.element_to_be_clickable((By.XPATH, confirm_button_xpath)))
        confirm_button.click()
        time.sleep(3)

        # Step 11: Verify that the amount of share element contains the correct value
        order_summary_container = wait.until(EC.presence_of_element_located((By.XPATH, order_summary_container_xpath)))
        order_summary_value = order_summary_container.text
        assert "10.00" in order_summary_value, f"Expected '10.00' in div text, but found: {order_summary_value}"
        time.sleep(3)

        # Step 12: Verify that Tip button exists and click on it
        tip_button = wait.until(EC.presence_of_element_located((By.XPATH, tip_button_xpath)))
        tip_button.click()
        time.sleep(3)

        # Step 13: Verify that the amount of share element is updated after tip and contains the correct value
        order_summary_container = driver.find_element(By.XPATH, order_summary_container_xpath)
        order_summary_value = order_summary_container.text
        assert "11.50" in order_summary_value, f"Expected '11.50' in div text, but found: {order_summary_value}"
        time.sleep(3)

        # Step 14: Enter card number input area value
        card_number_input = wait.until(EC.presence_of_element_located((By.XPATH, card_number_input_xpath)))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", card_number_input)
        card_number_input.send_keys("424242424242")
        time.sleep(3)

        # Step 15: Enter date input area value
        date_input = wait.until(EC.presence_of_element_located((By.XPATH, date_input_xpath)))
        date_input.send_keys("0226")
        time.sleep(3)

        # Step 16: Enter CVV input area value
        cvv_input = wait.until(EC.presence_of_element_located((By.XPATH, cvv_input_xpath)))
        cvv_input.send_keys("100")
        time.sleep(3)

        # Step 17: Click on pay button
        pay_button_css_selector = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, pay_button_css)))
        pay_button_css_selector.click()
        time.sleep(5)

        # Step 18: Verify that 3D secure Authentication input field is shown successfully
        secure_authentication_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, secure_authentication_input_xpath)))
        assert secure_authentication_input.is_displayed()


if __name__ == "__main__":
    pytest.main()
