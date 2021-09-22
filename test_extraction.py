from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import  time

from website_list import WEBSITE_LIST, INITIAL_WEBSITE_LIST

url = "https://www.lexpress.fr/actualite/societe/environnement/la-crise-des-sous-marins-australiens-met-elle-en-peril-les-negociations-de-la-cop26_2158787.html"

driver = webdriver.Firefox()
driver.maximize_window()

driver.get(url)
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID,"popin_tc_privacy_button_3"))).click()

content = driver.find_element_by_css_selector("article").text
title = driver.find_element_by_css_selector("h1").text

print(f"content  : {content}")
print(f"title : {title}")

time.sleep(3)
driver.quit()