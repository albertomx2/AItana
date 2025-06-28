<h1 align="center">🤖 AItana</h1>
<p align="center">
  <em>Agente de Telegram impulsado por IA — Echo, Q&amp;A, memoria y depuración.</em><br>
  <img alt="Python" src="https://img.shields.io/badge/python-3.10%2B-blue?logo=python">
  <img alt="License" src="https://img.shields.io/badge/license-MIT-green">
  <img alt="Build"   src="https://img.shields.io/badge/tests-passing-brightgreen">
</p>

---

## ✨ Características

| **Capacidad** | **Comando**                    | **Descripción**                                                     |
|---------------|--------------------------------|---------------------------------------------------------------------|
| Saludo & ayuda  | `/start`, `/help`              | Muestra la guía rápida.                                             |
| Preguntar al LLM (DeepSeek vía Together AI) | `/ask <pregunta>`               | Responde con el modelo configurado y recuerda el contexto.          |
| Mostrar/Ocultar “pensamientos” del LLM | `/debug on` / `/debug off`      | Activa o desactiva la vista de `<think>…</think>`.                  |
| Estadísticas de memoria | `/stats`                        | Muestra cuántos pares usuario/asistente se guardan.                 |
| Borrar memoria | `/clear`                        | Elimina el historial reciente del chat.                             |
| Eco de respaldo | *texto plano*                   | Cualquier otro texto se devuelve como eco.                          |

---

## 🚀 Inicio rápido

```bash
# 1. Clonar & entrar
git clone https://github.com/<tu-usuario>/AItana.git
cd AItana

# 2. Crear un entorno virtual
python3 -m venv .venv && source .venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt
pip install -r dev-requirements.txt   # 🧪 lint & tests (opcional)

# 4. Configurar variables de entorno
cp .env.example .env
nano .env      # pega tu token de TELEGRAM y TOGETHER_API_KEY

# 5. Ejecutar
python -m aitana
# (Ejecuta desde la raíz del proyecto para que .env se cargue)

```

### ⚙️ Configuración (`.env`)

| Variable           | Ejemplo                                                  | Propósito                                             |
|--------------------|----------------------------------------------------------|-------------------------------------------------------|
| `AITANA_TOKEN`     | `123456:ABC…`                                            | Token de **BotFather**.                               |
| `TOGETHER_API_KEY` | `tgp_v1_…`                                               | Clave de **Together AI**.                             |
| `MODEL_NAME`       | `deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free`         | Nombre del modelo a usar.                             |
| `MAX_HISTORY`      | `6`                                                      | Número de pares turno-a-turno que se conservan.       |
| `MAX_TOKENS_OUT`   | `300`                                                    | Tokens máximos por respuesta.                         |

> [!TIP]
> Si falta `TOGETHER_API_KEY` o es inválida, el comando `/ask` devuelve error sin consumir créditos.

---

## 🗄️ Estructura del proyecto

```text
src/aitana/
├── bot.py              # Punto de entrada
├── handlers/           # Manejadores de Telegram
│   ├── ask.py          # /ask + filtro think
│   ├── start.py        # /start ➜ ayuda
│   ├── help.py         # /help
│   ├── stats.py        # /stats
│   ├── clear.py        # /clear
│   ├── debug.py        # /debug on|off
│   └── echo.py         # Eco de respaldo
├── llm_client.py       # Wrapper de Together AI
├── memory.py           # Memoria SQLite + flags
└── utils/              # Logging & helpers
tests/                  # Pytest suite

```

### 🧑‍💻 Desarrollo

```bash
# Formateo automático & lint
aitana-fmt            # ruff --fix
ruff check src tests  # estilo
mypy src/aitana       # tipado

# Tests
pytest                # 4 tests, todos en verde ✔️

```
### ⛑️ Roadmap

- **Fase 7** – Dockerfile + despliegue CI  
- **Fase 8** – Memoria a largo plazo (resúmenes / vector store)

> [!NOTE]
> Ideas futuras: *rate-limit*, moderación, voz, web UI… ¡PRs bienvenidos!

---

### 📜 Licencia

Publicado bajo la licencia **MIT**.  
Consulta el archivo **LICENSE** para el texto completo.

© 2025 Proyecto AItana
