import os, json
import matplotlib.pyplot as plt
import numpy as np
from transformers import CamembertModel, CamembertTokenizer, FlaubertModel, FlaubertTokenizer




PATH = 'text_articles/'
camembert_tokenizer = CamembertTokenizer.from_pretrained("camembert-base")
flaubert_tokenizer = flaubert_tokenizer = FlaubertTokenizer.from_pretrained('flaubert/flaubert_base_cased')

def char_lengths(PATH, label):
    lengths = []
    for count, filename in enumerate(os.listdir(PATH)):
        with open(os.path.join(PATH, filename), 'r') as file:
            if filename.startswith('.'):
                continue
            paragraphs = json.loads(file.read())["content"]
            for text in paragraphs :
                lengths.append(len(text))

    fig, ax = plt.subplots(1)
    fig.suptitle('Paragraphs lengths (characters), label : ' + label, fontsize = 16)
    ax.hist(lengths, bins = np.arange(0, 20000, 100))
    plt.show()


def flaubert_token_lengths(PATH, label):
    lengths = []
    for count, filename in enumerate(os.listdir(PATH)):
        with open(os.path.join(PATH, filename), 'r') as file:
            if filename.startswith('.'):
                continue
            paragraphs = json.loads(file.read())["content"]
            for text in paragraphs :
                tokens = flaubert_tokenizer.encode(text)
                lengths.append(len(tokens))

    fig, ax = plt.subplots(1)
    fig.suptitle('Paragraphs lengths (flaubert), label : ' + label, fontsize = 16)
    ax.hist(lengths, bins = np.arange(0, 20000, 100))
    plt.show()

def camembert_token_lengths(PATH, label):
    lengths = []
    for count, filename in enumerate(os.listdir(PATH)):
        with open(os.path.join(PATH, filename), 'r') as file:
            if filename.startswith('.'):
                continue
            paragraphs = json.loads(file.read())["content"]
            for text in paragraphs:
                tokens = camembert_tokenizer.encode(text)
                lengths.append(len(tokens))

    fig, ax = plt.subplots(1)
    fig.suptitle('Paragraphs lengths (camembert), label : ' + label, fontsize = 16)
    ax.hist(lengths, bins = np.arange(0, 20000, 100))
    plt.show()




if __name__ == '__main__':
    true_path = 'json-annotations/TRUE'
    fake_path = 'json-annotations/FAKE'
    biased_path = 'json-annotation/BIASED'
    char_lengths(true_path, 'TRUE' )
    flaubert_token_lengths(true_path, 'TRUE')
    camembert_token_lengths(true_path, 'TRUE')
    char_lengths(biased_path, 'BIASED' )
    flaubert_token_lengths(biased_path, 'BIASED')
    camembert_token_lengths(biased_path, 'BIASED')
    char_lengths(fake_path, 'FAKE' )
    flaubert_token_lengths(fake_path, 'FAKE')
    camembert_token_lengths(fake_path, 'FAKE')