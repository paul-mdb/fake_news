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
    test = 0

    #TODO: Handle ann between two paragraphs: kind of split the annotation ?
    for paragraph in paragraphs:
        paragraph_ann = {"content": []}
        subcontent = paragraph
        test += len(paragraph)

        if not len(annotations):
            paragraph_ann["content"] = paragraph
            continue

        for ann_id, annotation in enumerate(annotations):
            length = len(subcontent)

            if not length:
                break

            start = annotation["start"]
            ann_text = annotation["text"]
            ann_label = annotation["label"]

            if cursor + length < start:
                print(f"Length: {length}")
                cursor += length # - 1
                print(f"{cursor} == {test} ?")
                if len(paragraph_ann["content"]):
                    neutral_content = {"content": subcontent}
                    paragraph_ann["content"].append(neutral_content)
                else:
                    paragraph_ann["content"] = paragraph

                break
            else: # Should we remove the annotation once it has been used ? Y
                del annotations[ann_id]
                
                subcursor = start - cursor
                stop = subcursor + len(ann_text)

                print(f"Start: {start}")
                print(f"Cursor: {cursor}")
                print(f"Stop: {stop}")

                neutral, ann, subcontent = subcontent[:subcursor], subcontent[subcursor:stop], subcontent[stop:]
                cursor += stop

                if ann == ann_text:
                    if len(neutral) > 0:
                        neutral_content = {"content": neutral}
                        paragraph_ann["content"].append(neutral_content)

                    ann_content = {"label": ann_label, "content": ann_text}
                    paragraph_ann["content"].append(ann_content)
                else:
                    print(f"> The text of the annotation #{ann_id} doesn't match with the paragraphs.")
                    print(f"Text in the annotation: {ann_text}")
                    print(f"Text in the paragraph: {ann}")
                    print("> Skipping.")

        if len(paragraph_ann["content"]):
            paragraphs_ann["content"].append(paragraph_ann)

    return paragraphs_ann

if __name__ == '__main__':
    driver = webdriver.Firefox()

    paragraphs_ann = generate_paragraphs_ann(driver, 772)
    print(paragraphs_ann)


# $ python paragraph_ann.py
# Association des climatoaarealistes
# 772.txt found on page 25/62
# > The text of the annotation #0 doesn't match with the paragraphs.
# Text in the annotation: La messe est dite, bonnes gens, alors circulez : il n▒y a plus rien ▒ voir▒
# Text in the paragraph:  messe est dite, bonnes gens, alors circulez : il n▒y a plus rien ▒ voir▒
# > Skipping.
# > The text of the annotation #0 doesn't match with the paragraphs.
# Text in the annotation: Des co▒ts pour rien
# Text in the paragraph:  int▒ressant : dans
# > Skipping.
# > The text of the annotation #0 doesn't match with the paragraphs.
# Text in the annotation: ne servirait absolument ▒ rien
# Text in the paragraph: CLIMAT
# > Skipping.
# > The text of the annotation #0 doesn't match with the paragraphs.
# Text in the annotation: l▒humanit▒ marche aujourd▒hui sur la t▒te, voire devient folle
# Text in the paragraph: d▒ objectifs contradictoires impossibles ▒ concilier. Karl Mar
# > Skipping.
# > The text of the annotation #0 doesn't match with the paragraphs.
# Text in the annotation: agitation politico-m▒diatique
# Text in the paragraph:
# > Skipping.
# > The text of the annotation #0 doesn't match with the paragraphs.
# Text in the annotation: nouveau petit ▒ge glaciaire dont le retour n▒est pas une hypoth▒se farfelue
# Text in the paragraph: Nous nous trouverions d▒munis pour  faire face ▒ un nouveau petit ▒ge glaci
# > Skipping.
# > The text of the annotation #0 doesn't match with the paragraphs.
# Text in the annotation: ACTIVIT▒S DE L▒ASSOCIATION, DE SES MEMBRES ET DE SES SYMPATHISANTS  Lettre ouverte de Catherine et Jacques Guyot  au d▒put▒ pro ▒olien de la Vienne Nicolas Turquois La France n▒est pas ▒ vendre : oui ▒ l▒▒cologie, non au saccage de nos territoires par l▒▒olien. ▒ d▒couvrir sur le site de la F▒d▒ration Environnement Durable de Jean-Louis Butr▒. Ubu chez les Allemands, ou les chiffres officiels d▒une combinaison perdante Un article de Jean Pierre Riou, publi▒ sur son blog. ▒olien, CO2 : une politique ▒nerg▒tique absurde Un article de Jean-Pierre Bardinet dans Contrepoints. PPE : confusion dans le pilotage de la politique ▒nerg▒tique de la France Un article de Michel Gay dans Le monde de l▒▒nergie. DERNI▒RES PUBLICATIONS SUR LE SITE DE L▒ASSOCIATION
# Text in the paragraph: SES MEMBRES ET DE SES SYMPATHISANTS
# > Skipping.
# {'label': 3, 'content': [{'content': 'Mais ▒ quoi va servir ce sixi▒me rapport si, comme on l▒entend ici et l▒ (et notamment ▒ France Inter), la science est d▒j▒ ▒tablie ? Une publication de Nature Climate Change sugg▒re que les rapports du GIEC ne devraient plus traiter  de l▒attribution des causes mais de solutions au changement climatique. La messe est dite, bonnes gens, alors circulez : il n▒y a plus rien ▒ voir▒'}, {'content': 'Point d▒orgue de ces c▒r▒monies d▒anniversaire, l▒annonce en grande pompe du pacte Jouzel-Laroutorou qui propose un Plan Marshall pour le climat financ▒ (notamment) par une contribution de 5 % sur les b▒n▒fices des entreprises non r▒investis. Des co▒ts pour rien commente l▒▒conomiste R▒my Prud▒homme. D▒tail int▒ressant : dans la liste des premiers signataires du pacte, on trouve tout de m▒me le nom de deux anciens Premiers ministres fran▒ais.'}, {'content': 'CLIMAT : L▒ARTICLE 1er DE LA CONSTITUTION, SINON RIEN'}, {'content': 'N▒en d▒plaise au ministre, tout le monde ne semble pas exactement d▒accord avec ses objectifs. Par exemple, Lo▒k Le Floch-Prigent s▒▒tonne dans Atlantico du ▒ d▒ni de r▒alit▒ d▒sarmant dans lequel s▒enferme la France ▒, expliquant que les pouvoirs publics sont pris dans la nasse d▒ objectifs contradictoires impossibles ▒ concilier. Karl Marx  a ▒crit que l▒humanit▒ ne se pose jamais que des probl▒mes qu▒elle est capable de r▒soudre : une pens▒e frapp▒e au coin du bon sens, sauf que l▒humanit▒ marche aujourd▒hui sur la t▒te, voire devient folle comme l▒affirmait r▒cemment Carlos Tavares.'}, {'content': 'TOUT ▒A POUR QUOI ?'}, {'content': []}, {'content': []}]}
