# from fastapi import FastAPI
# from pydantic import BaseModel
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI( title="LLM Hallucination Detector",
#     version="0.1.0")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
# from services.text_processor import process_text
# from services.claim_extractor import extract_claims

# from services.retrieval_service import (
#     load_evidence,
#     retrieve_evidence
# )

# from services.web_search_service import (
#     search_wikipedia
# )

# from services.verification_service import (
#     verify_claim
# )

# from services.scoring_service import (
#     calculate_claim_score,
#     calculate_overall_score
# )


# # --------------------------------------------------
# # FastAPI Application
# # --------------------------------------------------

# app = FastAPI(
#     title="LLM Hallucination Detector",
#     version="0.1.0"
# )


# # --------------------------------------------------
# # Request Model
# # --------------------------------------------------

# class TextRequest(BaseModel):
#     text: str


# # --------------------------------------------------
# # Startup
# # --------------------------------------------------

# @app.on_event("startup")
# def startup_event():
#     """
#     Load local evidence into ChromaDB
#     when the application starts.
#     """

#     load_evidence()


# # --------------------------------------------------
# # Root Endpoint
# # --------------------------------------------------

# @app.get("/")
# def root():

#     return {
#         "message": "Hallucination Detection API is running"
#     }


# # --------------------------------------------------
# # Analyze Endpoint
# # --------------------------------------------------

# @app.post("/api/analyze")
# def analyze(request: TextRequest):

#     # ----------------------------------------------
#     # 1. NLP Processing
#     # ----------------------------------------------

#     processed = process_text(
#         request.text
#     )


#     # ----------------------------------------------
#     # 2. Claim Extraction
#     # ----------------------------------------------

#     claims = extract_claims(
#         request.text
#     )


#     claim_results = []


#     # ----------------------------------------------
#     # 3. Process Every Claim
#     # ----------------------------------------------

#     for claim in claims["claims"]:

#         claim_text = claim["text"]


#         # ------------------------------------------
#         # 4. Retrieve Local Evidence
#         # ------------------------------------------

#         local_evidence = retrieve_evidence(
#             claim_text,
#             top_k=3
#         )


#         # ------------------------------------------
#         # 5. Filter Weak Semantic Matches
#         # ------------------------------------------

#         local_evidence = [
#             item
#             for item in local_evidence
#             if item.get("similarity", 0) >= 0.45
#         ]


#         # ------------------------------------------
#         # 6. Search Wikipedia
#         # ------------------------------------------

#         web_results = search_wikipedia(
#             claim_text,
#             limit=3
#         )


#         # ------------------------------------------
#         # 7. Add Web Evidence
#         # ------------------------------------------

#         for result in web_results:

#             snippet = result.get(
#                 "snippet",
#                 ""
#             )


#             if snippet.strip():

#                 local_evidence.append({

#                     "text": snippet,

#                     "source": result.get(
#                         "source",
#                         "Wikipedia"
#                     ),

#                     "url": result.get(
#                         "url"
#                     ),

#                     "similarity_distance": None,

#                     "similarity": None

#                 })


#         # ------------------------------------------
#         # 8. Verify Evidence Using DeBERTa
#         # ------------------------------------------

#         verified_evidence = []


#         for item in local_evidence:

#             evidence_text = item.get(
#                 "text",
#                 ""
#             )


#             # Skip empty evidence

#             if not evidence_text.strip():
#                 continue


#             verification = verify_claim(
#                 claim_text,
#                 evidence_text
#             )


#             verified_evidence.append({

#                 "text": evidence_text,

#                 "source": item.get(
#                     "source"
#                 ),

#                 "url": item.get(
#                     "url"
#                 ),

#                 "similarity_distance": item.get(
#                     "similarity_distance"
#                 ),

#                 "similarity": item.get(
#                     "similarity"
#                 ),

#                 "verification": verification

#             })


#         # ------------------------------------------
#         # 9. Calculate Claim-Level Result
#         # ------------------------------------------

#         claim_verification = calculate_claim_score(
#             verified_evidence
#         )


#         # ------------------------------------------
#         # 10. Store Claim Result
#         # ------------------------------------------

#         claim_results.append({

#             "id": claim["id"],

#             "claim": claim_text,

#             "evidence": verified_evidence,

#             "verification": claim_verification

#         })


#     # ----------------------------------------------
#     # 11. Calculate Overall Hallucination Score
#     # ----------------------------------------------

#     overall_score = calculate_overall_score(
#         claim_results
#     )


#     # ----------------------------------------------
#     # 12. Final API Response
#     # ----------------------------------------------

#     return {

#         "input": request.text,

#         "nlp": processed,

#         "claims": claim_results,

#         "overall": overall_score

#     }


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from services.text_processor import process_text
from services.claim_extractor import extract_claims

from services.retrieval_service import (
    load_evidence,
    retrieve_evidence
)

from services.web_search_service import (
    search_wikipedia
)

from services.verification_service import (
    verify_claim
)

from services.scoring_service import (
    calculate_claim_score,
    calculate_overall_score
)


# --------------------------------------------------
# FastAPI Application
# --------------------------------------------------

app = FastAPI(
    title="LLM Hallucination Detector",
    version="0.1.0"
)


# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,

    # Development configuration
    allow_origins=["*"],

    allow_credentials=False,

    allow_methods=["*"],

    allow_headers=["*"],
)


# --------------------------------------------------
# Request Model
# --------------------------------------------------

class TextRequest(BaseModel):
    text: str


# --------------------------------------------------
# Startup
# --------------------------------------------------

@app.on_event("startup")
def startup_event():

    load_evidence()


# --------------------------------------------------
# Root Endpoint
# --------------------------------------------------

@app.get("/")
def root():

    return {
        "message": "Hallucination Detection API is running"
    }


# --------------------------------------------------
# Analyze Endpoint
# --------------------------------------------------

@app.post("/api/analyze")
def analyze(request: TextRequest):

    # 1. NLP processing
    processed = process_text(
        request.text
    )

    # 2. Extract claims
    claims = extract_claims(
        request.text
    )

    claim_results = []

    # 3. Process each claim
    for claim in claims["claims"]:

        claim_text = claim["text"]

        # 4. Retrieve local evidence
        local_evidence = retrieve_evidence(
            claim_text,
            top_k=3
        )

        # 5. Filter weak matches
        local_evidence = [
            item
            for item in local_evidence
            if item.get("similarity", 0) >= 0.45
        ]

        # 6. Search Wikipedia
        web_results = search_wikipedia(
            claim_text,
            limit=3
        )

        # 7. Add web evidence
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
                    "url": result.get(
                        "url"
                    ),
                    "similarity_distance": None,
                    "similarity": None
                })

        # 8. Verify evidence
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
                "source": item.get(
                    "source"
                ),
                "url": item.get(
                    "url"
                ),
                "similarity_distance": item.get(
                    "similarity_distance"
                ),
                "similarity": item.get(
                    "similarity"
                ),
                "verification": verification
            })

        # 9. Calculate claim score
        claim_verification = calculate_claim_score(
            verified_evidence
        )

        # 10. Store claim result
        claim_results.append({
            "id": claim["id"],
            "claim": claim_text,
            "evidence": verified_evidence,
            "verification": claim_verification
        })

    # 11. Overall score
    overall_score = calculate_overall_score(
        claim_results
    )

    # 12. Response
    return {
        "input": request.text,
        "nlp": processed,
        "claims": claim_results,
        "overall": overall_score
    }