# Python Application

This repository contains a Python application.

## Requirements

- Python **3.9+**
- `pip` (comes with Python)

Check your Python version:
```bash
python --version
```

## Setup Virtual Environment

It is strongly recommended to use a virtual environment.

🪟 Windows (PowerShell)
```powershell
python -m venv venv
venv\Scripts\activate
```
🐧 Linux / macOS
```bash
python3 -m venv venv
source venv/bin/activate
```

## Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Run the Application
```bash
python ./src/main.py --path PATH
```

## Deactivate Virtual Environment
```bash
deactivate
```

