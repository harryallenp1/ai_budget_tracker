import requests

prompt = """
Categorize and rephrase the following transaction:
Transaction: Klarna Walmart VANCOUVER BC

Use categories: Travel, Purchases, Misc, Bills, Housing, Groceries, Experiences, Eating out.
Respond like:
Category: <...>
Rephrased: <...>
"""

res = requests.post("http://localhost:11434/api/generate", json={
    "model": "mistral",
    "prompt": prompt
})

print(res.json()["response"])