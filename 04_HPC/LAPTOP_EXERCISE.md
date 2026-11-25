# How fast is your laptop?

The same job as on the slide: the warming trend of every country, with a bootstrap
interval, first on 1 core, then on several. You need this morning's `clim-course`
folder with `data/GlobalLandTemperaturesByCountry.csv` in it.

**Plug in your charger.** On battery, most laptops slow themselves down.

## 0. Download Whisper (at lunch on day 1)

It fetches about 250 MB (programs plus the speech model). Do it over lunch, not
during the session, when 25 laptops share the Wi-Fi. In a terminal in `clim-course` (VS Code: **Terminal → New Terminal**):

```
curl.exe -LO https://raw.githubusercontent.com/dsl-unibe-ch/Climplus_DSL_Training_v1/main/04_HPC/whisper_laptop.py
uv run --group whisper python whisper_laptop.py --download
```

(macOS/Linux: `curl` instead of `curl.exe`.) It ends with `Download done.`
Windows laptops with an ARM processor (e.g. Snapdragon) cannot install it: team up with a neighbour.

## 1. Get the script and run it

**Leaderboard (optional):** pick a nickname, not your real name, and save it as a file
`nickname.txt` in `clim-course`. Then add `--send` to the commands below. Only the result line
and your nickname are sent (to ntfy.sh, a public relay; deleted after 12 hours). Without
`--send`, nothing leaves your laptop.

In the same terminal:

```
curl.exe -LO https://raw.githubusercontent.com/dsl-unibe-ch/Climplus_DSL_Training_v1/main/04_HPC/trends.py
uv run python trends.py --send
```

(macOS/Linux: `curl` instead of `curl.exe`.) It takes 1 to 3 minutes. While it runs,
open Task Manager (Windows) or Activity Monitor (macOS) and watch the CPU.

## 2. Report your line

At the end it prints a line like this one:

```
cores 16 | 1 core 16.4 s | best 2.7 s on 16 | speed-up 6.1x
```

If you ran with `--send`, it is already on the leaderboard. Otherwise post it in the chat.

## 3. Transcribe speech on your laptop

The demo from the start of the session, on your own CPU: two minutes of a 1975 climate report, read aloud.

```
uv run --group whisper python whisper_laptop.py --send
```

It prints a line like this one (with `--send`, it also goes to the leaderboard):

```
whisper base | cores 8 | 2.0 min in 9.1 s | 13x real time | 2.1% words differ
```

"words differ" compares your transcript with the one the largest model (large-v3) made on a GPU.
Then try the smallest model: `uv run --group whisper python whisper_laptop.py --model tiny`.
Faster? More wrong? Open the two `climate_clip_120s.*.txt` files and look at what changed.

## 4. Read your numbers

- With *n* workers, did it get *n* times faster? Where did it stop improving?
- How long would the same job take for every cell of a 0.25° grid, on your laptop?
- At your Whisper speed, how long would 200 hours of interviews take? Is `tiny` good enough for them?
- Your neighbour has a different laptop. Who was faster on 1 core? On all cores?

## 5. Write the cluster job

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
- `uv run --group whisper python whisper_laptop.py --model small` (480 MB more download): how much slower, how much better?
