from services.verification_service import verify_claim


claim = "The Taj Mahal was built by Akbar."

evidence = (
    "The Taj Mahal was commissioned by the Mughal emperor "
    "Shah Jahan in memory of his wife Mumtaz Mahal."
)

result = verify_claim(
    claim,
    evidence
)

print(result)