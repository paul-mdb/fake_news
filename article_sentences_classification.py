import pandas as pd
import spacy
import torch
from transformers import CamembertForSequenceClassification, CamembertTokenizer

from extract_annotated_sentences import get_sentences_from_doc
from tagtog import get_text_from_id
# from extract_annotated_sentences import get_topic_sentences

MODEL_PATH = "articles_sentences.model"

def preprocess(raw_articles, tokenizer, labels=None):
    """
        Create pytorch dataloader from raw data
    """

    # https://huggingface.co/docs/transformers/internal/tokenization_utils#transformers.PreTrainedTokenizerBase.batch_encode_plus.truncation

    encoded_batch = tokenizer.batch_encode_plus(raw_articles,
                                                add_special_tokens=False,
                                                padding = True,
                                                truncation = True,
                                                max_length = 128,
                                                return_attention_mask=True,
                                                return_tensors = 'pt')
        

    if labels:
        labels = torch.tensor(labels)
        return encoded_batch['input_ids'], encoded_batch['attention_mask'], labels
    return encoded_batch['input_ids'], encoded_batch['attention_mask']

def predict(articles, model, tokenizer):
    with torch.no_grad():
        model.eval()
        input_ids, attention_mask = preprocess(articles, tokenizer)
        output = model(input_ids, attention_mask=attention_mask)
        print(output[0])
        return torch.argmax(output[0], dim=1)

if __name__ == "__main__":
    ##
    article_ids = [10202, 3000, 2999, 10204]
    ##

    model = CamembertForSequenceClassification.from_pretrained(
        'camembert-base',
        num_labels = 3
    )
    model.load_state_dict(torch.load(MODEL_PATH))
    model.eval()

    tokenizer = CamembertTokenizer.from_pretrained(
        'camembert-base',
        do_lower_case=True
    )

    nlp = spacy.load("fr_core_news_md", exclude=["parser"])
    nlp.enable_pipe("senter")

    data = []

    for article_id in article_ids:
        content = get_text_from_id(article_id)

        doc = nlp(content)
        sentences = get_sentences_from_doc(doc)

        predicted_labels = predict(sentences, model, tokenizer).tolist()

        for sentence, label in zip(sentences, predicted_labels):
            data.append((article_id, label, sentence))
            print(f'({article_id}) {label}: {sentence}')

    df = pd.DataFrame(data, columns=["article_id", "label", "text"])
    df.to_csv("article_sentences_classification.csv")
        
