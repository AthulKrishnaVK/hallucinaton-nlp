def calculate_claim_score(verifications):
    """
    Calculate the verification result for a claim
    using multiple evidence items.
    """

    if not verifications:
        return {
            "status": "unverified",
            "hallucination_score": 1.0,
            "confidence": 0.0
        }

    # Find the strongest evidence for each NLI category
    entailment_score = max(
        item["verification"]["probabilities"].get(
            "entailment", 0
        )
        for item in verifications
    )

    contradiction_score = max(
        item["verification"]["probabilities"].get(
            "contradiction", 0
        )
        for item in verifications
    )

    neutral_score = max(
        item["verification"]["probabilities"].get(
            "neutral", 0
        )
        for item in verifications
    )

    # Determine claim status
    if entailment_score >= contradiction_score:
        if entailment_score >= neutral_score:
            status = "supported"
            confidence = entailment_score
        else:
            status = "unverified"
            confidence = neutral_score

    else:
        if contradiction_score >= neutral_score:
            status = "hallucinated"
            confidence = contradiction_score
        else:
            status = "unverified"
            confidence = neutral_score

    # Hallucination score
    #
    # 0.0 = strongly supported
    # 1.0 = strongly contradicted
    #
    # Neutral claims receive an intermediate score.
    if status == "supported":
        hallucination_score = 1 - entailment_score

    elif status == "hallucinated":
        hallucination_score = contradiction_score

    else:
        hallucination_score = 0.5

    return {
        "status": status,
        "hallucination_score": round(
            hallucination_score,
            4
        ),
        "confidence": round(
            confidence,
            4
        ),
        "nli_scores": {
            "entailment": round(
                entailment_score,
                4
            ),
            "contradiction": round(
                contradiction_score,
                4
            ),
            "neutral": round(
                neutral_score,
                4
            )
        }
    }


def calculate_overall_score(claim_results):
    """
    Calculate hallucination score for the complete response.
    """

    if not claim_results:
        return {
            "hallucination_score": 0.0,
            "hallucination_percentage": 0.0,
            "total_claims": 0,
            "hallucinated_claims": 0
        }

    total_claims = len(claim_results)

    hallucinated_claims = sum(
        1
        for claim in claim_results
        if claim["verification"]["status"] == "hallucinated"
    )

    hallucination_score = (
        hallucinated_claims / total_claims
    )

    return {
        "hallucination_score": round(
            hallucination_score,
            4
        ),
        "hallucination_percentage": round(
            hallucination_score * 100,
            2
        ),
        "total_claims": total_claims,
        "hallucinated_claims": hallucinated_claims
    }