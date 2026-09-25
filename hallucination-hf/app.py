import gradio as gr

from services.text_processor import process_text
from services.claim_extractor import extract_claims
from services.retrieval_service import (
    load_evidence,
    retrieve_evidence
)
from services.web_search_service import search_wikipedia
from services.verification_service import verify_claim
from services.scoring_service import (
    calculate_claim_score,
    calculate_overall_score
)
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Load local evidence into ChromaDB
load_evidence()


def analyze_text(text):
    if not text or not text.strip():
        return "Please enter some text.", "", ""

    try:
        # NLP processing
        processed = process_text(text)

        # Extract claims
        claims = extract_claims(text)

        claim_results = []

        for claim in claims["claims"]:

            claim_text = claim["text"]

            # Local evidence
            local_evidence = retrieve_evidence(
                claim_text,
                top_k=3
            )

            # Web evidence
            web_results = search_wikipedia(
                claim_text,
                limit=3
            )

            for result in web_results:

                snippet = result.get(
                    "snippet",
                    ""
                )

                if snippet.strip():

                    local_evidence.append({
                        "text": snippet,
                        "source": result.get(
                            "source",
                            "Wikipedia"
                        ),
                        "url": result.get("url"),
                        "similarity_distance": None
                    })

            # Verify against evidence
            verified_evidence = []

            for item in local_evidence:

                evidence_text = item.get(
                    "text",
                    ""
                )

                if not evidence_text.strip():
                    continue

                verification = verify_claim(
                    claim_text,
                    evidence_text
                )

                verified_evidence.append({
                    "text": evidence_text,
                    "source": item.get("source"),
                    "url": item.get("url"),
                    "similarity_distance": item.get(
                        "similarity_distance"
                    ),
                    "verification": verification
                })

            claim_verification = calculate_claim_score(
                verified_evidence
            )

            claim_results.append({
                "id": claim["id"],
                "claim": claim_text,
                "evidence": verified_evidence,
                "verification": claim_verification
            })

        overall = calculate_overall_score(
            claim_results
        )

        # Build readable output
        claim_output = []

        for result in claim_results:

            verification = result["verification"]

            claim_output.append(
                f"""
### Claim {result["id"]}

**{result["claim"]}**

**Status:** `{verification["status"]}`

**Confidence:** `{verification["confidence"]}`

**Hallucination Score:** `{verification["hallucination_score"]}`

**NLI Scores**
- Entailment: `{verification["nli_scores"]["entailment"]}`
- Contradiction: `{verification["nli_scores"]["contradiction"]}`
- Neutral: `{verification["nli_scores"]["neutral"]}`
"""
            )

        claims_text = "\n---\n".join(
            claim_output
        )

        # Evidence output
        evidence_output = []

        for result in claim_results:

            for evidence in result["evidence"]:

                evidence_output.append(
                    f"""
**Claim {result["id"]}**

Evidence: {evidence["text"]}

Source: {evidence["source"]}

Verification: `{evidence["verification"]["status"]}`

Confidence: `{evidence["verification"]["confidence"]}`
"""
                )

        evidence_text = "\n---\n".join(
            evidence_output
        )

        overall_text = f"""
## Overall Result

**Hallucination Score:** `{overall["hallucination_score"]}`

**Hallucination Percentage:** `{overall["hallucination_percentage"]}%`

**Total Claims:** `{overall["total_claims"]}`

**Hallucinated Claims:** `{overall["hallucinated_claims"]}`

### NLP Entities

{processed["entities"]}
"""

        return (
            overall_text,
            claims_text,
            evidence_text
        )

    except Exception as error:

        return (
            f"### Error\n\n```text\n{str(error)}\n```",
            "",
            ""
        )


demo = gr.Interface(
    fn=analyze_text,
    inputs=gr.Textbox(
        lines=10,
        placeholder=(
            "Enter an LLM-generated answer "
            "to analyze..."
        ),
        label="LLM Generated Text"
    ),
    outputs=[
        gr.Markdown(label="Overall Result"),
        gr.Markdown(label="Claims"),
        gr.Markdown(label="Evidence & Verification")
    ],
    title="🔎 LLM Hallucination Detector",
    description=(
        "Claim-level hallucination detection using "
        "semantic retrieval, web evidence and DeBERTa NLI."
    ),
    examples=[
        [
            "The Taj Mahal was built by Akbar."
        ],
        [
            "The Taj Mahal was commissioned by "
            "Shah Jahan and is located in Agra."
        ]
    ]
)


if __name__ == "__main__":
    demo.launch()