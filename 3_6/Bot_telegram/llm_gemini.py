# -*- coding: utf-8 -*-
"""
/gpt con Google Gemini (API REST, senza SDK).

Chiave: costant.LLM_API_KEY (letta da env.ini -> llmapi=...).
Le chiavi nuove di Google (quelle che iniziano con "AQ.") funzionano SOLO
passate nell'header x-goog-api-key, non come ?key= nell'URL.
"""
import logging

import requests

import costant as key

log = logging.getLogger("pandamem.gemini")

ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
TIMEOUT = 60

# Errori per cui ha senso passare al modello successivo:
# 404 modello inesistente, 429 quota, 5xx sovraccarico temporaneo di Google
STATUS_DA_RIPROVARE = (404, 429, 500, 502, 503, 504)


class GeminiError(Exception):
    pass


def _modelli():
    modelli = [key.LLM_MODEL] + [m for m in key.LLM_MODEL_FALLBACK if m != key.LLM_MODEL]
    return modelli


def _estrai_testo(data):
    candidati = data.get("candidates") or []
    if not candidati:
        motivo = (data.get("promptFeedback") or {}).get("blockReason")
        return f"(nessuna risposta{': ' + motivo if motivo else ''})"
    parti = (candidati[0].get("content") or {}).get("parts") or []
    testo = "".join(p.get("text", "") for p in parti if not p.get("thought")).strip()
    if not testo:
        motivo = candidati[0].get("finishReason")
        return f"(risposta vuota{': ' + motivo if motivo else ''})"
    return testo


def chiedi(query, storico=None, system_prompt=None):
    """
    Manda la domanda a Gemini e ritorna il testo della risposta.

    storico: lista di battute precedenti [{"role": "user"|"model", "text": "..."}]
             per far capire al modello il contesto della conversazione.
    """
    api_key = key.LLM_API_KEY
    if not api_key:
        raise GeminiError("chiave Gemini mancante: aggiungi  llmapi=<chiave>  in .env")

    contents = []
    for battuta in storico or []:
        ruolo = "model" if battuta.get("role") == "model" else "user"
        testo = (battuta.get("text") or "").strip()
        if testo:
            contents.append({"role": ruolo, "parts": [{"text": testo}]})
    contents.append({"role": "user", "parts": [{"text": query}]})

    body = {
        "contents": contents,
        "generationConfig": {"maxOutputTokens": 2048, "temperature": 0.8},
    }
    system_prompt = system_prompt if system_prompt is not None else key.LLM_SYSTEM_PROMPT
    if system_prompt:
        body["systemInstruction"] = {"parts": [{"text": system_prompt}]}

    headers = {"x-goog-api-key": api_key, "Content-Type": "application/json"}

    ultimo_errore = None
    for model in _modelli():
        try:
            resp = requests.post(ENDPOINT.format(model=model), headers=headers, json=body, timeout=TIMEOUT)
        except requests.RequestException as e:
            raise GeminiError(f"errore di rete verso Gemini: {e}") from e

        if resp.status_code == 200:
            return _estrai_testo(resp.json())

        try:
            msg = resp.json().get("error", {}).get("message", resp.text)
        except ValueError:
            msg = resp.text
        ultimo_errore = f"{model}: HTTP {resp.status_code} - {msg[:300]}"

        if resp.status_code in (401, 403):
            raise GeminiError(f"chiave Gemini rifiutata ({resp.status_code}): {msg[:200]}")
        if resp.status_code in STATUS_DA_RIPROVARE:
            # modello assente o sovraccarico: provo il prossimo della lista
            log.warning("Gemini %s non disponibile (HTTP %s), provo il successivo",
                        model, resp.status_code)
            continue
        raise GeminiError(ultimo_errore)

    raise GeminiError(f"nessun modello Gemini disponibile al momento ({ultimo_errore})")


if __name__ == "__main__":
    print(chiedi("Dimmi una curiosita' sui panda in una frase."))
    print(chiedi(
        "E quanto pesa?",
        storico=[
            {"role": "user", "text": "Parlami del panda gigante"},
            {"role": "model", "text": "Il panda gigante vive nelle foreste di bambu' della Cina."},
        ],
    ))
