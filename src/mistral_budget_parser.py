import requests
import json
import textwrap
from collections import defaultdict

def get_user_input():
    print("📝 Paste your transaction data below. Press Enter **twice** to finish:\n")
    lines = []
    while True:
        line = input()
        if line.strip() == "":
            break
        lines.append(line)
    return "\n".join(lines)

def clean_text(raw_text):
    # Optional: remove weird characters and spacing
    cleaned = raw_text.replace("Ý", "").replace("\r", "").strip()
    return cleaned

def build_prompt(transaction_text):
    return f"""
You are a smart finance assistant.

Below is a block of cleaned transaction text from a credit card statement. 
Please extract each transaction and return them in a structured format like this:

Date: YYYY-MM-DD  
Vendor: <Vendor Name>  
Amount: <Amount>  
Category: <Purchases, Groceries, Bills, Experiences, Eating out, etc.>  
Rephrased: <Human-friendly summary of the transaction>  

Only include real expenses. Skip headers or totals.

Text:
{transaction_text}
"""

def query_mistral(prompt):
    response_text = ""
    res = requests.post("http://localhost:11434/api/generate", json={
        "model": "mistral",
        "prompt": prompt,
        "stream": True
    }, stream=True)

    for line in res.iter_lines():
        if line:
            raw = line.decode("utf-8").removeprefix("data: ")
            try:
                data = json.loads(raw)
                response_text += data.get("response", "")
            except json.JSONDecodeError:
                continue
    return response_text

def summarize_by_category(mistral_output):
    totals = defaultdict(float)
    current_category = None

    for line in mistral_output.splitlines():
        line = line.strip()
        if line.startswith("Category:"):
            current_category = line.split(":", 1)[1].strip()
        elif line.startswith("Amount:"):
            try:
                amount = float(line.split(":", 1)[1].strip())
                if current_category:
                    totals[current_category] += amount
            except ValueError:
                continue
    return totals

# ---- Main Workflow ---- #
if __name__ == "__main__":
    raw_input = get_user_input()
    cleaned_input = clean_text(raw_input)
    prompt = build_prompt(cleaned_input)
    print("\n🤖 Asking Mistral to summarize...\n")
    result = query_mistral(prompt)

    print("\n📊 AI Expense Breakdown:\n")
    print(textwrap.indent(result.strip(), "  "))

    category_totals = summarize_by_category(result)
    print("\n📊 Total Spending by Category:\n")
    for category, total in category_totals.items():
        print(f"  {category}: ${total:.2f}")

    # Optional: save to file
    with open("mistral_expense_report.txt", "w") as f:
        f.write(result.strip())