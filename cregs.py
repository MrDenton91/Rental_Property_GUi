
from bs4 import BeautifulSoup
from time import sleep



from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.action_chains import ActionChains

DRIVER_PATH = 'C:\\Users\\Nick\\Documents\\Python Scripts\\chromedriver'
# want this to bbe in wodowless mode, can change with Headless
options = Options()
options.headless = True
options.add_argument("--test-type")
options.add_argument('--window-size=1920,1200')
options.add_argument('--disable-gpu')
options.add_argument('--ignore-certificate-errors')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_experimental_option("detach", True)




#    appartment_listings('Belmont CA', 'appartment', '1', '1', ['parking'])
all_url =[]
def craigslist_findings(city, type, bed, bath, amenities):
    
    driver = webdriver.Chrome(options = options, executable_path = DRIVER_PATH)
    url = 'https://www.google.com/'
    action = ActionChains(driver) 
    page = 'craigslist'
    #city = 'Belmont, CA'

    look_for = page + ' ' + city

    

    craigslist_search = str(bed) + ' bedroom ' + str(bath) + ' bathroom with ' + amenities

    
    driver.get(url)
    ##search engine and search
    

    search = driver.find_element_by_xpath('/html/body/div[1]/div[3]/form/div[2]/div[1]/div[1]/div/div[2]/input')
    search.click()
    search.send_keys(look_for)
    search.send_keys(Keys.RETURN)
    try:
        
        city_page = driver.find_element_by_xpath('//*[@id="rso"]/div/div[1]/div/div[1]/a/h3/span')
        city_page.click()
    except:
        try:
            
            driver.find_element_by_xpath('//*[@id="rso"]/div[1]/div/div[1]/a/h3/span').click()
        except:
            driver.find_element_by_xpath(('//*[@id="rso"]/div/div[1]/div/div/div[1]/a/h3/span')).click()
    sleep(4)
    rental_page = driver.find_element_by_xpath('//*[@id="hhh0"]/li[1]/a')
    rental_page.click()

    search_craig = driver.find_element_by_xpath('//*[@id="query"]')
    search_craig.click()
    search_craig.send_keys(craigslist_search)

    ## enter search result
    driver.find_element_by_xpath('//*[@id="searchform"]/div[1]/button/span[1]').click()
    ## select craiglist suggestion
    try:
        driver.find_element_by_xpath('//*[@id="sortable-results"]/div[1]/ul/li/a').click()
    except:
        pass
    ## availabity and winthin 30 days
    #driver.find_element_by_xpath('//*[@id="searchform"]/div[2]/div[2]/div[8]/select').click()
    #driver.find_element_by_xpath('//*[@id="searchform"]/div[2]/div[2]/div[8]/select/option[2]').click()

    sleep(5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    all_listings = []

    all_prices = ['0']

    state = True
    while state:
        driver.implicitly_wait(2)
        for key, price in enumerate(soup.find_all('span', class_ = 'result-price')):
                modded_price = str(price.text)
                #modded_price = modded_price.repalce(' ','').replace('$','').replace(',','')
                if key%2 == 1:
                    pass
                elif key == 0:
                   all_prices.append(str(price.text)) 
                else:
                    all_prices.append(str(price.text))
                    #print(modded_price)

        for list in soup.find_all('li', class_ = 'result-row'):

            if list.a['href'] not in all_listings:
                all_listings.append(list.a['href'])    
            else:
                pass
        try: 
            #next_page_button = driver.find_elements_by_xpath('//*[@id="searchform"]/div[5]/div[3]/span[2]/a[3]')
                        
            next_page_button = driver.find_element_by_xpath('//*[@id="searchform"]/div[5]/div[3]/span[2]/a[3]')   
            
            next_page_button.click()   
            
        except:
            state = False
            
    #driver.delete_all_cookies()
    final_price =[]   
    all_prices.remove("0")
    for price in all_prices:
        if int((price.replace(",",'').replace("$",''))) < 20000 and int((price.replace(",",'').replace("$",''))) > 100:
                final_price.append(price)
        else:
            final_price.append('None')
    
    driver.close()
    #print(len(all_listings))
    #print(len(all_prices))
    return all_listings, final_price


def grab_sqft(all_listings,ammenities_list, house):
    driver = webdriver.Chrome(options = options, executable_path = DRIVER_PATH)
    driver.get(all_listings[0])

    all_sqrt = []
    lxury_list = []
    #house_f = []

    for listing in all_listings:

        try:
            
            driver.get(listing)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            driver.implicitly_wait(1)
            sqrt = driver.find_element_by_xpath('/html/body/section/section/section/div[1]/p[1]/span[2]/b')
            all_sqrt.append(sqrt.text)

#            tags = driver.find_element_by_xpath('/html/body/section/section/section/div[1]/p[2]')
#            if house == True and 'house' in tags.text.lower():
#                house_f.append(1)
#            elif house == False and 'appartment' in tags.text.lower():
#                house_f.append(1)
#            else:
#                house.append(0)


            content_f = driver.find_element_by_xpath('//*[@id="postingbody"]').text

            if 'luxury' in str(ammenities_list) or 'modern' in str(ammenities_list):
                if 'luxury' in content_f.lower():
                    lxury_list.append(1)
                else:
                    lxury_list.append(0)
            elif 'luxury' not in str(ammenities_list) or 'modern' not in str(ammenities_list):
                if 'luxury' not in content_f.lower():
                    lxury_list.append(1)
                else: 
                    lxury_list.append(0)
        except:
            all_sqrt.append('None')
            lxury_list.append((0))
    driver.quit()
    #print(all_sqrt)
    #print(lxury_list)
    return all_sqrt, lxury_list, #house_f




def posted(all_listings):
    post_time = ['Posted']

    driver = webdriver.Chrome(options = options, executable_path = DRIVER_PATH)
    driver.get(all_listings[0])

    for listing in all_listings[:]:

        try:
            driver.get(listing)
            driver.implicitly_wait(1)
            posting = driver.find_element_by_xpath('//*[@id="display-date"]/time')
            post_time.append(posting.text)
        except:
            post_time.append('None')
    driver.quit()

    return post_time


# I only want the listing where there is a price and a squarfootage of the place listed.
def combined_info(all_listings, all_prices, all_sqrt, lxury_list, house_list):

    listing_final = []
    price_final = []
    sqrt_final = []
    for key, val in enumerate(all_listings):
        if all_prices[key] != 'None' and all_sqrt[key] != 'None' and val not in listing_final and lxury_list[key] == 1:
            listing_final.append(val)
            price = str(all_prices[key])
            
            price.replace('$','').replace(',','')
            price_final.append(price)
            
            sqrt_final.append((all_sqrt[key]))
        else:
            pass

    return listing_final, price_final, sqrt_final



#all_listings, all_prices = craigslist_findings('Belmont CA', 'appartment', '1', '1', 'parking')
#all_sqrt = grab_sqft(all_listings)

#listing_f, price_f, sqrt_f = combined_info(all_listings, all_prices, all_sqrt)

#posted = posted(listing_f)


