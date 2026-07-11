from backend.agent.tools import (
    inspect_dataframe,
    execute_with_self_correction,
)

csv_path = "sample.csv"

summary = inspect_dataframe.invoke(
    {
        "file_path": csv_path
    }
)

result = execute_with_self_correction(
    schema_summary=summary,
    user_instruction="Extract the EmployeeSalary column.",
    input_csv_path=csv_path,
)

print("\n========== RESULT ==========")
print(result)