import requests

def query_mistral(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "mistral", "prompt": prompt}
    )
    return response.json()["response"]

def categorize_and_rephrase(description):
    prompt = f"""
You are a highly accurate financial assistant.

Below is a transaction description. You must analyze it and return:

1. A category from this list ONLY: Travel, Purchases, Misc, Bills, Housing, Groceries, Experiences, Eating out, Personal and Household Expenses, Professional and Financial Services
2. A rephrased version of the transaction in human-friendly language.

Transaction: "{description}"

Return ONLY in this format:
Category: <one from the list>
Rephrased: <clean description>

Do not explain or add any commentary.
"""

    result = query_mistral(prompt)
    return result