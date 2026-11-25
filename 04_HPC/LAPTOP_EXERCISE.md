# How fast is your laptop?

The same job as on the slide: the warming trend of every country, with a bootstrap
interval, first on 1 core, then on several. You need this morning's `clim-course`
folder with `data/GlobalLandTemperaturesByCountry.csv` in it.

**Plug in your charger.** On battery, most laptops slow themselves down.

## 1. Get the script and run it

In a terminal in `clim-course` (VS Code: **Terminal → New Terminal**):

```
curl.exe -LO https://raw.githubusercontent.com/dsl-unibe-ch/Climplus_DSL_Training_v1/main/04_HPC/trends.py
uv run python trends.py
```

(macOS/Linux: `curl` instead of `curl.exe`.) It takes 1 to 3 minutes. While it runs,
open Task Manager (Windows) or Activity Monitor (macOS) and watch the CPU.

## 2. Report your line

At the end it prints a line like this one:

```
cores 16 | 1 core 16.4 s | best 2.7 s on 16 | speed-up 6.1x
```

Send it in the chat or call it out.

## 3. Read your numbers

- With *n* workers, did it get *n* times faster? Where did it stop improving?
- How long would the same job take for every cell of a 0.25° grid, on your laptop?
- Your neighbour has a different laptop. Who was faster on 1 core? On all cores?

## 4. Write the cluster job

On a cluster you don't run the job, you queue it. Each country becomes its own
task. First time one task:

```
Measure-Command { uv run python trends.py --country 1 }     # Windows PowerShell
time uv run python trends.py --country 1                    # macOS/Linux
```

Then fill in the blanks in a new file `job.sh`:

```
#!/bin/bash
#SBATCH --job-name=trends
#SBATCH --time=________        # how long may ONE task run? (hh:mm:ss, with margin)
#SBATCH --mem=________         # memory for ONE task (e.g. 2G)
#SBATCH --array=1-___          # one task per country: how many countries?

uv run python trends.py --country $SLURM_ARRAY_TASK_ID
```

We will submit one of these on UBELIX together.

## Done early?

- `uv run python trends.py --boot 20000`: four times the work. Does the speed-up change?
- Run it on battery and compare.
