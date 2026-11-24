from dotenv import load_dotenv
import os
import requests
import re
load_dotenv() #load all the env variables
api_key = os.getenv("GOOGLE_API_KEY")

print("API key loaded:", bool(api_key))
print("API key length:", len(api_key) if api_key else 0)

import streamlit as st
import sqlite3
import google.generativeai as genai

##configure api key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#function to load google gemini model and provide sql query as response
#function to load local model and provide sql query as response
def get_gemini_response(question, prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "qwen2.5-coder:3b",
            "prompt": prompt[0] + "\n" + question,
            "stream": False
        },
        timeout=120
    )
    response.raise_for_status()
    return response.json()["response"]

# Function to retrieve query from the SQL database
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    sql = sql.strip()
    sql = re.sub(r"^```(?:sql)?\s*|\s*```$", "", sql, flags=re.IGNORECASE).strip()
    cur.execute(sql)
   
    rows = cur.fetchall()
    conn.commit()
    conn.close()

    for row in rows:
     print(row)
    return rows


prompt = [
    """
    You are an expert in converting English questions to SQL query!

    The SQL database has the name STUDENT and has the following columns - NAME, CLASS, SECTION and MARKS.

    For example,
    Example 1 - How many entries of records are present?
    The SQL command will be something like this:
    SELECT COUNT(*) FROM STUDENT;

    Example 2 - Tell me all the students studying in Data Science class?
    The SQL command will be something like this:
    SELECT * FROM STUDENT WHERE CLASS="Data Science";

    Also, the SQL code should not have ``` in the beginning or end and the word SQL in the output.
    Return only the SQL query. Do not include markdown, code fences, or explanations.
    """
]



## Streamlit App

st.set_page_config(page_title="I can Retrieve Any SQL query")

st.header("Gemini App To Retrieve SQL Data")

question = st.text_input("Input: ", key="input")

submit = st.button("Ask the question")

# If submit is clicked
if submit:
    response = get_gemini_response(question, prompt)
    print(response)
    data = read_sql_query(response, "student.db")

    st.subheader("The Response is")

    for row in data:
        print(row)
        st.write(row)