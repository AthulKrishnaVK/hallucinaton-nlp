---
title: LLM Hallucination Detector
emoji: 🔎
colorFrom: blue
colorTo: purple
sdk: gradio
app_file: app.py
python_version: "3.11"
---

# LLM Hallucination Detector

Claim-level hallucination detection for LLM-generated text.

## Pipeline

LLM Generated Text
→ Claim Extraction
→ Evidence Retrieval
→ Web Search
→ DeBERTa NLI
→ Hallucination Score

## Technologies

- Python
- Gradio
- spaCy
- Groq
- Sentence Transformers
- ChromaDB
- DeBERTa NLI