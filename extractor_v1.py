from selenium import webdriver
from json import dumps
from pandas import isna

from website_list import WEBSITE_LIST, INITIAL_WEBSITE_LIST
from utils import DATABASE_PATH, SPECIAL_CHARACTERS, format_article_into_json, skip_cookie_popup, get_links, get_text_in_selected_element, get_date

THRESHOLD_ON_CONTENT_LENGTH = 50

driver = webdriver.Firefox()
# driver.maximize_window()

for (label, url, cookie_selector, link_selector, content_selector, title_selector, date_selector, author_selector) in INITIAL_WEBSITE_LIST:
    # Replace by default values if empty string
    cookie_selector = "x" if isna(cookie_selector) else cookie_selector
    link_selector = "article a" if isna(link_selector) else link_selector
    content_selector = "article" if isna(content_selector) else content_selector
    title_selector = "h1" if isna(title_selector) else title_selector
    date_selector = "x" if isna(date_selector) else date_selector
    author_selector = "x" if isna(author_selector) else author_selector

    # DEBUG : SKIP WEBSITES WITH ISSUES
    if label  == "Paris innovation review"  :
        continue

    # Go to the URL
    driver.get(url)

    # Skip cookie pop-up
    skip_cookie_popup(driver, cookie_selector)

    # Find all the article links on the page
    links = get_links(driver, link_selector)

    # DEBUG : 1 ARTICLE / WEBSITE
    links = [links[0]]

    #  Extract all articles  for the website
    for link in links:
        driver.get(link)
        
        try :
            content = get_text_in_selected_element(driver, content_selector)

            if len(content) <= THRESHOLD_ON_CONTENT_LENGTH:
                print(f"{link} : content too short")
                continue

            title = get_text_in_selected_element(driver, title_selector)
            author = get_text_in_selected_element(driver, author_selector)
            date = get_date(driver, date_selector)

            # Export article
            filename = label + "-" + title[:15]
            filename.replace(" ", '_')
            for character in SPECIAL_CHARACTERS:
                filename.replace(character, '_')
            filename += ".json"

            file = open(DATABASE_PATH + filename, "w")
            file.write(dumps(format_article_into_json(
                title=title,
                author=author,
                date=date,
                content=content
            )))
            file.close()

        except :
            print(f"{label} : extraction failed")
            continue

driver.quit()
# print(f"{number_of_articles} articles")
