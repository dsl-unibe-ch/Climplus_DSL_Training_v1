# Climplus DSL Training v1

## Repository organisation

The repository is organised by training session: each session has its own folder containing the notebooks and any supporting material (data, images, exercises) for that session. Folder names start with the session's number in the programme, so they sort in timeline order.

```
Climplus_DSL_Training_v1/
├── NN_<Session Name>/         # one folder per training session, NN = place in the programme
│   ├── *.ipynb                # notebook(s) for the session
│   └── data/                  # session-specific data files (if any)
├── requirements.txt           # shared Python dependencies for all sessions
├── .env.example.              # example environment file
└── README.md                  # this file
```

### Programme

Numbered sessions have (or will have) a folder in this repository; the number is the start of the folder name.

#### Day 1, 1 December: best practice and foundations

| Time | No. | Session | Folder |
|---|---|---|---|
| 09:00 – 09:15 | | Intro session | |
| 09:15 – 10:15 | | Workshop on science integrity / FAIR principles | |
| 10:15 – 10:45 | | *break* | |
| 10:45 – 12:00 | 01 | Workflow management, Git, AI-assisted workflows | [`01_Workflow_Git_AI/`](01_Workflow_Git_AI/) |
| 12:00 – 13:00 | | *lunch* | |
| 13:00 – 14:00 | 02 | Workshop on dataset types and sources | |
| 14:00 – 15:00 | 03 | Computational research tools: GPUStack, OnDemand, TextLab | [`03_Computational_Research_Tools/`](03_Computational_Research_Tools/) |
| 15:00 – 15:30 | | *break* | |
| 15:30 – 17:00 | 04 | HPC hands-on | [`04_HPC/`](04_HPC/) |

#### Day 2, 2 December: programming and data processing (two parallel tracks)

**Beginner track** (no or very little prior programming experience)

| Time | No. | Session | Folder |
|---|---|---|---|
| 09:00 – 10:15 | 05 | Python basics | |
| 10:15 – 10:45 | | *break* | |
| 10:45 – 12:00 | 06 | NumPy, pandas | |
| 12:00 – 13:00 | | *lunch* | |
| 13:00 – 14:15 | 07 | Images, time series, and graphs | |
| 14:15 – 14:45 | | *break* | |
| 14:45 – 15:45 | 08 | LLM-based data processing, beginner | [`08_LLM_Data_Processing/beginner/`](08_LLM_Data_Processing/beginner/) |
| 15:45 – 16:00 | | Q&A and closing session | |

**Experienced track** (prior programming experience, not necessarily in Python)

| Time | No. | Session | Folder |
|---|---|---|---|
| 09:00 – 10:15 | 09 | Recap: Python basics, NumPy, pandas, images, time series, and graphs | |
| 10:15 – 10:45 | | *break* | |
| 10:45 – 12:00 | 10 | Data formats, NetCDF, HDF5, Zarr | |
| 12:00 – 13:00 | | *lunch* | |
| 13:00 – 14:15 | 08 | LLM-based data processing, advanced | [`08_LLM_Data_Processing/`](08_LLM_Data_Processing/) |
| 14:15 – 14:45 | | *break* | |
| 14:45 – 16:00 | | Q&A and closing session | |

- **Session folders** are self-contained: you can work through a session without needing files from other sessions.
- **Dependencies** are shared across all sessions and installed once from `requirements.txt` (see setup below). Exception: `01_Workflow_Git_AI/` uses its own `pyproject.toml` and `uv.lock` (see its `SETUP.md`); session 04 runs in the same environment.

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

