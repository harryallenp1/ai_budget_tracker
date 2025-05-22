from ocr import extract_text_from_image
from categorize import categorize_and_rephrase
from excel_writer import write_to_excel

# Simulate rows like you'd get from OCR
raw_transactions = [
    ("2025-04-01", "WALMART.CA", 16.48),
    ("2025-04-03", "UBER CANADA", 23.14)
]

results = []
for date, desc, amount in raw_transactions:
    ai_result = categorize_and_rephrase(desc)
    lines = ai_result.splitlines()
    category = lines[0].replace("Category: ", "").strip()
    rephrased = lines[1].replace("Rephrased: ", "").strip()
    results.append((date, desc, category, rephrased, amount))

write_to_excel(results)