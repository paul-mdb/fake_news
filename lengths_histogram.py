import os
import matplotlib.pyplot as plt
import numpy as np

PATH = 'text_articles/'

def main():
    lengths = []
    for count, filename in enumerate(os.listdir(PATH)):
        with open(os.path.join(PATH, filename), 'r') as file:
            text = file.read()
            lengths.append(len(text))

    fig, ax = plt.subplots(1)
    fig.suptitle('lengths distribution', fontsize = 16)
    ax.hist(lengths, bins = np.arange(0, 20000, 100))
    plt.show()

if __name__ == '__main__':
    main()