import json
from paragraph_ann import generate_paragraphs_ann, visualize
from selenium import webdriver

EXTRACT_PARAGRAPHS_ANN_FOLDER = "annotations/"

def extract_paragraphs_ann(driver, article_id):
    paragraphs_ann = generate_paragraphs_ann(driver, article_id)
    # visualize(paragraphs_ann)
    path = EXTRACT_PARAGRAPHS_ANN_FOLDER + str(article_id) + ".json"
    print(f"> Saving in {path}")
    with open(path, "w") as f:
        f.write(json.dumps(paragraphs_ann))

if __name__ == "__main__":
    driver = webdriver.Firefox()

    for article_id in range(1, 1000):
        try:
            extract_paragraphs_ann(driver, article_id)
        except Exception as e:
            continue

    driver.quit()