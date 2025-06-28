# AItana

AItana is an AI-powered Telegram agent built with Python and the
`python-telegram-bot` framework.

## Quick Start

```bash
git clone https://github.com/<your-username>/AItana.git
cd AItana
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 1. Crear entorno virtual
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Exportar el token (o usar archivo .env)
export AITANA_TOKEN="123456:ABC-DEF..."

# 4. Lanzar el bot
python -m aitana                  # o: python src/aitana/bot.py
