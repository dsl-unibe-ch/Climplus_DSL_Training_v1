"""Session 3 hands-on: transcribe two minutes of speech on YOUR laptop's CPU.

    uv run --group whisper python whisper_laptop.py --download   # once, fetches ~200 MB
    uv run --group whisper python whisper_laptop.py              # the measurement
    uv run --group whisper python whisper_laptop.py --send       # ...and post it to the leaderboard

Prints one line to report, like:
    whisper base | cores 8 | 2.0 min in 9.1 s | 13x real time | 2.1% words differ

"words differ" compares your transcript with one made by the largest model
(large-v3) on a GPU. Faster is not the same as right: try --model tiny.
"""
import argparse
import difflib
import os
import re
import sys
import time
import urllib.request
from pathlib import Path

os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS_WARNING", "1")

RAW = "https://raw.githubusercontent.com/dsl-unibe-ch/Climplus_DSL_Training_v1/main/04_HPC/"
HERE = Path(__file__).resolve().parent
# LibriVox reading of "Understanding Climatic Change" (US NRC, 1975), chapter 1, first 2 minutes.
# Public domain: https://archive.org/details/understanding_climatic_change_1903_librivox
AUDIO = HERE / "climate_clip_120s.mp3"
REFERENCE = HERE / "climate_clip_120s.reference.txt"


# --send: post the report line to the room's leaderboard (off unless you ask).
# Only the line and the nickname in nickname.txt are sent; nothing else about you or your laptop.
TOPIC = "https://ntfy.sh/climplus-octef4924s3t"


def send(line):
    import urllib.request
    file = Path("nickname.txt")                  # in the folder you run from
    nick = file.read_text(encoding="utf-8").strip()[:24] if file.exists() else ""
    nick = " ".join(nick.replace("|", "/").split())    # one line, no separators
    msg = f"{nick} | {line}" if nick else line
    try:
        urllib.request.urlopen(urllib.request.Request(TOPIC, data=msg.encode("utf-8")), timeout=10)
        print(f"sent to the leaderboard{' as ' + nick if nick else ' (no nickname.txt: anonymous)'}")
    except Exception as e:
        print(f"could not send ({e}); report the line by hand")


def fetch(path):
    if not path.exists():
        print(f"downloading {path.name} ...")
        urllib.request.urlretrieve(RAW + path.name, path)


def words(text):
    return re.findall(r"[a-z0-9']+", text.lower())


def percent_differ(mine, ref):
    a, b = words(ref), words(mine)
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    wrong = sum(max(i2 - i1, j2 - j1) for op, i1, i2, j1, j2 in sm.get_opcodes() if op != "equal")
    return 100 * wrong / len(a)


p = argparse.ArgumentParser()
p.add_argument("--model", default="base", help="tiny (75 MB), base (145 MB), small (480 MB)")
p.add_argument("--download", action="store_true", help="only download audio and model, then stop")
p.add_argument("--send", action="store_true", help="also post the report line to the room's leaderboard")
a = p.parse_args()

try:
    from faster_whisper import WhisperModel, decode_audio
except ImportError:
    print("faster-whisper is not installed. Run with:  uv run --group whisper python whisper_laptop.py\n"
          "(On Windows laptops with an ARM processor it cannot be installed: team up with a neighbour.)")
    sys.exit(1)

fetch(AUDIO)
fetch(REFERENCE)
cores = os.cpu_count() or 4
print(f"loading model '{a.model}' (downloaded the first time) ...")
t0 = time.perf_counter()
model = WhisperModel(a.model, device="cpu", compute_type="int8", cpu_threads=cores)
print(f"model ready in {time.perf_counter() - t0:.1f} s")
if a.download:
    print("Download done. You are ready for the exercise.")
    sys.exit(0)

audio = decode_audio(str(AUDIO), sampling_rate=16000)
clip = len(audio) / 16000
print(f"transcribing {clip / 60:.1f} min of audio on {cores} cores ...")
t0 = time.perf_counter()
# condition_on_previous_text=False: Whisper's default (True) can loop and invent sentences.
segments, _ = model.transcribe(audio, language="en", beam_size=5, vad_filter=True,
                               condition_on_previous_text=False)
text = " ".join(s.text.strip() for s in segments)   # the work happens here (lazy generator)
t_run = time.perf_counter() - t0

out = HERE / f"climate_clip_120s.{a.model}.txt"
out.write_text(text, encoding="utf-8")
diff = percent_differ(text, REFERENCE.read_text(encoding="utf-8"))
print(f"\nfirst words: {text[:160]} ...")
print(f"transcript -> {out.name}\n")
line = (f"whisper {a.model} | cores {cores} | {clip / 60:.1f} min in {t_run:.1f} s | "
        f"{clip / t_run:.0f}x real time | {diff:.1f}% words differ")
print(line)
if a.send:
    send(line)
