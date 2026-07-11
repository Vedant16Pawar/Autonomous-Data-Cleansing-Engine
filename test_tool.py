from backend.agent.tools import (
    inspect_dataframe,
    generate_cleaning_code,
    execute_generated_code_reliably,
    validate_output,
)

instruction = """
Remove duplicate rows.
Fill missing Age values with the median.
Convert Email to lowercase.
"""

inspect_result = inspect_dataframe.invoke(
    {
        "file_path": "sample.csv"
    }
)

code_result = generate_cleaning_code.invoke(
    {
        "schema_summary": inspect_result.summary,
        "user_instruction": instruction,
    }
)

execution_result = execute_generated_code_reliably.invoke(
    {
        "generated_code": code_result.generated_code,
        "user_instruction": instruction,
        "input_csv_path": "sample.csv",
    }
)

validation_result = validate_output.invoke(
    {
        "input_csv_path": "sample.csv",
        "output_csv_path": execution_result.output_path,
        "user_instruction": instruction,
    }
)

print("\n===== Validation Result =====\n")
print(type(validation_result))
print(validation_result)