from types import new_class
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep



# currently working as of 1/31/2021
def get_citys_in_range(zipcode, miles):

    DRIVER_PATH = 'C:\\Users\\Nick\\Documents\\Python Scripts\\chromedriver'
# want this to bbe in wodowless mode, can change with Headless
    options = Options()
    options.headless = True
    options.add_argument("--test-type")
    options.add_argument('--window-size=1920,1200')
    options.add_argument('--disable-gpu')
    options.add_argument('--ignore-certificate-errors')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(options = options, executable_path = DRIVER_PATH) 
    baseURL = 'https://www.freemaptools.com/find-zip-codes-inside-radius.htm'
    driver.get(baseURL) 
    soup = BeautifulSoup(driver.page_source, 'html.parser')


    if int(miles) > 250 or int(miles) < 0:
        miles = '20'
    # allows me to input the user miles that they'd like to look around max is 600
    miles_element = driver.find_element_by_xpath('//*[@id="tb_radius_miles"]')
    miles_element.clear()
    miles_element.click()
    miles_element.send_keys(miles)

    sleep(1)

    if len(zipcode) != 5:
        zipcode ='90210'
    zipcode_element = driver.find_element_by_id("locationSearchTextBox")
    zipcode_element.clear()
    zipcode_element.click()
    zipcode_element.send_keys(zipcode)

    sleep(1)

    # press the search button
    submit_button = driver.find_element_by_xpath('//*[@id="locationSearchButton"]')
    submit_button.click()

    sleep(5)

    grab_state = driver.find_element_by_xpath('//*[@id="tb_output_states"]')
    state = grab_state.get_attribute('value')

    close_cities = driver.find_element_by_xpath('//*[@id="tb_output_cities"]')
    cities = close_cities.get_attribute('value').replace(',', ' '+ state + ', ')
    #print(cities)

    cities_list = cities.split(', ')
    
    
    driver.quit()

    return cities_list

#get_citys_in_range('94002', '15')

#appartment_listings(city, type, beds, baths, amenities):


