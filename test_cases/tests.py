from BasicWebDriver.MyWebDriver import BasicSeleniumDriver, selenium_test


def test_launch_driver():
    driver = BasicSeleniumDriver()
    driver.quit()


@selenium_test
def test_jira_invalid_login(driver, headless=True, capture_screenshot=True):

    # visit Jira
    driver.get('https://id.atlassian.com/login')

    # input invalid username
    driver.get_element('//input[@name="username"]').send_keys('notvalidemail@gmail.com')

    # click continue button
    driver.get_element('//button[@id="login-submit"]').click()

    # assert the signup option is displayed
    assert driver.get_element(f'//button[@id="signup-submit"]')

    return True


@selenium_test
def test_jira_valid_login(driver, headless=True, capture_screenshot=True):

    # visit Jira
    driver.get('https://id.atlassian.com/login')

    # input invalid username
    driver.get_element('//input[@name="username"]').send_keys('sebcampos23@gmail.com')

    # click continue button
    driver.get_element('//button[@id="login-submit"]').click()

    # assert the `continue with google` appears for existing user
    assert driver.get_element(f"//button[@id='social-login-submit']//span[contains(text(), 'Continue with Google')]")

    return True

@selenium_test
def test_made_to_fail(driver, headless=True, capture_screenshot=True):

    # visit fake page
    driver.get('https://notarealsite.org')

    assert driver.get_element('//input[@name="username"]').send_keys('sebcampos23@gmail.com')