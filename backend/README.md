---
title: LLM Hallucination Detector API

colorFrom: blue
colorTo: purple
sdk: docker
app_port: 7860
---

# LLM Hallucination Detector API

FastAPI backend for claim-level hallucination detection in LLM-generated text.

## Pipeline

LLM Answer
↓
Claim Extraction
↓
Evidence Retrieval
↓
Semantic Similarity
↓
DeBERTa NLI
↓
Hallucination Score

## Technologies

- FastAPI
- spaCy
- Groq
- Sentence Transformers
- ChromaDB
- DeBERTa NLI
- Wikipedia API