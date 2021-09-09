from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from json import dumps

from website_list import WEBSITE_LIST
from utils import format_article_into_json, DATABASE_PATH

content_list = []

driver = webdriver.Firefox()
driver.maximize_window()

for (label, url) in WEBSITE_LIST:
    driver.get(url)

    # Skip cookie pop-up
    if label == "Ouest France":
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID,"didomi-notice-agree-button"))).click()

    link_elements = driver.find_elements_by_css_selector("article a")
    links = []
    for link_element in link_elements:
        links += [
            link_element.get_attribute("href")
        ]

    # TMP : 1 article / website to debug
    links = [links[0]]

    for link in links:
        driver.get(link)

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

driver.quit()
