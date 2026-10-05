# AItana

Asistente de Telegram en Python con conversación mediante Together AI, memoria corta por chat y registro sencillo de gastos en CSV.

## Funciones actuales

- `/start`, `/help`: guía.
- `/stats`, `/clear`: consultar o vaciar memoria.
- `/debug on` y `/debug off`: mostrar/ocultar bloques de razonamiento del proveedor.
- Mensajes de gasto reconocidos mediante expresiones regulares: CSV por nombre.
- Otros mensajes: conversación con el modelo configurado.

**No es una IA completamente local.** Telegram y Together AI son servicios externos. La detección de gastos no es un parser financiero universal y el nombre escrito en un mensaje no acredita una identidad.

## Instalación y arranque

Requisitos: Python 3.10 o superior, token de bot de Telegram y clave de Together AI para conversar.

```bash
git clone https://github.com/albertomx2/AItana.git
cd AItana
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip install -e .
cp .env.example .env
```

En Windows: `.venv\Scripts\Activate.ps1`. Edita el entorno:

| Variable | Función |
| --- | --- |
| AITANA_TOKEN | Token obtenido con BotFather |
| TOGETHER_API_KEY | Clave privada del proveedor |
| MODEL_NAME | Identificador de un modelo disponible en tu cuenta |
| MAX_HISTORY | Pares de mensajes mantenidos, por defecto 6 |
| MAX_TOKENS_OUT | Límite de salida, por defecto 600 |

```bash
python -m aitana
```

El bot usa polling; no requiere publicar un puerto ni configurar webhook. Abre el chat del bot y prueba `/help`. Detén el proceso con Ctrl+C.

El modelo por defecto del código es histórico: confirma que sigue disponible y su precio en tu cuenta. No se garantiza acceso gratuito. Parte de la configuración del cliente LLM se lee al importar módulos: si `MODEL_NAME` del archivo no se aplica, exporta la variable antes de arrancar y reinicia.

## Persistencia y privacidad

Los gastos se escriben en `data/gastos_<nombre>.csv`, con fecha, cantidad, lugar y mensaje original. Revisa `src/aitana/memory.py` para la memoria SQLite. Guarda copias privadas y no subas CSV, memoria, mensajes ni `.env`.

No hay lista de usuarios autorizados en el arranque revisado: antes de uso real, añadir control de acceso, límites y una política de retención. No enviar documentos confidenciales al proveedor.

## Desarrollo

```bash
python -m pip install -r dev-requirements.txt
python -m pytest
python -m ruff check src tests
python -m mypy src/aitana
```

`src/aitana/handlers` gestiona comandos; `llm_client.py` llama a Together; `utils/expenses.py` analiza gastos. Esta revisión comprueba documentación contra el código, no la conexión real a Telegram/Together.

MIT, según `LICENSE`. Pendientes: autorización, mejor extracción, tests de integración y despliegue reproducible.
