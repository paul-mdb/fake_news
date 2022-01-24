from re import I
from annotations import get_annotations
from paragraphs import extract_paragraphs, get_article_data, get_article_location, get_url
from selenium import webdriver

def generate_paragraphs_ann(driver: webdriver.Firefox, id: int) -> dict:
    path = get_article_location(id)
    label = path.split('-')[0].split('/')[1].replace('_', ' ')
    data = get_article_data(path)
    url = get_url(data)
    
    paragraphs = extract_paragraphs(driver, label, url)
    annotations = get_annotations(id)

    document_label = annotations["label"]
    annotations = annotations["annotations"]

    paragraphs_ann = {"label": document_label, "content": []}

    cursor = 0
    ann_cursor = 0

    for paragraph in paragraphs:
        paragraph_ann = {"content": []}
        subcontent = paragraph

        if ann_cursor == len(annotations):
            paragraph_ann["content"] = paragraph

        while ann_cursor < len(annotations):
            annotation = annotations[ann_cursor]
            length = len(subcontent)

            if not length:
                break

            # Particular case due to the extraction
            if subcontent == " ":
                cursor += 1
                break

            start = annotation["start"]
            ann_text = annotation["text"]
            ann_label = annotation["label"]

            if cursor + length <= start:
                cursor += length

                if len(paragraph_ann["content"]):
                    neutral_content = {"content": subcontent}
                    paragraph_ann["content"].append(neutral_content)
                else:
                    paragraph_ann["content"] = paragraph

                break
            else:
                subcursor = start - cursor
                stop = subcursor + len(ann_text)

                if subcursor < 0:
                    print("> This annotation is inside an other one.")
                    print("> Skipping.")
                    continue

                # Annotation between two paragraphs
                if subcursor + length <= stop: #TODO: bug 772
                    stop = subcursor + length

                    ann_split_len = len(ann_text) - length

                    # if ann_split_len < 0:
                    #     paragraph_ann["content"] = subcontent
                    #     break

                    ann_split = {
                        "label": ann_label,
                        "start": cursor + stop,
                        "text": ann_text[-ann_split_len:]
                    }

                    print(ann_split)

                    annotations[ann_cursor] = ann_split

                    ann_text = ann_text[:length]
                    print(ann_text)

                    if not len(paragraph_ann["content"]):
                        paragraph_ann = {"label": ann_label, "content": ann_text}
                        cursor += stop
                        break
                else:
                    ann_cursor += 1

                neutral, ann, subcontent = subcontent[:subcursor], subcontent[subcursor:stop], subcontent[stop:]
                cursor += stop

                if ann == ann_text:
                    if len(neutral):
                        neutral_content = {"content": neutral}
                        paragraph_ann["content"].append(neutral_content)

                    ann_content = {"label": ann_label, "content": ann_text}

                    if not len(neutral) and (not len(subcontent) or subcontent == " "):
                        paragraph_ann = ann_content
                    else:
                        paragraph_ann["content"].append(ann_content)

                    if ann_cursor == len(annotations) and len(subcontent):
                        neutral_content = {"content": subcontent}
                        paragraph_ann["content"].append(neutral_content)
                else:
                    print(f"> The text of the annotation #{ann_cursor} doesn't match with the paragraphs.")
                    print(f"Text in the annotation: {ann_text}")
                    print(f"Text in the paragraph: {ann}")
                    print("> Skipping.")

        if len(paragraph_ann["content"]):
            paragraphs_ann["content"].append(paragraph_ann)

    return paragraphs_ann

if __name__ == '__main__':
    driver = webdriver.Firefox()

    article_id = 4 # 772
    paragraphs_ann = generate_paragraphs_ann(driver, article_id)
    print(paragraphs_ann)