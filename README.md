# 🧹 Autonomous Data Cleansing Engine

An end-to-end AI-powered data cleaning platform that lets users upload messy CSV files, describe transformations in plain English, and receive a cleaned dataset — all without writing a single line of code.

The system uses a **LangChain autonomous agent** backed by **Groq's LLaMA 3.3 70B** model to inspect the data, generate a custom Python cleaning script, execute it inside an **isolated Docker sandbox**, validate the results, and present a side-by-side comparison of the original vs. cleaned data with a plain-English explanation of every change made.

**Built with:** Python · FastAPI · LangChain · Groq · Docker · React · Vite

---

## 📽️ Demo Video

**Download and watch the demo:**

[https://github.com/Vedant16Pawar/Autonomous-Data-Cleansing-Engine/releases/download/v1.0/demo.mp4]

---

## ✨ Features

- 🗣️ **Natural Language Instructions** — Describe your cleaning task in plain English, no code or formulas required.
- 🤖 **LLM-Powered Code Generation** — An autonomous AI agent inspects your data and writes custom Python cleaning scripts.
- 🔒 **Sandboxed Execution** — All generated code runs inside isolated Docker containers with zero risk to your system.
- 📊 **Side-by-Side Preview** — Compare the original dataset against the cleaned version in an interactive table.
- 📈 **Summary Metrics** — Instantly see row counts, removed entries, and validation warnings.
- 💡 **Plain-English Explanation** — Every transformation is explained in human-readable language.
- 🧾 **Generated Code Viewer** — View the exact Python code the AI wrote, with syntax highlighting and a copy button.
- ⬇️ **One-Click Download** — Download your cleaned CSV file instantly.
- ⚠️ **Smart Validation** — Automatic checks for data loss, type mismatches, and structural integrity.

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                          USER'S BROWSER                              │
│                                                                      │
│   ┌──────────────────────────────────────────────────────────────┐   │
│   │              React Frontend                                  │   │
│   │                                                              │   │
│   │   Upload CSV  →  Type Instructions  →  View Results          │   │
│   └──────────────────────────┬───────────────────────────────────┘   │
│                              │ HTTPS                                 │
└──────────────────────────────┼───────────────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────────────┐
│                      Cloud Server (EC2 / VM)                         │
│                                                                      │
│   ┌────────────────────┐    ┌────────────────────────────────────┐   │
│   │   Nginx + SSL      │───▶│   FastAPI Backend (Docker)         │   │
│   │   (Let's Encrypt)  │    │                                    │   │
│   └────────────────────┘    │   ┌────────────────────────────┐   │   │
│                              │   │     LangChain Agent        │   │   │
│                              │   │                            │   │   │
│                              │   │  1. inspect_dataframe      │   │   │
│                              │   │  2. generate_cleaning_code │   │   │
│                              │   │  3. execute_generated_code │   │   │
│                              │   │  4. validate_output        │   │   │
│                              │   └─────────────┬──────────────┘   │   │
│                              │                 │                  │   │
│                              └─────────────────┼──────────────────┘   │
│                                                │ Docker Socket        │
│                                                ▼                     │
│                              ┌────────────────────────────────────┐   │
│                              │   Sandbox Container (Isolated)     │   │
│                              │                                    │   │
│                              │   • No network access              │   │
│                              │   • Read-only filesystem           │   │
│                              │   • 256 MB memory limit            │   │
│                              │   • 10 second timeout              │   │
│                              │   • Runs generated Python code     │   │
│                              └────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 🔧 Tech Stack

**Backend:** Python 3.12 · FastAPI · LangChain · Groq (LLaMA 3.3 70B) · Docker · Pandas · NumPy

**Frontend:** React 18 · Vite · Vanilla CSS (custom dark-theme design system)

**Infrastructure:** Docker Compose · Nginx · Let's Encrypt (Certbot)

---

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- Node.js 18+ and npm
- Docker and Docker Compose
- Groq API Key — get one free at [console.groq.com](https://console.groq.com/)

### 1. Clone the Repository

```bash
git clone https://github.com/Vedant16Pawar/Autonomous-Data-Cleansing-Engine.git
cd Autonomous-Data-Cleansing-Engine
```

### 2. Set Up Environment Variables

```bash
cp .env.example .env
```

Open `.env` and add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### 3. Build and Run the Backend

```bash
# Build the sandbox image (required for code execution)
docker build -t data-cleaning-sandbox -f docker/Dockerfile.sandbox .

# Start the backend with Docker Compose
docker compose up -d --build
```

Verify the backend is running:

```bash
curl http://localhost:8080
# Expected: {"status":"healthy","message":"Backend is running successfully."}
```

### 4. Start the Frontend

```bash
cd frontend
npm install
npm run dev
```

Open your browser and navigate to `http://localhost:5173`

---

## 📁 Project Structure

```
Autonomous-Data-Cleansing-Engine/
│
├── backend/
│   ├── Dockerfile                   # Backend container image
│   ├── agent/
│   │   ├── agent.py                 # LangChain agent orchestration
│   │   ├── llm.py                   # Shared Groq LLM client
│   │   ├── schemas.py               # Pydantic data models for tool I/O
│   │   └── tools.py                 # 4 agent tools (inspect, generate, execute, validate)
│   ├── api/
│   │   └── app.py                   # FastAPI routes (/upload, /clean, /preview, /download)
│   └── sandbox/
│       └── executor.py              # Docker SDK integration for sandboxed execution
│
├── docker/
│   └── Dockerfile.sandbox           # Minimal Python image for safe code execution
│
├── frontend/
│   └── src/
│       ├── api/
│       │   └── client.js            # Axios HTTP client
│       ├── components/
│       │   ├── UploadZone.jsx       # Drag-and-drop CSV upload
│       │   ├── DataPreview.jsx      # Side-by-side before/after tables
│       │   ├── InstructionInput.jsx # Natural language input box
│       │   ├── ProgressStepper.jsx  # 4-step pipeline progress indicator
│       │   ├── SummaryMetrics.jsx   # Row count & warning metric cards
│       │   ├── CodeViewer.jsx       # Syntax-highlighted code display
│       │   ├── Explanation.jsx      # AI-generated explanation card
│       │   └── Warnings.jsx         # Validation warning alerts
│       ├── App.jsx                  # Main application component
│       └── index.css                # Global dark-theme design system
│
├── docker-compose.yml               # Backend + Docker socket orchestration
├── requirements.txt                 # Python dependencies
└── .env.example                     # Environment variable template
```

---

## ⚙️ How It Works

The engine uses an autonomous LangChain agent that orchestrates 4 specialized tools in sequence:

**Step 1 — Inspect Data**
Reads the uploaded CSV and generates a structured summary (column names, data types, missing values, preview rows). This gives the LLM full context about the dataset before writing any code.

**Step 2 — Generate Code**
The LLM receives the data summary along with the user's natural language instructions and writes a custom Python script using pandas and numpy. The prompt includes safety guardrails to prevent destructive operations like accidentally deleting all rows.

**Step 3 — Execute in Sandbox**
The generated script runs inside an isolated Docker container with no network access, a read-only filesystem, 256 MB memory limit, and a 10-second timeout. Only pandas and numpy are available inside the sandbox.

**Step 4 — Validate Output**
Compares the input and output datasets to check for unexpected column changes, significant row loss, data type mismatches, and empty output files. Any issues are surfaced as warnings to the user.

---

## 🧪 Example Queries

Here are some natural language instructions you can try:

| Instruction | What It Does |
|:---|:---|
| `Remove duplicate rows` | Drops exact duplicate entries across all columns |
| `Fill missing Age values with the median` | Replaces NaN values in the Age column with the column median |
| `Normalize email addresses to lowercase` | Converts all email strings to lowercase |
| `Remove rows where Salary is less than 0` | Filters out rows with negative salary values |
| `Convert Date column to datetime format` | Parses string dates into proper datetime objects |
| `Drop columns with more than 50% missing values` | Removes columns that are mostly empty |
| `Trim whitespace from all string columns` | Strips leading/trailing spaces from text data |

---

## 🛡️ Security

- **Sandboxed Execution** — All AI-generated code runs in isolated Docker containers with no network, no filesystem writes, and strict resource limits.
- **CORS Protection** — Backend only accepts requests from whitelisted frontend origins.
- **HTTPS Encryption** — All traffic between frontend and backend is encrypted via TLS/SSL.
- **No Data Persistence** — Uploaded files are stored temporarily and cleaned up after processing.

---

## 🗺️ Roadmap

- [x] Natural language data cleaning with LLM agent
- [x] Sandboxed Docker execution
- [x] Side-by-side data comparison UI
- [x] Cloud deployment with HTTPS
- [ ] Support for Excel (.xlsx) and JSON file formats
- [ ] Multi-step conversation memory for iterative cleaning
- [ ] Data visualization and profiling dashboard
- [ ] Batch processing for multiple files
- [ ] Custom cleaning templates and presets

---

## 📬 Contact

**Vedant Pawar** — [GitHub](https://github.com/Vedant16Pawar)
