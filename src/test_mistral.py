import requests
import json
import textwrap
from collections import defaultdict
import os
import datetime

# Save result to a timestamped report
def save_report(text, folder="reports"):
    if not os.path.exists(folder):
        os.makedirs(folder)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"report_{timestamp}.txt"
    path = os.path.join(folder, filename)
    with open(path, "w") as f:
        f.write(text)
    print(f"\n💾 Saved report to: {path}")

# Delete all .txt files in reports/ before writing new output
def clear_old_reports(folder="reports"):
    if not os.path.exists(folder):
        os.makedirs(folder)  # in case the folder doesn't exist
    for filename in os.listdir(folder):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder, filename)
            os.remove(file_path)
            print(f"🗑️ Deleted old report: {filename}")

# Call it at the start
clear_old_reports()
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

def summarize_categories(parsed_text):
    category_totals = defaultdict(lambda: {"spent": 0.0, "refunded": 0.0})
    total_spent = 0.0
    total_refunded = 0.0

    current_category = None

    for line in parsed_text.splitlines():
        line = line.strip()

        if line.startswith("Category:"):
            current_category = line.split(":", 1)[1].strip()

        elif line.startswith("Amount:"):
            try:
                amount = float(line.split(":", 1)[1].strip())
                if current_category:
                    if amount >= 0:
                        category_totals[current_category]["spent"] += amount
                        total_spent += amount
                    else:
                        category_totals[current_category]["refunded"] += abs(amount)
                        total_refunded += abs(amount)
            except ValueError:
                continue

    return category_totals, total_spent, total_refunded

# ---- Main Workflow ---- #
if __name__ == "__main__":
    raw_input = get_user_input()
    cleaned_input = clean_text(raw_input)
    prompt = build_prompt(cleaned_input)
    print("\n🤖 Asking Mistral to summarize...\n")
    result = query_mistral(prompt)

    print("\n📊 AI Expense Breakdown:\n")
    print(textwrap.indent(result.strip(), "  "))
    save_report(result.strip())

    # 📊 Add category-wise summary
    category_totals, total_spent, total_refunded = summarize_categories(result)
    print("\n📊 Total Spending by Category:\n")
    for category, data in category_totals.items():
        net = data["spent"] - data["refunded"]
        print(f"  {category}:")
        print(f"    Spent:    ${data['spent']:.2f}")
        print(f"    Refunded: ${data['refunded']:.2f}")
        print(f"    Net:      ${net:.2f}")

    print("\n💰 Overall Totals:")
    print(f"  Total Spent:    ${total_spent:.2f}")
    print(f"  Total Refunded: ${total_refunded:.2f}")
    print(f"  Net Total:      ${total_spent - total_refunded:.2f}")