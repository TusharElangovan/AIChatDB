# AIChatDB

# ✅ Natural Language to MySQL Query Assistant

This Python script lets you **talk to your MySQL database in plain English** — or run direct SQL queries — using OpenAI's GPT model to translate your questions into valid SQL.

---

## 🚀 What it does

- **Natural Language Input**  
  Ask questions like:  
  > *"Show me all customers from California"*  
  The script uses GPT to translate your question to SQL, shows you the SQL, asks for confirmation, and then executes it.

- **Direct SQL Input**  
  If you already know SQL, you can skip GPT and just run your query directly:
  SQL: SELECT * FROM customers WHERE state = 'CA'


- **Safe Query Cleaning**  
The script automatically:
- Removes trailing semicolons (`;`)  
- Strips away markdown code blocks (like ```sql) that GPT may include  
- Cleans extra whitespace

- **Easy Output**  
Results are displayed in your terminal as a neat **Pandas DataFrame**.

---

## 📁 Files

| File | Description |
|------|--------------|
| `your_script.py` | The main Python script |
| `README.md` | This instruction file |

---

## ⚙️ Setup

### Install dependencies

In your terminal, run:

```bash
pip install mysql-connector-python pandas openai

