from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

driver = webdriver.Safari()

driver.get("https://www.ouest-france.fr/environnement/rechauffement-climatique/")
driver.maximize_window()

try : 
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,"//button[@id='didomi-notice-agree-button']"))).click()
except : 
    print("failed here")
    driver.quit()

articles = driver.find_elements_by_tag_name("article")

print("hey")
time.sleep(3)
#driver.quit()