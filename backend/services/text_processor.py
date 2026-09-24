import spacy

nlp = spacy.load("en_core_web_sm")


def process_text(text: str):
    doc = nlp(text)

    sentences = [
        sentence.text.strip()
        for sentence in doc.sents
    ]

    entities = [
        {
            "text": entity.text,
            "label": entity.label_
        }
        for entity in doc.ents
    ]

    return {
        "sentences": sentences,
        "entities": entities
    }