import re
import pandas as pd
import json

from langchain.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from backend.sandbox import run_code_in_docker
from backend.agent.schemas import (
    InspectResult,
    CodeGenerationResult,
    ExecutionResult,
    ValidationResult,
)
from backend.agent.llm import llm



def inspect_dataframe(file_path: str) -> InspectResult:
    """
    Read a CSV file and return a structured summary
    for downstream tools.
    """

    df = pd.read_csv(file_path)

    total_rows = len(df)
    total_columns = len(df.columns)

    column_names = list(df.columns)

    column_dtypes = {
        column: str(dtype)
        for column, dtype in df.dtypes.items()
    }

    missing_values = {
        column: int(count)
        for column, count in df.isnull().sum().items()
    }

    preview = df.head(10).to_string()

    summary_lines = [
      f"Total Rows: {total_rows}",
      f"Total Columns: {total_columns}",
      "",
      "Columns and Data Types:",
    ]

    for column, dtype in column_dtypes.items():
        summary_lines.append(f"- {column}: {dtype}")

    summary_lines.append("")
    summary_lines.append("Missing Values:")

    for column, count in missing_values.items():
        summary_lines.append(f"- {column}: {count}")

    summary_lines.append("")
    summary_lines.append("First 10 Rows:")
    summary_lines.append(preview)

    summary = "\n".join(summary_lines)

    return InspectResult(
        total_rows=total_rows,
        total_columns=total_columns,
        column_names=column_names,
        column_dtypes=column_dtypes,
        missing_values=missing_values,
        preview=preview,
        summary=summary,
    )



def generate_cleaning_code(
    schema_summary: str,
    user_instruction: str,
    ) -> CodeGenerationResult:
    """
    Generate Python pandas code that cleans a CSV according to
    the user's instruction.
    """

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
                You are an expert Python data engineer.

                Write ONLY executable Python code.

                Rules:
                1. Read the dataset from '/sandbox/input.csv'
                2. Save the cleaned dataset to '/sandbox/output/output.csv'
                3. Perform ONLY the transformation requested by the user. If the user's instruction is conversational, a greeting (e.g., "hi", "hello", "hey"), or does not ask for any changes/modifications to the dataset, write a Python script that simply reads the dataset and saves it to the output path without making ANY changes or transformations to the data.
                4. Import ONLY:
                - pandas
                - numpy
                - re
                5. Do NOT print explanations.
                6. Do NOT use markdown.
                7. Do NOT wrap the code inside ```python or ``` fences.
                8. The final script must be directly executable.
                """,
            ),
            (
                "human",
                """
                Dataset Summary:

                {schema_summary}

                User Instruction:

                {user_instruction}
                """,
            ),
        ]
    )

    parser = StrOutputParser()

    # LCEL Chain
    chain = prompt | llm | parser

    generated_code = chain.invoke(
        {
            "schema_summary": schema_summary,
            "user_instruction": user_instruction,
        }
    )

    # Remove markdown fences if the model adds them anyway
    generated_code = re.sub(
        r"^```(?:python)?\s*",
        "",
        generated_code.strip(),
        flags=re.IGNORECASE,
    )

    generated_code = re.sub(
        r"\s*```$",
        "",
        generated_code,
    )

    return CodeGenerationResult(
        generated_code=generated_code
    )



def fix_generated_code(
    original_code: str,
    user_instruction: str,
    stderr: str,
    ) -> str:
    """
    Fix previously generated Python code using the execution error.
    Returns ONLY corrected executable Python code.
    """

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
                You are an expert Python data engineer.

                The previous Python script failed.

                Your task is to FIX it.

                Rules:

                1. Return ONLY executable Python code.
                2. Do NOT explain anything.
                3. Do NOT use markdown.
                4. Do NOT wrap code inside ``` fences.
                5. Read input from:
                /sandbox/input.csv
                6. Save output to:
                /sandbox/output/output.csv
                7. Import ONLY:
                pandas
                numpy
                re
                8. Preserve the user's requested transformation.
                """,
            ),
            (
                "human",
                """
                User Instruction:

                {instruction}

                Previous Code:

                {code}

                Execution Error:

                {stderr}
                """,
            ),
        ]
    )

    parser = StrOutputParser()

    chain = prompt | llm | parser

    fixed_code = chain.invoke(
        {
            "instruction": user_instruction,
            "code": original_code,
            "stderr": stderr,
        }
    )

    fixed_code = re.sub(
        r"^```(?:python)?\s*",
        "",
        fixed_code.strip(),
        flags=re.IGNORECASE,
    )

    fixed_code = re.sub(
        r"\s*```$",
        "",
        fixed_code,
    )

    return fixed_code

