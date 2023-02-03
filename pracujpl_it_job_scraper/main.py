from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, NoSuchWindowException
from pprint import pprint
import time
import json


driver = webdriver.Chrome()
offers_list = []
path = f"https://it.pracuj.pl/?pn=1"
driver.get(path)

#setup
time.sleep(2)
accept_button_selector = "#gp-cookie-agreements > div > div > div.g1kqzctt > div.bafq4sb > button"
driver.find_element(By.CSS_SELECTOR, value=accept_button_selector).click()
time.sleep(2)

#checking number of offers
num_of_offers = int((driver.find_element(By.CSS_SELECTOR, ".MainTitlestyles__Wrapper-sc-crpnw3-0 > span:nth-child(1)").text).strip("()"))
offers_on_page = 20

pg_num = 1
while pg_num <= num_of_offers // offers_on_page:

    path = f"https://it.pracuj.pl/?pn={pg_num}"
    driver.get(path)
    time.sleep(1)

    #find offers
    offers = driver.find_elements(By.CSS_SELECTOR, ".kWskaM")

    #looping through offers
    for offer in offers:
            # offers_left = False

        offer_dict = {}
        
        #find offer names
        name = offer.find_element(By.TAG_NAME, "h3")
        offer_dict["Offer Name"] = name.text
            
        #find company
        company = offer.find_element(By.CSS_SELECTOR, ".fUIqOA")
        offer_dict["Company"] = company.text

        #find locations
        locations = offer.find_elements(By.CSS_SELECTOR, ".fSgqsj")
        for location in locations:
            #looping causes that actually the last element is added to location key which is <city name> or <remote work>
            offer_dict["Location"] = location.text 

        #find contract type
        contract_type = offer.find_element(By.CSS_SELECTOR, ".bKlAEw")
        offer_dict["Contract Type"] = contract_type.text

        #find job level
        job_level = offer.find_elements(By.CSS_SELECTOR, ".drHfhW")
        for job in job_level:
            #similar to location, only actual job level is added to dictionary instead of earnings (which are optional)
            offer_dict["Job Level"] = job.text

        #find tags
        tags = offer.find_elements(By.CSS_SELECTOR, ".dDTkNx")
        tags_list = []
        for tag in tags:
            tags_list.append(tag.text)
            offer_dict["Tags"] = tags_list

        #date of publication
        date = offer.find_element(By.CLASS_NAME, "JobOfferstyles__FooterText-sc-1rq6ue2-22")
        offer_dict["Date"] = date.text
        offers_list.append(offer_dict)

            
    pg_num += 1


with open("pracujpl_it_job_scraper/offers.json", "w") as file:
    data = json.dumps(offers_list)
    file.write(data)




driver.quit()

