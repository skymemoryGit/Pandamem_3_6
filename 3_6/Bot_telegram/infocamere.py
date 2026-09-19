# -*- coding: utf-8 -*-
"""
Modulo InfoCamere per PandaMem.

- get_job_listings()      -> scarica gli annunci di lavoro pubblicati da InfoCamere
- build_listing_message() -> testo HTML pronto per Telegram (lista annunci)
- check_for_changes()     -> confronta il numero di annunci con l'ultimo salvato
                              su counter.txt e restituisce il messaggio di notifica
                              se qualcosa e' cambiato (altrimenti None)
"""
import html
import os

import requests
from bs4 import BeautifulSoup

# Annunci pubblicati (per testare le variazioni si puo' usare annType=expired)
URL_PUBLISHED = (
    "https://selezione-ic-eco.intervieweb.it/app.php?module=iframeAnnunci&lang=it"
    "&k=33c37121b6f5bfb252869f8efdf12e6c&d=www.infocamere.it&LAC=&utype=&act1=23"
    "&defgroup=date&gnavenable=1&desc=1&annType=published&h=&typeView=small"
    "&fontFamily=Arial&bgColor=FFFFFF&bgRowVacancy=FFFFFF&separatoColor=D2DAE6"
    "&filterColor=000000&filterActiveColor=24509A&jobTitleColor=000000"
    "&jobTitleActiveColor=24509A&jobDescColor=000000&jobInfoColor=5B6770"
)

# File in cui viene salvato l'ultimo numero di annunci visto
COUNTER_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "counter.txt")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/128.0 Safari/537.36"
    ),
    "Accept-Language": "it-IT,it;q=0.9",
}
TIMEOUT = 20

# Telegram accetta al massimo 4096 caratteri per messaggio
TELEGRAM_MAX_LEN = 4000


class InfoCamereError(Exception):
    pass


def get_job_listings():
    """Ritorna una lista di dict: {"title", "location", "link"}."""
    try:
        response = requests.get(URL_PUBLISHED, headers=HEADERS, timeout=TIMEOUT)
    except requests.RequestException as e:
        raise InfoCamereError(f"Errore di rete verso InfoCamere: {e}") from e

    if response.status_code != 200:
        raise InfoCamereError(
            f"InfoCamere ha risposto {response.status_code}. Riprova piu' tardi."
        )

    soup = BeautifulSoup(response.content, "html.parser")
    jobs = []
    for job in soup.find_all("a", class_="item-job-list"):
        link = job.get("href", "") or ""
        if link.startswith("/"):
            link = "https://selezione-ic-eco.intervieweb.it" + link

        name_div = job.find("div", class_="name-job")
        title = name_div.get_text(strip=True) if name_div else "(senza titolo)"

        location = ""
        info_div = job.find("div", class_="info-job")
        if info_div:
            span = info_div.find("span", class_="font-inherit")
            location = (span or info_div).get_text(" ", strip=True)

        jobs.append({"title": title, "location": location, "link": link})

    return jobs


def build_listing_message(jobs):
    """Costruisce il testo HTML (parse_mode=HTML) con tutti gli annunci."""
    if not jobs:
        return "📭 Nessun annuncio InfoCamere disponibile al momento."

    lines = [f"<b>InfoCamere - annunci disponibili: {len(jobs)}</b>", ""]
    for j in jobs:
        title = html.escape(j["title"])
        location = html.escape(j["location"]) if j["location"] else "n/d"
        if j["link"]:
            lines.append(f"📌 <b>{title}</b>\n   📍 {location}\n   🔗 <a href=\"{html.escape(j['link'], quote=True)}\">Candidati qui</a>")
        else:
            lines.append(f"📌 <b>{title}</b>\n   📍 {location}")
        lines.append("")
    return "\n".join(lines).rstrip()


def split_message(text, max_len=TELEGRAM_MAX_LEN):
    """Divide un messaggio lungo in piu' pezzi, spezzando sulle righe vuote."""
    if len(text) <= max_len:
        return [text]

    chunks, current = [], ""
    for block in text.split("\n\n"):
        candidate = block if not current else current + "\n\n" + block
        if len(candidate) > max_len and current:
            chunks.append(current)
            current = block
        else:
            current = candidate
    if current:
        chunks.append(current)
    return chunks


def read_saved_job_count():
    try:
        with open(COUNTER_FILE, "r", encoding="utf-8") as f:
            return int(f.read().strip())
    except (FileNotFoundError, ValueError):
        return None


def save_job_count(count):
    with open(COUNTER_FILE, "w", encoding="utf-8") as f:
        f.write(str(count))


def check_for_changes():
    """
    Confronta il numero attuale di annunci con quello salvato.
    Ritorna (messaggio_notifica | None, numero_annunci).
    """
    jobs = get_job_listings()
    new_count = len(jobs)
    old_count = read_saved_job_count()

    if old_count is None:
        # Prima esecuzione: salvo e basta, niente notifica
        save_job_count(new_count)
        return None, new_count

    if new_count == old_count:
        return None, new_count

    save_job_count(new_count)
    if new_count > old_count:
        change = f"➕ Annunci aggiunti: {new_count - old_count}"
    else:
        change = f"➖ Annunci rimossi: {old_count - new_count}"

    message = (
        "🔔 <b>InfoCamere - aggiornamento annunci</b> 🔔\n\n"
        f"📊 Prima: <b>{old_count}</b>\n"
        f"📈 Adesso: <b>{new_count}</b>\n\n"
        f"{change}\n\n"
        "✅ /infocamere per i dettagli"
    )
    return message, new_count


if __name__ == "__main__":
    # Test rapido da riga di comando
    lista = get_job_listings()
    print(build_listing_message(lista))
    print("\nTotale:", len(lista))
