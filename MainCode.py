import mysql.connector
import pandas as pd
from mysql.connector import Error
from openai import OpenAI
import os
import re


def clean_sql_query(sql_query):
    """Clean SQL query by removing markdown code blocks and semicolons"""
    # Remove markdown code blocks (```sql and ```)
    sql_query = re.sub(r'```sql\s*', '', sql_query, flags=re.IGNORECASE)
    sql_query = re.sub(r'```\s*', '', sql_query)
    
    # Remove any leading/trailing whitespace
    sql_query = sql_query.strip()
    
    # Remove semicolon at the end (and anything after it)
    sql_query = re.sub(r';\s*$', '', sql_query)
    
    return sql_query.strip()


os.environ["OPENAI_API_KEY"] = "" # Enter your openai api key here
database = ""  # Enter your database name here
client = OpenAI()

try:
    connection = mysql.connector.connect(
        host="localhost",
        database=database,
        user="root",
        password="" # Enter your mysql password here
    )
    if connection is None:
        print("-" * 50)
        print("SQL Server Not found")
        print("-" * 50)
    elif connection.is_connected():
        print("✅ Connected to SQL Server")
    else:
        print("❌ Not connected to SQL Server")
except Exception as e:
    print(f"❌ Error: {e}")


def main():
    while True:
        user_input = input("\nAsk me anything (or type 'exit'): ").strip()
        if user_input.lower() == "exit":
            break

        # 🔑 Check if user provided direct SQL
        if user_input.strip().lower().startswith("sql:"):
            sql_query = user_input[4:].strip()  # Remove 'SQL:' part
            print("\n👉 You provided this SQL query directly:")
        else:
            # 🔑 Use OpenAI to generate SQL
            system_prompt = f"""
            You are a helpful assistant that converts user questions into SQL queries 
            for a MySQL database named '{database}'. 
            Only return the SQL query, no explanations.
            """
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ]
            )
            sql_query = response.choices[0].message.content.strip()
            print("\n👉 Proposed SQL query:")
        
        # Clean up the query: remove markdown and semicolons
        sql_query = clean_sql_query(sql_query)
        print(sql_query)

        confirm = input("\nRun this query? (yes/no): ")
        if confirm.lower() == "yes":
            try:
                cursor = connection.cursor()
                cursor.execute(sql_query)
                rows = cursor.fetchall()
                columns = [i[0] for i in cursor.description]
                df = pd.DataFrame(rows, columns=columns)
                print("\n✅ Query Results:")
                print(df)
            except Exception as e:
                print(f"❌ Query error: {e}")
        else:
            print("❌ Query cancelled.")

if __name__ == "__main__":
    main()