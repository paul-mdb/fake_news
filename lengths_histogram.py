import os, json
import matplotlib.pyplot as plt
import numpy as np
from transformers import CamembertModel, CamembertTokenizer, FlaubertModel, FlaubertTokenizer




camembert_tokenizer = CamembertTokenizer.from_pretrained("camembert-base")
flaubert_tokenizer = flaubert_tokenizer = FlaubertTokenizer.from_pretrained('flaubert/flaubert_base_cased')

<<<<<<< HEAD
def char_lengths(PATH):
=======
def char_lengths(PATH, label):
>>>>>>> fbdc462e4eee0840809dbda8be9f57975a46267b
    lengths = []
    for count, filename in enumerate(os.listdir(PATH)):
        with open(os.path.join(PATH, filename), 'r') as file:
            if filename.startswith('.'):
                continue
<<<<<<< HEAD
            paragraphs = json.load(file)["content"]
            for paragraph in paragraphs :
                text = ''
                for entity in paragraph["content"] :
                    if type(entity)==str :
                        text += entity
                    else :
                        text += entity["content"]
                lengths.append(len(text))
    return np.array(lengths)



def flaubert_token_lengths(PATH):
=======
            paragraphs = json.loads(file.read())["content"]
            for text in paragraphs :
                lengths.append(len(text))

    fig, ax = plt.subplots(1)
    fig.suptitle('Paragraphs lengths (characters), label : ' + label, fontsize = 16)
    ax.hist(lengths, bins = np.arange(0, 20000, 100))
    plt.show()


def flaubert_token_lengths(PATH, label):
>>>>>>> fbdc462e4eee0840809dbda8be9f57975a46267b
    lengths = []
    for count, filename in enumerate(os.listdir(PATH)):
        with open(os.path.join(PATH, filename), 'r') as file:
            if filename.startswith('.'):
                continue
<<<<<<< HEAD
            paragraphs = json.load(file)["content"]
            for paragraph in paragraphs :
                text = ''
                for entity in paragraph["content"] :
                    if type(entity)==str :
                        text += entity
                    else :
                        text += entity["content"]
                tokens = flaubert_tokenizer.encode(text, truncation=True, max_length = 512)
                lengths.append(len(tokens))
    return np.array(lengths)

def camembert_token_lengths(PATH):
=======
            paragraphs = json.loads(file.read())["content"]
            for text in paragraphs :
                tokens = flaubert_tokenizer.encode(text)
                lengths.append(len(tokens))

    fig, ax = plt.subplots(1)
    fig.suptitle('Paragraphs lengths (flaubert), label : ' + label, fontsize = 16)
    ax.hist(lengths, bins = np.arange(0, 20000, 100))
    plt.show()

def camembert_token_lengths(PATH, label):
>>>>>>> fbdc462e4eee0840809dbda8be9f57975a46267b
    lengths = []
    for count, filename in enumerate(os.listdir(PATH)):
        with open(os.path.join(PATH, filename), 'r') as file:
            if filename.startswith('.'):
                continue
<<<<<<< HEAD
            paragraphs = json.load(file)["content"]
            for paragraph in paragraphs :
                text = ''
                for entity in paragraph["content"] :
                    if type(entity)==str :
                        text += entity
                    else :
                        text += entity["content"]
                tokens = camembert_tokenizer.encode(text, truncation=True, max_length = 512)
                lengths.append(len(tokens))
    return np.array(lengths)
=======
            paragraphs = json.loads(file.read())["content"]
            for text in paragraphs:
                tokens = camembert_tokenizer.encode(text)
                lengths.append(len(tokens))

    fig, ax = plt.subplots(1)
    fig.suptitle('Paragraphs lengths (camembert), label : ' + label, fontsize = 16)
    ax.hist(lengths, bins = np.arange(0, 20000, 100))
    plt.show()

>>>>>>> fbdc462e4eee0840809dbda8be9f57975a46267b



if __name__ == '__main__':
<<<<<<< HEAD
    fig, axs = plt.subplots(3, 2)
    true_path = 'json-annotations/TRUE/'
    fake_path = 'json-annotations/FAKE/'
    biased_path = 'json-annotations/BIASED/'
    true_char_lengths=char_lengths(true_path)
    true_flau_lengths=flaubert_token_lengths(true_path)
    true_cam_lengths=camembert_token_lengths(true_path)
    biased_char_lengths=char_lengths(biased_path)
    biased_flau_lengths=flaubert_token_lengths(biased_path)
    biased_cam_lengths=camembert_token_lengths(biased_path)
    fake_char_lengths=char_lengths(fake_path)
    fake_flau_lengths=flaubert_token_lengths(fake_path)
    fake_cam_lengths=camembert_token_lengths(fake_path)
    axs[0, 0].hist(true_char_lengths, bins = np.arange(5, 1300, 10), color = 'green')
    axs[0, 0].set_title('Number of characters')
    axs[0, 0].set(ylabel='TRUE')
    axs[0, 0].axvline(true_char_lengths.mean(), color='k', linestyle='dashed', linewidth=1)
    axs[0, 1].hist(true_cam_lengths, bins = np.arange(5, 550), color = 'green')
    axs[0, 1].set_title('Number of camembert tokens')
    axs[0, 1].axvline(true_cam_lengths.mean(), color='k', linestyle='dashed', linewidth=1)
    axs[1, 0].hist(biased_char_lengths, bins = np.arange(5, 1300, 10), color = 'pink')
    axs[1, 0].set(ylabel='BIASED')
    axs[1, 0].axvline(biased_char_lengths.mean(), color='k', linestyle='dashed', linewidth=1)
    axs[1, 1].hist(biased_cam_lengths, bins = np.arange(5, 550), color = 'pink')
    axs[1, 1].axvline(biased_cam_lengths.mean(), color='k', linestyle='dashed', linewidth=1)
    axs[2, 0].hist(fake_char_lengths, bins = np.arange(5, 1300, 10), color = 'red')
    axs[2, 0].set(ylabel='FAKE')
    axs[2, 0].axvline(fake_char_lengths.mean(), color='k', linestyle='dashed', linewidth=1)
    axs[2, 1].hist(fake_cam_lengths, bins = np.arange(5, 550), color = 'red')
    axs[2, 1].axvline(fake_cam_lengths.mean(), color='k', linestyle='dashed', linewidth=1)
    fig.suptitle('Paragraphs lengths', fontsize = 16)
    plt.show()
=======
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
>>>>>>> fbdc462e4eee0840809dbda8be9f57975a46267b
