# Git by hand

This morning the agent ran git for you. Now you do it yourself, in the same
folder. Open a terminal in VS Code (**Terminal → New Terminal**) inside
`clim-course`.

Each step: run the command, read the output, then move on. If a command opens
a pager (text with `:` at the bottom), press `q` to leave it. Warnings like
`LF will be replaced by CRLF` are harmless: ignore them.

## 1. What did the agent do?

```
git status
git log --oneline
```

**`fatal: not a git repository`?** The agent never set up git here (or you are
in the wrong folder: check with `pwd` that you are in `clim-course`). Start it
yourself, then continue:

```
git init
git add -A
git commit -m "Start"
```

- Which files did the agent commit? Which are not tracked?
- Is there a commit for the analysis, or only "Initial commit"?

**No commits at all** (`git log` says "does not have any commits yet"), or the
analysis is not committed? Save this morning's work first, then continue:

```
git add -A
git commit -m "My analysis from this morning"
```

(If git asks who you are, run the two `git config --global user...` commands it
shows, with your name and email, then commit again.)

```
git log --all --oneline
```

- The lines `Agent host session … turn N` are checkpoints VS Code saved while
  the agent worked. They are not on your branch, but they are in your repository.

## 2. Make a change, see it, save it

Open `analysis.py` (or the agent's script) and change one thing, for example
the title of the chart. **No script?** Create `notes.md` with one line of text,
commit it (`git add notes.md`, `git commit -m "Notes"`), and use `notes.md`
wherever these steps say `analysis.py`. Then:

```
git status
git diff
git add analysis.py
git commit -m "Clearer chart title"
git log --oneline
```

`git diff` shows exactly what changed. `git add` chooses what goes into the next
commit; `git commit` saves it, with a message for future you.

## 3. Break something, get it back

Delete a few lines from `analysis.py` and save. Then:

```
git diff
git restore analysis.py
git diff
```

The second `git diff` is empty: the file is back to the last commit.

## 4. Try something on a branch

```
git switch -c monthly-baseline
```

Change the script (or ask the agent to), run it, then commit:

```
git add -A
git commit -m "Try a baseline per month"
git switch -
```

`git switch -` goes back to the branch you came from. Look at the script: your
change is gone from here, but kept on `monthly-baseline`. `git log --all --oneline`
shows both.

## 5. What should and should not be in git

```
git ls-files
```

| should be in git | should **not** be in git |
|---|---|
| your scripts and notebooks | `.venv/` (rebuilt by `uv sync`) |
| `pyproject.toml` **and** `uv.lock` | API keys, passwords, `.env` files |
| a README | large or confidential data |

**Does `git ls-files` list files under `.venv/`?** The agent committed your
environment. Take it out of git (the folder itself stays on your disk) and
ignore it from now on:

```
git rm -r --cached .venv
```

Add a line `.venv/` to `.gitignore` (create the file if it does not exist),
then `git add .gitignore` and `git commit -m "Stop tracking .venv"`.

Check it: create a file `my_key.txt` with any text in it, then `git status`.
If git lists it, add a line `*_key.txt` to `.gitignore`, run `git status` again,
and commit the `.gitignore`.

Why `uv.lock`: with `pyproject.toml` and `uv.lock` in git, anyone (including you,
on the cluster, in a year) gets the same packages with `uv sync`.

## Done early?

- `git show HEAD~1` shows the commit before the last one.
- `git log -p analysis.py` shows every change to one file.
- Ask the agent: *"Explain what each of my last three commits changed."* Then
  check its answer with `git log -p`.
