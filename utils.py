from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

DATABASE_PATH = "articles/"
SPECIAL_CHARACTERS = [
    '/', '<', '>', ':', '"', '\\', '|', '?', '*'
]

# General functions
def format_article_into_json(title, author, date, content):
    return {
        "title": title,
        "author": author,
        "date": date,
        "content": content
    }

# Extraction functions
def skip_cookie_popup(driver, selector):
    if selector != "x":
        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,selector))).click()
        except:
            return

def get_links(driver, css_selector):
    link_elements = driver.find_elements_by_css_selector(css_selector)
    links = []
    for link_element in link_elements:
        link = link_element.get_attribute("href")
        if link not in links : # remove duplicates
            links += [link]
    return links

def get_text_in_selected_element(driver, selector):
    if selector == "x":
        return ""

    try:
        return driver.find_element_by_css_selector(selector).text
    except:
        return ""

def get_date(driver, selector):
    try:
        element = driver.find_element_by_css_selector(selector)
        datetime = element.get_attribute("datetime")
        if datetime is not None:
            return datetime
        return get_text_in_selected_element(driver, selector)
    except:
        return ""