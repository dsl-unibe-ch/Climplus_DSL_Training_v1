"""How fast is your laptop? Warming trends for every country, on 1 core and on all cores.

    uv run python trends.py                 # measure this laptop (1-3 minutes)
    uv run python trends.py --country 17    # one country only: what a cluster job runs
    uv run python trends.py --collect       # combine the per-country results of a cluster run

The job: for each country, the warming trend 1951-2012 (degC per decade) with a
bootstrap 95% interval. Every country is independent of the others, so the job
can be split into one task per country.
"""
import argparse
import os
import sys
import time
from multiprocessing import Pool
from pathlib import Path

import numpy as np
import pandas as pd

FILE = "GlobalLandTemperaturesByCountry.csv"
NOT_COUNTRIES = {"Africa", "Asia", "Europe", "North America", "South America", "Oceania", "Antarctica"}
GRID_CELLS = 1440 * 721          # a global 0.25 degree grid, e.g. ERA5


def find_data():
    here = Path(__file__).resolve().parent
    for d in [Path("data"), here / "data", here.parent / "data", Path("../data"),
              here.parent / "01_Workflow_Git_AI" / "data"]:     # inside the course repository
        if (d / FILE).exists():
            return d / FILE
    sys.exit(f"Cannot find data/{FILE}. Run this from your course folder.")


def tasks(n_boot):
    df = pd.read_csv(find_data(), parse_dates=["dt"]).dropna(subset=["AverageTemperature"])
    df = df[df["dt"].dt.year.between(1951, 2012)]
    yearly = df.groupby(["Country", df["dt"].dt.year])["AverageTemperature"].agg(["mean", "size"])
    yearly = yearly[yearly["size"] == 12]["mean"].reset_index()      # complete years only
    out = []
    for name, g in yearly.groupby("Country"):
        if name in NOT_COUNTRIES or name.endswith("(Europe)") or len(g) < 50:
            continue
        out.append((name, g["dt"].to_numpy(float), g["mean"].to_numpy(), n_boot))
    return out


def trend(task):
    """Trend of one country, degC/decade, with a bootstrap 95% interval."""
    name, years, temps, n_boot = task
    rng = np.random.default_rng(0)
    slope = np.polyfit(years, temps, 1)[0]
    idx = rng.integers(0, len(years), size=(n_boot, len(years)))
    boot = np.array([np.polyfit(years[i], temps[i], 1)[0] for i in idx])
    lo, hi = np.percentile(boot, [2.5, 97.5])
    return name, 10 * slope, 10 * lo, 10 * hi


def duration(s):
    for unit, size in (("days", 86400), ("h", 3600), ("min", 60)):
        if s >= size:
            return f"{s / size:,.1f} {unit}"
    return f"{s:,.0f} s"


def measure(n_boot):
    jobs = tasks(n_boot)
    cores = os.cpu_count() or 1
    print(f"job: warming trend 1951-2012 for {len(jobs)} countries, {n_boot} bootstrap resamples each")
    print(f"this laptop: {cores} logical cores\n")

    t0 = time.perf_counter()
    serial = [trend(j) for j in jobs]
    t1 = time.perf_counter() - t0
    print(f" 1 core     {t1:6.1f} s")

    best_n, best_t = 1, t1
    for n in sorted({2, 4, 8, cores}):
        if n > cores or n == 1:
            continue
        t0 = time.perf_counter()
        with Pool(n) as pool:
            parallel = pool.map(trend, jobs)
        t = time.perf_counter() - t0
        print(f"{n:2d} workers  {t:6.1f} s   speed-up {t1 / t:4.1f}x   (ideal {n}x)")
        if t < best_t:
            best_n, best_t = n, t
    assert parallel == serial if cores > 1 else True, "parallel and serial results differ"

    per_task = t1 / len(jobs)
    print(f"\nsame job for every 0.25 degree grid cell ({GRID_CELLS:,} instead of {len(jobs)}):")
    print(f"   1 core of this laptop    {duration(per_task * GRID_CELLS)}")
    print(f"  {best_n:>2} cores of this laptop   {duration(per_task * GRID_CELLS * best_t / t1)}")
    print(f"  1,000 cluster cores       {duration(per_task * GRID_CELLS / 1000)}  (if it scaled perfectly)")

    print("\n>>> REPORT THIS LINE:")
    print(f"cores {cores} | 1 core {t1:.1f} s | best {best_t:.1f} s on {best_n} | speed-up {t1 / best_t:.1f}x")


def one_country(i, n_boot):
    """Array task i (1-based): one country, result written to results/<i>.csv."""
    jobs = tasks(n_boot)
    if not 1 <= i <= len(jobs):
        sys.exit(f"--country must be between 1 and {len(jobs)}")
    name, s, lo, hi = trend(jobs[i - 1])
    Path("results").mkdir(exist_ok=True)
    Path(f"results/{i:03d}.csv").write_text(f"{name},{s:.4f},{lo:.4f},{hi:.4f}\n", encoding="utf-8")
    print(f"{i}: {name} {s:+.2f} degC/decade [{lo:+.2f}, {hi:+.2f}]")


def collect():
    files = sorted(Path("results").glob("*.csv"))
    rows = [f.read_text(encoding="utf-8").strip().split(",") for f in files]
    df = pd.DataFrame(rows, columns=["country", "trend", "lo", "hi"]).astype({"trend": float, "lo": float, "hi": float})
    print(f"{len(df)} countries collected. Fastest warming (degC/decade, 95% interval):")
    for r in df.sort_values("trend", ascending=False).head(5).itertuples():
        print(f"  {r.country:<28} {r.trend:+.2f}  [{r.lo:+.2f}, {r.hi:+.2f}]")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--country", type=int, help="compute one country only (1-based), as a cluster array task")
    p.add_argument("--collect", action="store_true", help="combine results/*.csv from a cluster run")
    p.add_argument("--boot", type=int, default=5000, help="bootstrap resamples per country (default 5000)")
    a = p.parse_args()
    if a.collect:
        collect()
    elif a.country:
        one_country(a.country, a.boot)
    else:
        measure(a.boot)
