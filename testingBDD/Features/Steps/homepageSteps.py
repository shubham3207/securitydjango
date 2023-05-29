from testingBDD.Utilities.readProperty import *
from testingBDD.Utilities.customLogger import *

from behave import *
from webdriver_manager.chrome import ChromeDriverManager

baseURL = ReadConfig.getURL()
mylogger = LogGen.loggen()

@given('Launch the browser')
def step_implementation(context):
    context.driver = webdriver.Chrome(ChromeDriverManager().install())
    mylogger.info("****Driver Installed******")
    context.driver.get(baseURL)
    mylogger.info("Browser Launched")

@then('verify the page ')
def step_imp(context):
    actual_title = context.driver.title
    expected_title = "HappyPaws"

    if expected_title==actual_title:
        assert True
        mylogger.info("****title matched******")
    else:
        mylogger.info("*****title not matche****")

@then('close the browser')
def step_impl(context):
    context.driver.close()
    mylogger.info('browse closed')
