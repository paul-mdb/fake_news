from annotations import get_annotations
from tagtog import get_text_from_id

from spacy.training import offsets_to_biluo_tags
import spacy
import pandas as pd

def get_entities_from_id(article_id: int) -> dict:
    annotations = get_annotations(article_id)["annotations"]
    entities = []
    for ann in annotations:
        entity = [ann["start"], ann["start"] + len(ann["text"]), str(ann["label"])]
        entities.append(entity)
    return entities

def remove_useless_entities(content, entities):
    n_entities = len(entities)
    new_entities = []
    for idx, entity in enumerate(entities):
        # Remove useless entities (id 0)
        if entity[2] == "0":
            start, end = entity[:2]
            length = end - start
            # From content
            content = content[:start] + content[end:] 
            # From entities
            for i in range(idx, n_entities):
                entities[i][0] -= length
                entities[i][1] -= length
        else:
            new_entities.append((entity[0], entity[1], entity[2]))

    return content, new_entities

def get_content_entities_from_id(article_id):
    content = get_text_from_id(article_id)
    entities = get_entities_from_id(article_id)

    content, entities = remove_useless_entities(content, entities)

    return content, entities

def get_biluo(content, entities):
    doc = nlp(content)
    tags = offsets_to_biluo_tags(doc, entities)
    return tags


# if __name__ == "__main__":
#     article_id = 3096

#     nlp = spacy.load("fr_core_news_md")

#     content, new_entities = get_content_entities_from_id(article_id)
#     biluo = get_biluo(content, new_entities)

#     print(biluo)

if __name__ == "__main__":
    nlp = spacy.load("fr_core_news_md")

    dataset = []

    for article_id in range(2):
        content, new_entities = get_content_entities_from_id(article_id)
        biluo = get_biluo(content, new_entities)
        dataset.append([content, ','.join(biluo)])

    df = pd.DataFrame(dataset, columns=["text", "word_labels"])
    df.to_csv("word_labels_per_text.csv")