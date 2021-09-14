from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from json import dumps

from website_list import WEBSITE_LIST, INITIAL_WEBSITE_LIST
from utils import format_article_into_json, DATABASE_PATH

content_list = []

driver = webdriver.Firefox()
driver.maximize_window()

for website in INITIAL_WEBSITE_LIST:

    label = website[0]
    url = website[1]

    driver.get(url)

    # Skip cookie pop-up
    if label == "Ouest France" or label == "Les Echos (Planete)" or  label == "Euronews":
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID,"didomi-notice-agree-button"))).click()
    elif  label == "L'Express":
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID,"popin_tc_privacy_button_3"))).click()



    link_elements = driver.find_elements_by_css_selector("article a")
    links = []
    for link_element in link_elements:
        links += [
            link_element.get_attribute("href")
        ]

    # TMP : 1 article / website to debug
    print(label, links)
    links = [links[0]]

    for link in links:
        driver.get(link)
        try :
                
            title = driver.find_element_by_css_selector("h1").text
            article = driver.find_element_by_css_selector("article")
            content = article.text


            # Export article
            filename = (label + "-" + title[:15]).replace(" ", "_") + ".json"
            file = open(DATABASE_PATH + filename, "w")
            file.write(dumps(format_article_into_json(
                title=title,
                author="",
                date="",
                content=content
            )))
            file.close()

        except :
            continue

driver.quit()
