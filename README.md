# Climplus DSL Training v1

## Repository organisation

The repository is organised by training session: each session has its own folder containing the notebooks and any supporting material (data, images, exercises) for that session.

```
Climplus_DSL_Training_v1/
├── <Session Name>/            # one folder per training session
│   ├── *.ipynb                # notebook(s) for the session
│   └── data/                  # session-specific data files (if any)
├── requirements.txt           # shared Python dependencies for all sessions
├── .env.example.              # example environment file
└── README.md                  # this file
```

- **Session folders** are self-contained: you can work through a session without needing files from other sessions.
- **Dependencies** are shared across all sessions and installed once from `requirements.txt` (see setup below).

## Local Environment Setup

This project uses [uv](https://docs.astral.sh/uv/) to manage the Python environment, with dependencies pinned in `requirements.txt`.

Follow the instructions for your operating system.

---

### macOS / Linux

#### 1. Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Alternatively, with Homebrew (macOS):

```bash
brew install uv
```

Verify the installation:

```bash
uv --version
```

#### 2. Create a virtual environment

From the project root:

```bash
uv venv
```

This creates a virtual environment in `.venv/`. To use a specific Python version:

```bash
uv venv --python 3.14
```

#### 3. Activate the environment

```bash
source .venv/bin/activate
```

#### 4. Install dependencies from requirements.txt

```bash
uv pip install -r requirements.txt
```

#### 5. Verify

```bash
uv pip list
```

---

### Windows

#### 1. Install uv

In PowerShell:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Verify the installation:

```powershell
uv --version
```

#### 2. Create a virtual environment

From the project root:

```powershell
uv venv
```

This creates a virtual environment in `.venv\`. To use a specific Python version:

```powershell
uv venv --python 3.12
```

#### 3. Activate the environment

```powershell
.venv\Scripts\Activate.ps1
```

If activation is blocked by the execution policy, run this first:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### 4. Install dependencies from requirements.txt

```powershell
uv pip install -r requirements.txt
```

#### 5. Verify

```powershell
uv pip list
```

---

### Environment File
Create a copy of the .env.example file with
```
cp .env.example .env
```
Populate the environment variables (follow instructions by facilitator)

