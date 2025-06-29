<!-- README.md -->

<h1 align="center">🤖 AItana</h1>
<p align="center">
  <em>AI-powered Telegram assistant — multi-function agent with short-term memory, debug mode and (so far) expense tracking.</em><br>
  <img alt="Python" src="https://img.shields.io/badge/python-3.10%2B-blue?logo=python">
  <img alt="License" src="https://img.shields.io/badge/license-MIT-green">
  <img alt="Tests"  src="https://img.shields.io/badge/tests-passing-brightgreen">
</p>

---

## ✨ Features

| Capability | Trigger | Description |
|------------|---------|-------------|
| Greeting & quick manual | `/start`, `/help` | Sends a concise user guide. |
| **Expense tracking** (Phase 8) | _Plain sentence containing_ “soy … me he gastado …” etc. | Auto-parses name / amount / place and appends a line to `data/gastos_<name>.csv`, replying with “✅ Gasto registrado: …”. |
| Chat with LLM (DeepSeek via Together AI) | any other text | Replies with the configured model while keeping short-term context. |
| Show / hide LLM “thoughts” | `/debug on` / `/debug off` | Toggles the hidden `<think>…</think>` block for that chat. |
| Memory statistics | `/stats` | Shows how many user/assistant pairs are stored. |
| Clear memory | `/clear` | Wipes recent history for the chat. |
| Telegram autocomplete | type `/` | Built-in menu with all commands. |

> **Roadmap:** future phases will add rate-limit, moderation, Docker deploy, long-term memory, etc.

---

## 🚀 Quick start

```bash
# 1. Clone & enter
git clone https://github.com/<your-user>/AItana.git
cd AItana

# 2. Virtualenv
python3 -m venv .venv && source .venv/bin/activate

# 3. Install deps
pip install -r requirements.txt
pip install -r dev-requirements.txt  # 🧪 lint & tests (optional)

# 4. Configure environment
cp .env.example .env
nano .env           # paste TELEGRAM bot token & TOGETHER_API_KEY

# 5. Run
python -m aitana    # run from repo root so .env is loaded


```

### ⚙️ Configuración (`.env`)

| Variable           | Example                                                  | Purpose                                               |
|--------------------|----------------------------------------------------------|-------------------------------------------------------|
| `AITANA_TOKEN`     | `123456:ABC…`                                            | **BotFather** Token                                   |
| `TOGETHER_API_KEY` | `tgp_v1_…`                                               | **Together AI** key                                   |
| `MODEL_NAME`       | `deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free`         | Any model listed by the API.                             |
| `MAX_HISTORY`      | `6`                                                      | User/assistant pairs kept in prompt window.           |
| `MAX_TOKENS_OUT`   | `600`                                                    | Max tokens generated per reply.                       |

> [!TIP]
> If TOGETHER_API_KEY is missing or invalid the bot replies with an error and no credits are consumed.

---

## 🗄️ Project layout

```text
src/aitana/
├── bot.py              # entry-point
├── handlers/           # telegram handlers
│   ├── chat.py         # all text → LLM or expense parser
│   ├── start.py        # /start → /help
│   ├── help.py         # /help
│   ├── stats.py        # /stats
│   ├── clear.py        # /clear
│   └── debug.py        # /debug on|off
├── utils/
│   ├── expenses.py     # parse & store CSV lines   ← Phase 8
│   └── logging.py      # colour logs
├── llm_client.py       # Together AI REST wrapper
├── memory.py           # SQLite short-term memory + flags
└── __main__.py
tests/                  # pytest suite (ruff, mypy clean)

```

### 🧑‍💻 Development workflow

```bash
# auto-format & lint
aitana-fmt          
ruff check src tests 
mypy src/aitana       

# Tests
pytest

```

### 💾 Expense file format
Each user gets a separate CSV in data/:
```bash
data/gastos_alberto.csv
timestamp,amount,place,raw
2025-06-29T15:42:17,15.0,Mercadona,Hola soy Alberto y me he gastado 15 euros...
```
The regex recognises phrases like:

 • Soy Ana y me he gastado 9 € en cine
 • Me llamo Luis, he gastado 12,50 euros en Zara
 • Soy Pedro y me acabo de gastar 20 € en el bar

Feel free to tweak the pattern in utils/expenses.py for your language style.

### ⛑️ Roadmap

- **Fase 9** – Dockerfile + despliegue CI  
- **Fase 10** – Memoria a largo plazo (resúmenes / vector store)

> [!NOTE]
> Extras: rate-limit, voice, web UI… PRs welcome!

---

### 📜 Licencia

Publicado bajo la licencia **MIT**.  
Consulta el archivo **LICENSE** para el texto completo.

© 2025 Proyecto AItana
