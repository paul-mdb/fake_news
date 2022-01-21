from remove_useless import remove_useless, fusion
from paragraph_ann import generate_paragraphs_ann
from selenium import webdriver
import pandas as pd

def get_text_dataset(n) :
    driver = webdriver.Firefox()
    articles = []
    labels = []
    for article_id in range(n):
        try :
            paragraphs_ann = generate_paragraphs_ann(driver, article_id)
            print(paragraphs_ann)
            data = fusion(remove_useless(paragraphs_ann))
            articles.append(data['content'])
            labels.append(data['label'])

        except :
            print(f'error with article no {article_id}')
    
    dataset = pd.DataFrame(list(zip(articles, labels)),
               columns =['article', 'label'])
    driver.quit()
    return dataset
    
df = get_text_dataset(10)
print(df.head())
