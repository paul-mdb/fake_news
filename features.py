# %% [markdown]
# # Features - Fake news detection

# %%
import spacy
import os
import json
import numpy as np

from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from spacy_readability import Readability
from spacy.language import Language

nlp = spacy.load("fr_dep_news_trf")

def get_readability(nlp, name):
    read = Readability()
    return read

Language.factory("my_readability", func=get_readability)
nlp.add_pipe("my_readability", last=True)

# %% [markdown]
# ## Dataset

# %%
def remove_useless(paragraph_ann):
    content = paragraph_ann["content"]
    paragraphs_to_delete = []
    entities_to_delete = []

    for index, paragraph in enumerate(content) :
        if 'label' in paragraph.keys() and paragraph["label"]==0:
            paragraphs_to_delete.append(index)

        else :
            if type(paragraph["content"])==list:
              for index_entity, entity_content in enumerate(paragraph["content"]):
                if type(entity_content) == dict and 'label' in entity_content.keys() and entity_content["label"]==0:
                      entities_to_delete.append((index, index_entity))

    for i in range(-1, -len(entities_to_delete)-1, -1) :
      index, index_entity = entities_to_delete[i]
      del paragraph_ann['content'][index]['content'][index_entity]

    for index in reversed(paragraphs_to_delete):
      del paragraph_ann['content'][index]

    return paragraph_ann


def fusion(paragraph_ann):
  label = paragraph_ann['label']
  author = paragraph_ann['author']
  title = paragraph_ann['title']
  date = paragraph_ann['date']
  content = ""
  for paragraph in paragraph_ann['content']:
    if type(paragraph['content']) == str :
      content += paragraph['content']
    elif type(paragraph['content']) == list :
      for entity in paragraph['content']:
        content += entity['content']
  json = {
    'label' : label, 
    'date': date,
    'title': title,
    'author': author,
    'content' : content,
  }
  return json

# %%
# assign directory
ANNOTATIONS_FOLDER = 'C:\\Users\\louis\\Desktop\\NLP\\fake_news\\annotations'
dataset = []
 
# iterate over files in
# that directory
for filename in os.listdir(ANNOTATIONS_FOLDER):
    f = os.path.join(ANNOTATIONS_FOLDER, filename)
    # checking if it is a file
    if os.path.isfile(f):
        with open(f, 'r') as file:
            data = json.load(file)
            if data["label"] > 0:
                data = fusion(remove_useless(data))
                dataset += [(data["label"], data["content"])]

dataset = np.array(dataset, dtype=str)

print(f'Dataset: {dataset.shape}')

# %%
train, test = train_test_split(dataset)
y_train, x_train_txt = np.array(train[:,0], dtype=int), [str(txt) for txt in train[:,1]]
y_test, x_test_txt = np.array(test[:, 0], dtype=int), [str(txt) for txt in test[:,1]]

print(f'Train: {len(x_train_txt)} ({type(x_train_txt[0])})')
print(f'Test: {len(x_test_txt)}')

# %%
x_train_doc = list(nlp.pipe(x_train_txt))
x_test_doc = list(nlp.pipe(x_test_txt))

# %% [markdown]
# ## Features

# %% [markdown]
# ### Functions

# %%
def get_punct_ratio(doc) -> float:
    n_token = len(doc)
    if n_token:
        return sum([1 if token.pos_ == "PUNCT" else 0 for token in doc]) / n_token
    else:
        return .0

def get_adv_ratio(doc) -> float:
    n_token = len(doc)
    if n_token:
        return sum([1 if token.pos_ == "ADV" else 0 for token in doc]) / n_token
    else:
        return .0

def get_fin_ratio(doc) -> float:
    n_token = len(doc)
    if n_token:
        return sum([1 if "Fin" in token.morph.get("VerbForm") else 0 for token in doc]) / n_token
    else:
        return .0   

def get_fkre(doc) -> float:
    return doc._.flesch_kincaid_reading_ease

def get_length(doc) -> float:
    return len(doc)

def get_expr(doc) -> float:
    return sum([1 if token.lemma_ in ['?', '!', '(', ')'] else 0 for token in doc])

# %%
FEATURES = {
    "PUNCT": get_punct_ratio,
    "ADV": get_adv_ratio,
    "FIN": get_fin_ratio,
    "FKRE": get_fkre,
    "LENGTH": get_length,
    "EXPR": get_expr,
}

