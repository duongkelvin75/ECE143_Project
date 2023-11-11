#ECE 143 Group 1

import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

##Data scrapping code originates from https://github.com/andportnoy/smartercapes.com
def get_raw_cape_dataframe(page_url, data_url, page_title):
    '''
    Scrape date from CAPES and returns Dataframe of capes

    Args:
        page_url (str): url of page
        data_url (str): url of where data is located
        page_title (str): page title to confirm SSO login successful
    '''

    assert isinstance(page_url, str), "page_url is not a string"
    assert isinstance(data_url, str), "data_url is not a string"
    assert isinstance(page_title, str), "page title is not a string"

    # launch browser using Selenium, need to have Firefox installed
    print('Opening a browser window...')
    driver = webdriver.Firefox()
    print('Browser window open, loading the page...')

    # get the page that lists all the data, first try
    driver.get(page_url)
    print('Please enter credentials...')

    # wait until SSO credentials are entered
    wait = WebDriverWait(driver, 60)
    element = wait.until(expected_conditions.title_contains(page_title))

    # get the page that lists all the data
    # (%2C is the comma, drops all the data since every professor name has it)
    driver.get(data_url)

    # read in the dataset from the html file
    df = pd.read_html(driver.page_source)[0]
    print('Dataset parsed, closing browser window.')

    # destroy driver instance
    driver.quit()

    return df


page_url = 'https://cape.ucsd.edu/responses/Results.aspx'
data_url = 'https://cape.ucsd.edu/responses/Results.aspx?Name=%2C'
page_title = 'Course And Professor Evaluations (CAPE)'
x = get_raw_cape_dataframe(page_url, data_url, page_title)
path = 'ECE143_Project/data.csv'
x.to_csv(path, index=False)
