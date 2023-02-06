# Importing modules
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, NoSuchWindowException
from pprint import pprint
import time
import json

# Initializing selenium with Chrome 
driver = webdriver.Chrome()

# Getting pracuj.pl page
path = f"https://it.pracuj.pl/?pn=1"
driver.get(path)

# Creating offers list
offers_list = []

# Setup
time.sleep(2)
accept_button_selector = "#gp-cookie-agreements > div > div > div.g1kqzctt > div.bafq4sb > button"
driver.find_element(By.CSS_SELECTOR, value=accept_button_selector).click()
time.sleep(2)

# Checking number of offers
num_of_offers = int((driver.find_element(By.CSS_SELECTOR, ".MainTitlestyles__Wrapper-sc-crpnw3-0 > span:nth-child(1)").text).strip("()"))
offers_on_page = 20

# Page number count
pg_num = 1
while pg_num <= num_of_offers // offers_on_page:

    # Getting number of page with offers
    path = f"https://it.pracuj.pl/?pn={pg_num}"
    driver.get(path)
    time.sleep(1)

    # Finding offers
    offers = driver.find_elements(By.CSS_SELECTOR, ".kWskaM")

    # Looping through offers
    for offer in offers:

        # Creating dict with offers that cleans every time new offer is searched through
        offer_dict = {}
        
        # Finding offer names
        name = offer.find_element(By.TAG_NAME, "h3")
        offer_dict["Offer Name"] = name.text
            
        # Finding company
        company = offer.find_element(By.CSS_SELECTOR, ".fUIqOA")
        offer_dict["Company"] = company.text

        # Finding locations
        locations = offer.find_elements(By.CSS_SELECTOR, ".fSgqsj")
        for location in locations:
            # Looping causes that actually the last element is added to location key which is <city name> or <remote work>
            offer_dict["Location"] = location.text 

        # Finding contract type
        contract_type = offer.find_element(By.CSS_SELECTOR, ".bKlAEw")
        offer_dict["Contract Type"] = contract_type.text

        # Finding job level
        job_level = offer.find_elements(By.CSS_SELECTOR, ".drHfhW")
        for job in job_level:
            # Similar to location, only actual job level is added to dictionary instead of earnings (which are optional)
            offer_dict["Job Level"] = job.text

        # Finding tags
        tags = offer.find_elements(By.CSS_SELECTOR, ".dDTkNx")
        tags_list = []
        for tag in tags:
            tags_list.append(tag.text)
            offer_dict["Tags"] = tags_list

        # Date of publication
        date = offer.find_element(By.CLASS_NAME, "JobOfferstyles__FooterText-sc-1rq6ue2-22")
        offer_dict["Date"] = date.text
        offers_list.append(offer_dict)

    # Incrementing page number after gathering all the data on page   
    pg_num += 1

# Saving scraped data to .json file
with open("pracujpl_it_job_scraper/offers.json", "w") as file:
    data = json.dumps(offers_list)
    file.write(data)




driver.quit()

