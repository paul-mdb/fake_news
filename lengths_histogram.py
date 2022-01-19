import os
import matplotlib.pyplot as plt
import numpy as np
from transformers import CamembertModel, CamembertTokenizer, FlaubertModel, FlaubertTokenizer




PATH = 'text_articles/'
camembert_tokenizer = CamembertTokenizer.from_pretrained("camembert-base")
flaubert_tokenizer = flaubert_tokenizer = FlaubertTokenizer.from_pretrained('flaubert/flaubert_base_cased')

def char_lengths():
    lengths = []
    for count, filename in enumerate(os.listdir(PATH)):
        with open(os.path.join(PATH, filename), 'r') as file:
            if filename.startswith('.'):
                continue
            text = file.read()
            lengths.append(len(text))

    fig, ax = plt.subplots(1)
    fig.suptitle('lengths distribution (characters)', fontsize = 16)
    ax.hist(lengths, bins = np.arange(0, 20000, 100))
    plt.show()


def flaubert_token_lengths():
    lengths = []
    for count, filename in enumerate(os.listdir(PATH)):
        with open(os.path.join(PATH, filename), 'r') as file:
            if filename.startswith('.'):
                continue
            text = file.read()
            tokens = flaubert_tokenizer.encode(text)
            lengths.append(len(tokens))

    fig, ax = plt.subplots(1)
    fig.suptitle('lengths distribution (flaubert)', fontsize = 16)
    ax.hist(lengths, bins = np.arange(0, 20000, 100))
    plt.show()

def camembert_token_lengths():
    lengths = []
    for count, filename in enumerate(os.listdir(PATH)):
        with open(os.path.join(PATH, filename), 'r') as file:
            if filename.startswith('.'):
                continue
            text = file.read()
            tokens = camembert_tokenizer.encode(text)
            lengths.append(len(tokens))

    fig, ax = plt.subplots(1)
    fig.suptitle('lengths distribution (camembert)', fontsize = 16)
    ax.hist(lengths, bins = np.arange(0, 20000, 100))
    plt.show()


def main():
    char_lengths()


if __name__ == '__main__':
    main()