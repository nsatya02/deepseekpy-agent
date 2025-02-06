import sys
from io import StringIO
from groq import Groq
import re
import os
import pandas as pd
import numpy as np

def clean_code_response(response):
    response = re.sub(r'<think>.*?</think>','',response, flags=re.DOTALL)
    code_match=re.search(r'```python\n(.*?)```',response, flags=re.DOTALL)
    if code_match:
        return code_match.group(1).strip()
    return response.strip()

def generate_code(question,data=None, data_context=""):
    client= Groq(api_key="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")
    system_prompt = """ generate python code that:
    -Uses only provided variables
    -prints results
    -Inculde any needed imports"""
    user_message= f"{data_context}\n Available variables: {list(data.keys()) if data else []}\n\n Task: {question}"

    chat_completion = client.chat.completions.create(
        messages=[
            {"role":"system", "content":system_prompt},
            {"role":"user","content": user_message}
        ],
        model = "deepseek-r1-distill-llama-70b"
    )

    response = chat_completion.choices[0].message.content
    return clean_code_response(response)
task=input("Enter your task: ")
res = generate_code(task, data_context="")
print(res)

def execute_python(code, data=None):
    old_stdout= sys.stdout
    sys.stdout= StringIO()
    local_vars= data or {}
    
    try:
        exec(code,local_vars)
        output = sys.stdout.getvalue()
        return {"output": output,"error":None,"results": local_vars}
    except Exception as e:
        return {"output": None,"error":str(e),"results": local_vars}
    finally:
        sys.stdout = old_stdout

def agent(question, data=None, data_context=""):
    solution= generate_code(question, data, data_context)
    print("Generated code:", solution)
    result=execute_python(solution,data)
    print("\n execution results:")
    if result['error']:
        print(f"Error: {result['error']}")
    else:
        print(result['output'])
    return solution, result

np.random.seed(42)

# Generate a series of dates (one year)
dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')

# Create a DataFrame with simulated data
df = pd.DataFrame({
    'date': dates,
    'category': np.random.choice(['Electronics', 'Clothing', 'Food', 'Books'], size=len(dates)),
    'store_id': np.random.choice(['Store_' + str(i) for i in range(1, 6)], size=len(dates)),
    'sales': np.random.normal(1000, 200, size=len(dates)),
    'temperature': np.random.normal(20, 5, size=len(dates)),
    'weekend': dates.dayofweek >= 5
})

# Introduce some relationships in the data
df['sales'] = df['sales'] * (1.2 * df['weekend'])  # Higher sales on weekends
df.loc[df['category'] == 'Electronics', 'sales'] *= 1.5  # Electronics tend to have higher sales
df['sales'] = df['sales'].abs().round(2)  # Ensure sales are positive and round the values

# Define the analytical task for sales analysis using pandas.
# This is just an  example, if you want to train an machine learning model you can mention in the question and execute.
question = "Analyze sales patterns: calculate total sales by category and show if weekends have higher average sales"
context = """DataFrame 'df' contains columns:
- date: daily dates for 2023
- category: product category (Electronics, Clothing, Food, Books)
- store_id: store identifier
- sales: daily sales amount
- temperature: daily temperature
- weekend: boolean flag indicating weekends
"""

# Invoke the agent with the question, the simulated DataFrame, and the data context.
solution, result = agent(question=question, data={'df': df}, data_context=context)
