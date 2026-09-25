from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch


MODEL_NAME = "cross-encoder/nli-deberta-v3-base"


# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

# Load NLI model
model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME
)


def verify_claim(claim: str, evidence: str):
    """
    Verify a claim against a piece of evidence.

    Parameters:
        claim: The factual claim we want to verify.
        evidence: The retrieved evidence.

    Returns:
        Dictionary containing:
        - label
        - confidence
        - probabilities
    """

    # Evidence = premise
    # Claim = hypothesis
    inputs = tokenizer(
        evidence,
        claim,
        return_tensors="pt",
        truncation=True,
        max_length=512
    )

    # Disable gradient calculation
    with torch.no_grad():
        outputs = model(**inputs)

    # Convert logits to probabilities
    probabilities = torch.softmax(
        outputs.logits,
        dim=-1
    )[0]

    # Get predicted class
    predicted_id = torch.argmax(probabilities).item()

    # Get model label
    label = model.config.id2label[predicted_id]

    # Normalize label
    label = label.lower()

    # Convert model output into our project terminology
    if "entail" in label:
        status = "supported"

    elif "contradict" in label:
        status = "hallucinated"

    else:
        status = "unverified"

    return {
        "label": label,
        "status": status,
        "confidence": round(
            probabilities[predicted_id].item(),
            4
        ),
        "probabilities": {
            model.config.id2label[i].lower(): round(
                probabilities[i].item(),
                4
            )
            for i in range(len(probabilities))
        }
    }