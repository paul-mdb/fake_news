from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import pickle
import re
import time



a_file = open("match_dictionary.pkl", "rb")
dict = pickle.load(a_file)

initial_link = 'https://tagtog.net/LouisDlms/fake_news/pool/aA8lkPVtaD6ZB.r0WxkVKpGmiLau-389.txt?p=10&i=0'

def  tagtog_login(driver, username, password):
    driver.get('https://www.tagtog.net/-login')
    driver.find_element_by_css_selector('#loginid').send_keys(username)
    driver.find_element_by_css_selector('#password').send_keys(password)
    driver.find_element_by_css_selector('body > div.container.fitbig > div.login-panel.col-xs-offset-4.col-xs-4 > form > div > div > div.row > div > button > strong').click()




true_websites = ['L\'Express', 'Jean_Marc_Jancovici', 'Ouest_France', 'Futura_Planet', 'Carbone_4', 'Euronews']
biased_websites = ['GreenPeace']
fake_websites = ['Egalité_&_Réconciliation', 'Réseau_Voltaire', 'Réseau_International', 'Association_des_climatorealistes', 'Contrepoints', 'Les_moutons_enragés', 'Arrêt_Sur_Info', 'Wikistrike']


# bool(re.match(prefix, text, re.I))


def go_to_link(driver, page_number):
    repo_button_selector = 'span.bold:nth-child(3)'
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,repo_button_selector))).click()
    next_selector = '.glyphicon-chevron-right'
    for i in range(page_number):
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,next_selector))).click()
    first_article_selector = '#search-results > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(4) > a:nth-child(1)'
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,first_article_selector))).click()






def main(driver, number_of_steps, page_number):
    go_to_link(driver, page_number)
    for i in range(number_of_steps):
        title_selector = '.filename'
        next_selector = '#docnavigator > a.btn.btn-next.btn-default'
        # article_id = driver.find_element_by_css_selector(title_selector).text[:-4]
        article_id = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, title_selector))).text[:-4]
        source = dict[int(article_id)]
        label = None
        for prefix in true_websites :
            if bool(re.match(prefix, source,  re.I)):
                label = 1
        for prefix in fake_websites :
            if bool(re.match(prefix, source,  re.I)):
                label = 0
        for prefix in  biased_websites :
            if bool(re.match(prefix, source,  re.I)):
                label = 2

        if label is not None :
            click_button_selector =  '#sidebar-doc-label-list > fieldset > div > div:nth-child(2) > div.dropdown.bootstrap-select.metalabel_select.form-control.bs3 > button > div > div > div'
            save_selector = '#save-doc > span.glyphicon.glyphicon-edit'
            fake_selector = '#bs-select-1-1'
            biased_selector = '#bs-select-1-2'
            true_selector = '#bs-select-1-3'

            selectors = [fake_selector, true_selector, biased_selector]
            selector = selectors[label]


            try :

                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,click_button_selector))).click()
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,selector))).click()
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,save_selector))).click()
                time.sleep(1.5)

            except :
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,next_selector))).click()
                continue
                
        
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,next_selector))).click()

    driver.quit()





if __name__ == '__main__':
    driver = webdriver.Firefox()
    tagtog_login(driver, 'Paul-2', 'dumb_password')
    main(driver, 50, 9)

"""driver = webdriver.Firefox()
tagtog_login(driver, 'Paul-2', 'dumb_password')
go_to_link(driver, 7)
time.sleep(3)
driver.quit()"""

