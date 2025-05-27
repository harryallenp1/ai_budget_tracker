import pandas as pd
import os
import datetime

def save_to_excel(parsed_text, filename="reports/expense_report.xlsx"):
    entries = []
    current_entry = {}

    for line in parsed_text.splitlines():
        line = line.strip()

        if line.startswith("Date:"):
            current_entry["Date"] = line.split(":", 1)[1].strip()
        
        elif line.startswith("Vendor:"):
            vendor = line.split(":", 1)[1].strip()

            if "KLARNA" in vendor and "WALMART" in vendor:
                vendor = "WALMART"
            elif "UBER" in vendor and "UBEREATS" in vendor:
                vendor = "UBER EATS"
            elif "UBER CANADA" in vendor:
                vendor = "UBER RIDE"

            current_entry["Vendor"] = vendor
        elif line.startswith("Amount:"):
            try:
                current_entry["Amount"] = float(line.split(":", 1)[1].strip())
            except ValueError:
                current_entry["Amount"] = None
        elif line.startswith("Category:"):
            current_entry["Category"] = line.split(":", 1)[1].strip()
        elif line.startswith("Rephrased:"):
            current_entry["Rephrased"] = line.split(":", 1)[1].strip()
            entries.append(current_entry)
            current_entry = {}

    if not entries:
        print("⚠️ No entries to write to Excel.")
        return

    df = pd.DataFrame(entries)
    os.makedirs("reports", exist_ok=True)
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"reports/expense_report_{timestamp}.xlsx"
    df.to_excel(filename, index=False)
    print(f"📁 Excel report saved to {filename}")