features_train = np.zeros((len(x_train_txt), len(FEATURES)), dtype=float)
features_test = np.zeros((len(x_test_txt), len(FEATURES)), dtype=float)

# %% [markdown]
# ### Computation

# %%
for doc_idx, doc in enumerate(x_train_doc):
    print(doc_idx / len(x_train_doc))
    for feature_idx, feature in enumerate(FEATURES.keys()):
        get_feature = FEATURES[feature]
        features_train[doc_idx, feature_idx] = get_feature(doc)

# %%
for doc_idx, doc in enumerate(x_test_doc):
    print(doc_idx / len(x_train_doc))
    for feature_idx, feature in enumerate(FEATURES.keys()):
        get_feature = FEATURES[feature]
        features_test[doc_idx, feature_idx] = get_feature(doc)

# %%
classifier = SVC()
classifier.fit(features_train, y_train)
y_predicted = np.array(classifier.transform(features_test), dtype=int)

# %% [markdown]
# ## Scores

# %%
def true_positives(predicted_labels, labels):
    return np.count_nonzero(labels[predicted_labels == 1])

def false_positives(predicted_labels, labels):
    return np.count_nonzero(1 - labels[predicted_labels == 1])

def true_negatives(predicted_labels, labels):
    return np.count_nonzero(1 - labels[predicted_labels == 0])

def false_negatives(predicted_labels, labels):
    return np.count_nonzero(labels[predicted_labels == 0])

class Scores:
    def __init__(self, predicted_labels, labels):
        self.predicted_labels = predicted_labels
        self.labels = labels

        self.tp = true_positives(self.predicted_labels, self.labels)
        self.fp = false_positives(self.predicted_labels, self.labels)
        self.tn = true_negatives(self.predicted_labels, self.labels)
        self.fn = false_negatives(self.predicted_labels, self.labels)

    def __repr__(self):
        print("===================\n")

        print(f"TP : { self.tp }")
        print(f"FP : { self.fp }")
        print(f"TN : { self.tn }")
        print(f"FN : { self.fn }\n")

        print("===================\n")

        print(f"P : { self.positives() }")
        print(f"N : { self.negatives() }")
        print(f"TPR : { self.tp_rate() }")
        print(f"TNR : { self.tn_rate() }")
        print(f"FPR : { self.fp_rate() }")
        print(f"ACC : { self.acc() }")
        print(f"Precision : { self.precision() }")
        print(f"NPV : { self.npv() }")
        print(f"MCC : { self.mcc() }")
        print(f"F1-score : { self.f_score(1) }")
        print(f"Kappa : { self.kappa() } \n")

        print("===================")

        return ""

    def positives(self):
        return self.tp + self.fn

    def negatives(self):
        return self.fp + self.tn

    def tp_rate(self):
        positives = self.positives()
        if positives > 0:
            return self.tp / positives
        else:
            return 0
    
    def tn_rate(self):
        negatives = self.negatives()
        if negatives > 0:
            return self.tn / negatives
        else:
            return 0

    def fp_rate(self):
        negatives = self.negatives()
        if negatives > 0:
            return self.fp / negatives
        else:
            return None

    def acc(self):
        return (self.tp + self.tn) / (self.negatives() + self.positives())

    def precision(self):
        den = self.tp + self.fp
        if den > 0:
            return self.tp / den
        else:
            return None

    def npv(self):
        den = self.tn + self.fn
        if den > 0:
            return self.tn / den
        else:
            return None

    def mcc(self):
        den = ((self.tp + self.fp)*(self.tp + self.fn)*(self.tn + self.fp)*(self.tn + self.fn)) ** 0.5
        if den != 0:
            return (self.tp * self.tn - self.fp * self.fn) / den
        else:
            return None

    def f_score(self, beta):
        precision = self.precision()
        tpr = self.tp_rate()

        if precision is None or tpr is None:
            return None
        return (1 + beta ** 2) * (self.precision() * self.tp_rate()) / ((beta ** 2) * self.precision() + self.tp_rate())

    def kappa(self):
        den = (self.tp + self.fp) * (self.fp + self.tn) + (self.tp + self.fn)*(self.fn + self.tn)
        if den != 0:
            return 2 * (self.tp * self.tn - self.fn * self.fp) / den
        else:
            return None

# %%
scores = Scores(y_predicted, y_test)
print(scores)


