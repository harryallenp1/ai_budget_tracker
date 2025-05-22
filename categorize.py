import requests

def query_mistral(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "mistral", "prompt": prompt}
    )
    return response.json()["response"]

def categorize_and_rephrase(description):
    prompt = f"""
You are a personal finance assistant. Categorize and rephrase the following transaction:

Transaction: "{description}"

Use one of these categories: Travel, Purchases, Misc, Bills, Housing, Groceries, Experiences, Eating out.

Respond in this format:
Category: <category>
Rephrased: <clean description>
"""
    result = query_mistral(prompt)
    return result