def _execute_generated_code_once(
    code: str,
    input_csv_path: str,
    ) -> dict:
    """
    Execute LLM-generated Python code inside the Docker sandbox exactly once.

    Parameters
    ----------
    code : str
        Python code generated by the LLM.

    input_csv_path : str
        Path to the uploaded CSV file on the host machine.

    Returns
    -------
    dict
        {
            "success": bool,
            "output_path": str | None,
            "stdout": str,
            "stderr": str,
            "exit_code": int,
            "execution_time": float
        }
    """

    return run_code_in_docker(
        code=code,
        input_csv_path=input_csv_path,
    )


def validate_output(
    input_csv_path: str,
    output_csv_path: str,
    user_instruction: str,
    ) -> ValidationResult:
    """
    Validate the cleaned dataset against the original dataset.

    Returns a ValidationResult containing any validation warnings.
    """

    warnings = []

    input_df = pd.read_csv(input_csv_path)
    output_df = pd.read_csv(output_csv_path)

    # -------------------------------------------------
    # Row Count Validation
    # -------------------------------------------------

    original_rows = len(input_df)
    cleaned_rows = len(output_df)

    if original_rows > 0:

        retained_ratio = cleaned_rows / original_rows

        instruction = user_instruction.lower()

        expected_large_drop = any(
            keyword in instruction
            for keyword in [
                "filter",
                "remove",
                "drop",
                "delete",
                "dedup",
                "duplicate",
                "unique",
            ]
        )

        if retained_ratio < 0.5 and not expected_large_drop:
            warnings.append(
                f"Row count decreased from {original_rows} "
                f"to {cleaned_rows} "
                "(more than 50%). Verify this was intentional."
            )

    # -------------------------------------------------
    # Column Validation
    # -------------------------------------------------

    original_columns = set(input_df.columns)
    output_columns = set(output_df.columns)

    missing_columns = sorted(original_columns - output_columns)

    if len(missing_columns) > len(original_columns) / 2:
        warnings.append(
            f"More than half of the original columns are missing. "
            f"Missing columns: {missing_columns}"
        )

    return ValidationResult(
        warnings=warnings
    )


def execute_with_self_correction(
    generated_code: str,
    user_instruction: str,
    input_csv_path: str,
    max_attempts: int = 3,
    ) -> ExecutionResult:
    """
    Execute generated code and automatically repair
    execution failures using the LLM.

    Returns an ExecutionResult.
    """

    code = generated_code
    last_result = None

    for attempt in range(1, max_attempts + 1):

        print(f"\n========== Attempt {attempt} ==========\n")

        result = _execute_generated_code_once(
            code=code,
            input_csv_path=input_csv_path,
        )
        

        if result["success"]:

            return ExecutionResult(
                success=True,
                generated_code=code,
                output_path=result["output_path"],
                stdout=result["stdout"],
                stderr=result["stderr"],
                exit_code=result["exit_code"],
                execution_time=result["execution_time"],
                attempts=attempt,
                message="Execution completed successfully.",
            )

        last_result = result

        if attempt == max_attempts:
            break

        fix_result = fix_generated_code(
            original_code=code,
            user_instruction=user_instruction,
            stderr=result["stderr"],
        )

        code = fix_result

    return ExecutionResult(
        success=False,
        generated_code=code,
        output_path=None,
        stdout=last_result["stdout"],
        stderr=last_result["stderr"],
        exit_code=last_result["exit_code"],
        execution_time=last_result["execution_time"],
        attempts=max_attempts,
        message="Failed after maximum self-correction attempts.",
    )


