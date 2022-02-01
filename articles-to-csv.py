from ntpath import join
import os
from cv2 import add
import pandas as pd
import json

true_path = 'txt-labelled-articles/TRUE/'
biased_path = 'txt-labelled-articles/BIASED/'
fake_path = 'txt-labelled-articles/FAKE/'

def add_to_lists(path):
    articles = []
    labels = []
    for _, filename in enumerate(os.listdir(path)):
        with open(os.path.join(path, filename), 'r') as file:
            json_file = json.load(file)
            label = json_file['label']
            article = json_file['content']
            articles.append(article)
            labels.append(label)
    return article, labels
        

if __name__== '__main__':

    true_articles, true_labels = add_to_lists(true_path)
    biased_articles, biased_labels = add_to_lists(biased_path)
    fake_articles, fake_labels = add_to_lists(fake_path)

    articles = true_articles + biased_articles + fake_articles
    labels = true_labels + biased_labels + fake_labels

    df = pd.DataFrame(zip(articles, labels), columns=['label', 'article'])
    df.to_csv('text_dataset.csv')
    print(df.head())


