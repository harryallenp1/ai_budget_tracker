📊 AI Budget Tracker

An intelligent budgeting assistant that uses Mistral LLM to understand your credit card statements, extract transactions, and categorize expenses. Paste transaction text or use OCR on images — get structured insights, rephrased descriptions, and category-wise spending breakdowns.

⸻

🚀 Features
	•	🔎 Text or OCR input support
	•	🤖 AI-driven extraction with date, vendor, amount, and category
	•	💬 Natural language summary of each transaction
	•	📊 Total spending per category
	•	📝 Saves structured report to text file

⸻

🛠️ Requirements
	•	Python 3.8+
	•	Ollama (to run Mistral locally)
	•	Tesseract (optional, for OCR)
	•	Install dependencies:

    ```pip install -r requirements.txt```

🧠 Mistral Setup (via Ollama)
1.	Install Ollama: https://ollama.com/download
2.	Pull the Mistral model:
    
    ```ollama pull mistral```

3.  Run Mistral:

    ```ollama run mistral```


📸 OCR for Scanned Statements (optional)

To extract text from images:
📥 How to Use
	1.	Run the script:
       ```python3 mistral_budget_parser.py```
    
    2.	Paste your transaction list (e.g.):
       ``` Apr 01 Apr 02 UBER CANADA TORONTO ON Restaurants 22.08
           Apr 09 Apr 10 KLARNA* WALMART VANCOUVER BC Retail and Grocery 14.26```

    3.	Press Enter twice
	
    4.	Output:

	•	Clean summary of transactions
	•	Totals by category
	•	File saved to mistral_expense_report.txt

⸻

📂 Folder Structure
ai_budget_tracker/
│
├── mistral_budget_parser.py      ← Main script
├── requirements.txt
├── statement_apr2025.png         ← (optional image file)
├── ocr_output_apr2025.txt        ← (optional OCR text output)
├── mistral_expense_report.txt    ← Final AI-generated report