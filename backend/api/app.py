from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import json
import pandas as pd
import os
import uuid
import shutil
from pydantic import BaseModel

from backend.agent.agent import (
    agent_executor,
    explanation_chain,
)

class CleanRequest(BaseModel):
    file_id: str
    instruction: str

app = FastAPI(
    title="Autonomous Data Cleansing & Feature Engineering Engine",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Folder where uploaded CSVs will be stored
UPLOAD_DIR = "uploads"

# Create the folder if it doesn't already exist
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def health_check():
    return {
        "status": "healthy",
        "message": "Backend is running successfully."
    }


@app.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    """
    Upload a CSV file and save it locally with a unique UUID filename.
    """

    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are allowed."
        )

    # Generate a unique ID
    file_id = str(uuid.uuid4())

    # Example:
    # uploads/6e4db7c8-....csv
    file_path = os.path.join(
        UPLOAD_DIR,
        f"{file_id}.csv"
    )

    # Save uploaded file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "file_id": file_id
    }

@app.post("/clean")
async def clean_csv(request: CleanRequest):
    """
    Run the full cleansing pipeline:
    agent inspects → generates code → executes in Docker →
    validates → explains.
    """

    file_path = os.path.join(
        UPLOAD_DIR,
        f"{request.file_id}.csv"
    )

    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail="Uploaded file not found."
        )

    agent_input = (
        f"CSV Path:\n{file_path}\n\n"
        f"User Instruction:\n{request.instruction}"
    )

    try:
        agent_result = agent_executor.invoke(
            {"input": agent_input}
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Agent execution failed: {str(e)}",
        )

    # ---------------------------------------------------------
    # Parse the agent's final text output to extract results.
    # The raw output is a string; the structured data was
    # produced by the tools and referenced by the agent.
    # ---------------------------------------------------------

    agent_output = agent_result.get("output", "")

    # Attempt to extract structured fields from tool outputs
    # stored in intermediate_steps (if available).
    generated_code = ""
    output_path = None
    validation_warnings = []

    for step in agent_result.get("intermediate_steps", []):
        action, observation = step

        if action.tool == "execute_generated_code_tool":
            try:
                exec_data = json.loads(observation)
                generated_code = exec_data.get("generated_code", "")
                if exec_data.get("success"):
                    output_path = exec_data.get("output_path")
            except (json.JSONDecodeError, TypeError):
                pass

        elif action.tool == "validate_output_tool":
            try:
                val_data = json.loads(observation)
                validation_warnings = val_data.get("warnings", [])
            except (json.JSONDecodeError, TypeError):
                pass

    # ---------------------------------------------------------
    # Generate plain-English explanation via the LCEL chain.
    # ---------------------------------------------------------

    explanation = ""

    if generated_code:
        try:
            explanation = explanation_chain.invoke(
                {
                    "instruction": request.instruction,
                    "generated_code": generated_code,
                    "validation_warnings": (
                        "\n".join(validation_warnings)
                        if validation_warnings
                        else "No warnings."
                    ),
                }
            )
        except Exception:
            explanation = "Explanation generation failed."

    # ---------------------------------------------------------
    # Compute preview data for the frontend.
    # ---------------------------------------------------------

    input_row_count = len(pd.read_csv(file_path))
    output_row_count = (
        len(pd.read_csv(output_path))
        if output_path is not None
        else 0
    )
    output_preview_rows = (
        pd.read_csv(output_path).head(50).fillna("").to_dict(orient="records")
        if output_path is not None
        else []
    )

    # ---------------------------------------------------------
    # Return structured JSON with all four deliverables.
    # ---------------------------------------------------------

    user_friendly_code = generated_code
    if user_friendly_code:
        user_friendly_code = user_friendly_code.replace("/sandbox/input.csv", "input.csv")
        user_friendly_code = user_friendly_code.replace("/sandbox/output/output.csv", "cleaned_output.csv")

    return {
        "success": output_path is not None,
        "output_path": output_path,
        "generated_code": user_friendly_code,
        "explanation": explanation,
        "validation_warnings": validation_warnings,
        "input_row_count": input_row_count,
        "output_row_count": output_row_count,
        "output_preview_rows": output_preview_rows,
    }


@app.get("/preview/{file_id}")
async def preview_csv(file_id: str):
    """
    Return the first 10 rows of an uploaded CSV as JSON,
    plus row and column counts for the frontend.
    """
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}.csv")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found.")
    df = pd.read_csv(file_path)
    return {
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "columns": list(df.columns),
        "rows": df.head(50).fillna("").to_dict(orient="records"),
    }


@app.get("/download")
async def download_csv(path: str):
    """
    Serve a cleaned CSV file for download.
    """
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Output file not found.")
    return FileResponse(
        path,
        media_type="text/csv",
        filename="cleaned_output.csv",
    )