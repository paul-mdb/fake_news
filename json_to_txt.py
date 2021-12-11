import os, json
import numpy as np
import pickle
 
# Function to rename multiple files
def main():

    dictionary_of_matches = {}
    json_folder = "articles"
    text_folder = "/Users/paulmeddeb/2A-Mines/data_Sophia/fake_news/text_articles"
    n = len(os.listdir(json_folder))
    numbering = np.arange(n)
    np.random.shuffle(numbering)

    for count, filename in enumerate(os.listdir(json_folder)):

        with open(os.path.join(json_folder, filename)) as json_file:
            json_text = json.load(json_file)
            file = open(os.path.join(text_folder, f"{numbering[count]}.txt"), "w") 
            file.write(json_text['content']) 
            file.close() 
            dictionary_of_matches[numbering[count]] = filename
    a_file = open("match_dictionary.pkl", "wb")
    pickle.dump(dictionary_of_matches, a_file)
    a_file.close()
    a_file = open("match_dictionary.pkl", "rb")
    output = pickle.load(a_file)
    print(output)

if __name__ == '__main__':
     
    main()