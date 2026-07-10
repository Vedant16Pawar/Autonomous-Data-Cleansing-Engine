"""
from backend.agent.tools import inspect_dataframe

file_path = "uploads/8680da78-b999-46f3-b473-e52f7a7a3825.csv"

summary = inspect_dataframe.invoke({"file_path": file_path})

print(summary)

"""
from dotenv import load_dotenv

load_dotenv()

from backend.agent.tools import generate_cleaning_code

schema_summary = """
Total Rows: 100
Total Columns: 3

Columns and Data Types:
- name: object
- age: float64
- email: object

Missing Values:
- name: 0
- age: 15
- email: 2

First 20 Rows:
(name, age, email ...)
"""

user_instruction = "Remove rows where age is null."

generated_code = generate_cleaning_code.invoke(
    {
        "schema_summary": schema_summary,
        "user_instruction": user_instruction,
    }
)

print("=" * 80)
print("GENERATED CODE")
print("=" * 80)
print(generated_code)