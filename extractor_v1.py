from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

content_list = []
website_list = []

driver = webdriver.Safari()

driver.get("https://www.ouest-france.fr/environnement/rechauffement-climatique/")
driver.maximize_window()
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID,"didomi-notice-agree-button"))).click()
time.sleep(3)

articles = driver.find_elements_by_tag_name("article")

for article in articles:
    link = article.find_element_by_xpath('a').get_attribute('href').click() # or click ?
    # driver.get(link)
    driver.implicitly_wait(5)
    # Find data and add to content_list
    driver.back()
    driver.implicitly_wait(3)

driver.quit()