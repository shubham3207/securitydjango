class Home:
    lick_login_xpath = "//*[@id='sign']"

    def __init__(self, driver):
        self.driver = driver

    def clickOnSignIn(self):
        self.driver.find_element_by_xpath(self.lick_login_xpath).click()