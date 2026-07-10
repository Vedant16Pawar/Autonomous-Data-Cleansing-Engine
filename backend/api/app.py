from fastapi import FastAPI, UploadFile, File, HTTPException
import os
import uuid
import shutil

app = FastAPI(
    title="Autonomous Data Cleansing & Feature Engineering Engine",
    version="1.0.0",
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