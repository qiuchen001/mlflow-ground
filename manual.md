# MLflow Custom UI User Manual

## Introduction
This is a custom UI for MLflow, built with Vue 3 and FastAPI. It provides a modern, clean interface to view your MLflow experiments and runs.

## Prerequisites
- Python 3.8+
- Node.js 16+
- An existing MLflow server running at `http://127.0.0.1:5002` (or update `backend/main.py` to point to your server).

## Installation

1. **Backend Setup**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   ```

## Running the Application

1. **Start the Backend**
   ```bash
   cd backend
   python -m uvicorn main:app --reload --port 8001
   ```
   The backend will be available at `http://127.0.0.1:8001`.

2. **Start the Frontend**
   ```bash
   cd frontend
   npm run dev
   ```
   The frontend will be available at `http://localhost:5173` (or the port shown in the terminal).

## Usage

1. Open the frontend URL in your browser.
2. **Sidebar**: You will see a list of experiments on the left. Click on an experiment to select it.
3. **Main View**: Once an experiment is selected, the main view will show a table of runs for that experiment.
4. **Run Details**: Click on any row in the run table to view detailed metrics and parameters for that run.

## Troubleshooting
- **Backend Port Conflict**: If port 8001 is in use, change the port in the `uvicorn` command and update `frontend/src/services/api.js`.
- **MLflow Connection**: Ensure your MLflow server is running and accessible. The backend defaults to `http://127.0.0.1:5002`.