def execute_generated_code_reliably(
    generated_code: str,
    user_instruction: str,
    input_csv_path: str,
    ) -> ExecutionResult:
    """
    Execute generated Python code inside the Docker sandbox.
    If execution fails, automatically repair the code using the LLM
    and retry up to 3 attempts.
    """

    return execute_with_self_correction(
        generated_code=generated_code,
        user_instruction=user_instruction,
        input_csv_path=input_csv_path,
    )





@tool
def inspect_dataframe_tool(file_path: str) -> str:
    """
    Inspect a CSV file and return a structured summary of its schema.

    Call this FIRST with the CSV file path.

    Args:
        file_path: Absolute or relative path to the CSV file.

    Returns:
        A text summary containing: total rows, total columns,
        column names with data types, missing value counts per column,
        and a preview of the first 20 rows.
        Pass this summary as 'schema_summary' to generate_cleaning_code_tool.
    """

    result = inspect_dataframe(file_path)

    return result.summary

@tool
def generate_cleaning_code_tool(
    schema_summary: str,
    user_instruction: str,
) -> str:
    """
    Generate executable Python pandas code that cleans a CSV dataset.

    Call this SECOND, after inspect_dataframe_tool.

    Args:
        schema_summary: The text summary returned by inspect_dataframe_tool.
        user_instruction: The original natural-language cleaning instruction
                          provided by the user.

    Returns:
        A string of executable Python code.
        Pass this code as 'generated_code' to execute_generated_code_tool.
    """

    result = generate_cleaning_code(
        schema_summary=schema_summary,
        user_instruction=user_instruction,
    )

    return result.generated_code

@tool
def execute_generated_code_tool(
    generated_code: str,
    user_instruction: str,
    input_csv_path: str,
) -> str:
    """
    Execute Python code inside a secure Docker sandbox with automatic
    self-correction on failure (up to 3 attempts).

    Call this THIRD, after generate_cleaning_code_tool.

    Args:
        generated_code: The Python code string returned by
                        generate_cleaning_code_tool.
        user_instruction: The original user cleaning instruction.
        input_csv_path: Path to the uploaded CSV file.

    Returns:
        A JSON string with keys: success (bool), generated_code (str),
        output_path (str or null), stdout, stderr, exit_code, attempts,
        and message.
        If success is true, use output_path for validate_output_tool.
    """

    result = execute_generated_code_reliably(
        generated_code=generated_code,
        user_instruction=user_instruction,
        input_csv_path=input_csv_path,
    )

    if result.success:
        return json.dumps({
            "success": True,
            "generated_code": result.generated_code,
            "output_path": result.output_path,
            "attempts": result.attempts,
            "message": "Code executed successfully."
        })
    else:
        return result.model_dump_json()

@tool
def validate_output_tool(
    input_csv_path: str,
    output_csv_path: str,
    user_instruction: str,
) -> str:
    """
    Validate the cleaned CSV against the original dataset.

    Call this FOURTH (final step), after execute_generated_code_tool
    succeeds.

    Args:
        input_csv_path: Path to the original uploaded CSV.
        output_csv_path: The output_path from execute_generated_code_tool.
        user_instruction: The original user cleaning instruction.

    Returns:
        A JSON string with key 'warnings' (list of strings).
        Empty list means the output passed all checks.
    """

    result = validate_output(
        input_csv_path=input_csv_path,
        output_csv_path=output_csv_path,
        user_instruction=user_instruction,
    )

    return result.model_dump_json()