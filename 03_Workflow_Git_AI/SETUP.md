# Setup: (≈ 20 minutes)

## 1. Install the tools

**uv** (manages Python and packages)

- Windows (PowerShell):
  ```powershell
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```
- macOS / Linux (Terminal):
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

Close and reopen the terminal, then check: `uv --version`

**Git**: https://git-scm.com/downloads (default options are fine).
Check: `git --version`

**Visual Studio Code**: https://code.visualstudio.com/download
You do not need to sign in with GitHub.

In VS Code, open the Extensions panel (`Ctrl+Shift+X` / `Cmd+Shift+X`) and install:

- **Python** (Microsoft)
- **Jupyter** (Microsoft)
- **GitHub Copilot Chat**, if the Chat panel (`Ctrl+Alt+I` / `Cmd+Ctrl+I`) is not already there

---

## 2. Get an API key for the AI models

We use open models hosted in Switzerland. Your prompts and data stay at Swiss
research infrastructure, not with a commercial provider.

### Option A (default): Swiss AI Research Platform, free for academics

1. Go to **https://serving.swissai.svc.cscs.ch** and log in with your university account.
2. Create an API key and copy it somewhere safe. **Treat it like a password.**
3. Test it. Replace `YOUR_KEY` and run in a terminal:
   ```powershell
   curl.exe https://api.swissai.svc.cscs.ch/v1/models -H "Authorization: Bearer YOUR_KEY"
   ```
   (macOS/Linux: `curl` instead of `curl.exe`.) You should see a long list of model names.

### Option B: you cannot create a Swiss AI account

We will give you a temporary key for GPUStack
(University of Bern). It is valid for the course only.

---

## 3. Connect VS Code to the models

1. In VS Code press `Ctrl+Shift+P` (`Cmd+Shift+P` on macOS) and run
   **Chat: Manage Language Models**.
2. **Add Models** → **Custom endpoint**. Give it a name (`SwissAI` or `GPUStack`),
   choose **Chat Completions**, and paste your API key when asked.
3. VS Code opens a settings file (JSON). **Keep the `"apiKey"` line it created**
   and replace the `"models"` list with the one for your option below.

**Option A: Swiss AI** (two models)

```json
"models": [
    {
        "id": "RCP-AIaaS/openai/gpt-oss-120b",
        "name": "gpt-oss-120b (Swiss AI)",
        "url": "https://api.swissai.svc.cscs.ch/v1",
        "toolCalling": true,
        "vision": false,
        "maxInputTokens": 100000,
        "maxOutputTokens": 16000
    },
    {
        "id": "CSCS-Inference/zai-org/GLM-5.3-Flash",
        "name": "GLM-5.3-Flash (Swiss AI)",
        "url": "https://api.swissai.svc.cscs.ch/v1",
        "toolCalling": true,
        "vision": false,
        "maxInputTokens": 180000,
        "maxOutputTokens": 32000
    }
]
```

**Option B: GPUStack** (two models)

```json
"models": [
    {
        "id": "gpt-oss-120b",
        "name": "gpt-oss-120b (GPUStack)",
        "url": "https://gpustack.unibe.ch/v1",
        "toolCalling": true,
        "vision": false,
        "maxInputTokens": 100000,
        "maxOutputTokens": 16000
    },
    {
        "id": "qwen3.8-27b",
        "name": "Qwen3.8-27B (GPUStack)",
        "url": "https://gpustack.unibe.ch/v1",
        "toolCalling": true,
        "vision": false,
        "maxInputTokens": 100000,
        "maxOutputTokens": 16000
    }
]
```

In the course, use Qwen wherever the instructions say GLM.

Qwen is slow: one answer can take several minutes. gpt-oss is a larger model, but for
each word it writes it uses only a small part of itself, so on this server it writes
about three to four times faster. Qwen uses all of itself for every word, and it also
"thinks" at length before it answers. When you give Qwen a task, start it and let it work.

4. Save the file. Open the Chat panel, set the mode to **Agent**, pick your model
   from the model list, and type: `Say hello in one sentence.`
   If you get an answer, you are ready.

---

## 4. Create the course folder

Pick a place **outside** OneDrive/Dropbox/iCloud (sync tools break Python
environments), for example `C:\Users\<you>\clim-course` or `~/clim-course`.

```powershell
mkdir clim-course
cd clim-course
curl.exe -LO https://raw.githubusercontent.com/dsl-unibe-ch/Climplus_DSL_Training_v1/main/03_Workflow_Git_AI/pyproject.toml
curl.exe -LO https://raw.githubusercontent.com/dsl-unibe-ch/Climplus_DSL_Training_v1/main/03_Workflow_Git_AI/uv.lock
uv sync
```

(macOS/Linux: `curl` instead of `curl.exe`.) `uv sync` downloads Python and the
packages into a `.venv` folder inside `clim-course`. Then open the folder in
VS Code: **File → Open Folder…**.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| `uv` / `git` not found | Close and reopen the terminal (or VS Code) after installing. |
| `401 Unauthorized` | The key is wrong or has a space/line break in it. Paste it again. |
| Model not in the list | Check the JSON was saved, then reload VS Code (`Developer: Reload Window`). |
| Model answers but never runs commands | Make sure the chat mode is **Agent**, not Ask. |
| `uv sync` says no `pyproject.toml` | You are in the wrong folder: `cd clim-course` first. |
