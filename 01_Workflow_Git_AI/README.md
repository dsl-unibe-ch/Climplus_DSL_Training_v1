# Workflow management, Git, AI-assisted workflows

CLIM+ Training, Day 1, 10:45–12:00 · Data Science Lab, University of Bern

## Getting started

Setup instructions: [`SETUP.md`](SETUP.md). The course folder is created with:

```powershell
mkdir clim-course
cd clim-course
curl.exe -LO https://raw.githubusercontent.com/dsl-unibe-ch/Climplus_DSL_Training_v1/main/01_Workflow_Git_AI/pyproject.toml
curl.exe -LO https://raw.githubusercontent.com/dsl-unibe-ch/Climplus_DSL_Training_v1/main/01_Workflow_Git_AI/uv.lock
uv sync
```

This session uses its own `pyproject.toml` and `uv.lock`, not the repository's
`requirements.txt`.

## Report what your agent said

Pick a nickname (not your real name). Open https://ntfy.sh/climplus-octef4924s3t in your
browser and post one line: your nickname, the model, and the warming your agent claimed, e.g.

```
Puffin | gpt-oss +1.4
```

It appears on the room's screen. Messages are public on that relay and deleted after 12 hours,
so send nothing else.

## After the agents: the notebook and the reference data

In a terminal in `clim-course`:

```powershell
curl.exe -LO https://raw.githubusercontent.com/dsl-unibe-ch/Climplus_DSL_Training_v1/main/01_Workflow_Git_AI/know_your_data.ipynb
curl.exe -L --create-dirs -o data/reference/kaggle_v2/GlobalTemperatures.csv https://raw.githubusercontent.com/dsl-unibe-ch/Climplus_DSL_Training_v1/main/01_Workflow_Git_AI/data/reference/kaggle_v2/GlobalTemperatures.csv
curl.exe -L --create-dirs -o data/reference/berkeley_2025/Complete_TAVG_complete.txt https://raw.githubusercontent.com/dsl-unibe-ch/Climplus_DSL_Training_v1/main/01_Workflow_Git_AI/data/reference/berkeley_2025/Complete_TAVG_complete.txt
curl.exe -L --create-dirs -o data/reference/berkeley_2025/Land_and_Ocean_complete.txt https://raw.githubusercontent.com/dsl-unibe-ch/Climplus_DSL_Training_v1/main/01_Workflow_Git_AI/data/reference/berkeley_2025/Land_and_Ocean_complete.txt
```

(macOS/Linux: `curl` instead of `curl.exe`.) Open `know_your_data.ipynb` in VS Code and
choose the `.venv` kernel (top right, **Select Kernel**).

## Before lunch: download Whisper for this afternoon

Session 3 (15:30) transcribes speech on your laptop. Over lunch, in a terminal in `clim-course`:

```powershell
curl.exe -LO https://raw.githubusercontent.com/dsl-unibe-ch/Climplus_DSL_Training_v1/main/04_HPC/whisper_laptop.py
uv run --group whisper python whisper_laptop.py --download
```

(macOS/Linux: `curl` instead of `curl.exe`.) About 250 MB; it ends with `Download done.`

## Notebook

- [`know_your_data.ipynb`](know_your_data.ipynb): what two AI agents did with one
  Berkeley Earth file, and what it takes to check their numbers.

## Data

`data/GlobalLandTemperaturesByCountry.csv`: monthly land temperature by country,
1743–2013.

- **Source:** Berkeley Earth (https://berkeleyearth.org), as released on Kaggle:
  *Climate Change: Earth Surface Temperature Data*, version 2
  (https://www.kaggle.com/datasets/berkeleyearth/climate-change-earth-surface-temperature-data).
- **Licence:** CC BY-NC-SA 4.0 (Kaggle release). Non-commercial use, with attribution;
  derivatives under the same licence.
- **Unmodified.** SHA-256
  `95d26615f8336585a5b92f340e08bc8c8bd8bc82fe6a0369f5abeb985a826fdf`.

Shared here so everyone in the course works with the identical file. For research,
get the current data from Berkeley Earth directly.

Reference series, used by the notebook to check the agents' numbers:

| file | what | source / licence |
|---|---|---|
| `data/reference/kaggle_v2/GlobalTemperatures.csv` | Berkeley Earth global land and land+ocean series, same Kaggle release | as above |
| `data/reference/berkeley_2025/` | current Berkeley Earth global land (`Complete_TAVG_complete.txt`) and land+ocean (`Land_and_Ocean_complete.txt`), downloaded 2026-11-23, data to Dec 2024 | https://berkeleyearth.org/data/ , CC BY-NC 4.0 |
