import json
import chromadb

from services.embedding_service import model


client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="evidence"
)


def load_evidence():

    with open(
        "data/evidence.json",
        "r",
        encoding="utf-8"
    ) as file:
        evidence = json.load(file)

    # Avoid inserting duplicate evidence
    if collection.count() > 0:
        return

    documents = []
    ids = []
    metadatas = []

    for item in evidence:

        documents.append(
            item["text"]
        )

        ids.append(
            str(item["id"])
        )

        metadatas.append({
            "source": item["source"]
        })

    embeddings = model.encode(
        documents
    ).tolist()

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )


def retrieve_evidence(
    claim: str,
    top_k: int = 3
):

    claim_embedding = model.encode(
        claim
    ).tolist()

    results = collection.query(
        query_embeddings=[
            claim_embedding
        ],
        n_results=top_k
    )

    evidence = []

    documents = results.get(
        "documents",
        [[]]
    )[0]

    metadatas = results.get(
        "metadatas",
        [[]]
    )[0]

    distances = results.get(
        "distances",
        [[]]
    )[0]

    for i in range(len(documents)):

        distance = distances[i]

        # Chroma distance is lower when documents
        # are more semantically similar.
        similarity = 1 / (1 + distance)

        evidence.append({
            "text": documents[i],
            "source": metadatas[i].get(
                "source",
                "Unknown"
            ),
            "similarity_distance": round(
                distance,
                4
            ),
            "similarity": round(
                similarity,
                4
            )
        })

    return evidence