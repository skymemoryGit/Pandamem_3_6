# -*- coding: utf-8 -*-
"""
Configurazione PandaMem bot.

Le chiavi si mettono nel file .env (oppure env.ini) nella stessa cartella,
una per riga, senza virgolette:

    pandamen_telegram_token=<token del bot, da @BotFather>
    llmapi=<chiave Gemini>

Questi file NON vanno su GitHub: sono gia' esclusi dal .gitignore.
"""
import os

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Vengono letti in ordine: quelli piu' avanti nella lista vincono
ENV_FILES = [os.path.join(_BASE_DIR, "env.ini"), os.path.join(_BASE_DIR, ".env")]


def _parse_env_file(path):
    """Legge un file chiave=valore (ignora righe vuote, commenti e [sezioni])."""
    data = {}
    try:
        with open(path, encoding="utf-8-sig") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith(("#", ";", "[")) or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                k = k.strip().lower().lstrip("﻿")
                v = v.strip().strip('"').strip("'")
                if k:
                    data[k] = v
    except FileNotFoundError:
        pass
    except OSError as e:
        print(f"Attenzione: non riesco a leggere {path}: {e}")
    return data


_ENV = {}
for _f in ENV_FILES:
    _ENV.update(_parse_env_file(_f))


def _first(*chiavi, default=""):
    """Ritorna il primo valore non vuoto tra le chiavi date (file .env, poi ambiente)."""
    for c in chiavi:
        v = _ENV.get(c.lower())
        if v:
            return v
    for c in chiavi:
        v = os.environ.get(c.upper())
        if v:
            return v
    return default


# --- Telegram -----------------------------------------------------------------
# Accetto piu' nomi possibili cosi' funziona comunque come l'hai scritto nel .env
API_KEY = _first(
    "pandamen_telegram_token",
    "pandamem_telegram_token",
    "telegram_token",
    "bot_token",
    "token",
)

# --- /gpt con Gemini -----------------------------------------------------------
LLM_API_KEY = _first("llmapi", "gemini_api_key", "google_api_key")
# Modello preferito; se non esiste piu' prova quelli in LLM_MODEL_FALLBACK
LLM_MODEL = _first("llm_model", default="gemini-3.8-flash")
LLM_MODEL_FALLBACK = [
    "gemini-3.7-flash",
    "gemini-3.5-flash",
    "gemini-2.5-flash",
    "gemini-flash-latest",
]
LLM_SYSTEM_PROMPT = (
    "Sei PandaMem, il bot di un gruppo Telegram di amici. "
    "Rispondi nella lingua della domanda, in modo breve e diretto (massimo 1500 caratteri), "
    "senza formattazione markdown. "
    "Nei gruppi i messaggi possono essere preceduti dal nome di chi scrive "
    "(es. 'Marco: ...'): usalo per capire chi parla, ma non ripeterlo nella risposta."
)
# Memoria di /gpt: quante battute tenere per chat (1 battuta = domanda o risposta)
# e dopo quanti minuti di silenzio dimenticare la conversazione. 0 = memoria spenta.
LLM_MEMORIA_BATTUTE = int(_first("llm_memoria_battute", default="10") or 0)
LLM_MEMORIA_MINUTI = int(_first("llm_memoria_minuti", default="30") or 0)

# --- /gpt con OpenAI (alternativa, non usata da main.py) ------------------------
OPENAI_API_KEY = _first("openai_api_key")
OPENAI_MODEL = "gpt-4o-mini"

# --- /infocamere -----------------------------------------------------------------
# Chat/canale dove mandare l'avviso quando cambia il numero di annunci.
INFOCAMERE_CHANNEL_ID = _first("infocamere_channel_id", default="-1002469064066")
# Ogni quanti minuti controllare gli annunci in automatico. 0 = disattivato
# (il comando /infocamere funziona comunque).
INFOCAMERE_CHECK_MINUTES = int(_first("infocamere_check_minutes", default="60") or 0)


if not API_KEY:
    print(
        "ATTENZIONE: manca il token Telegram.\n"
        "Aggiungi in .env una riga:  pandamen_telegram_token=<token di BotFather>"
    )
