# -*- coding: utf-8 -*-
"""
PandaMem bot 3.6

Created on Thu Mar 30 15:13:17 2023
@author: Ye Jian_cheng

Avvio: doppio click su avvia_bot.bat (installa le dipendenze e lancia il bot)
       oppure  python main.py  dalla cartella Bot_telegram.
"""
import asyncio
import logging
import os
import sys
import time
import traceback
from glob import glob
from random import choice

# Le immagini/audio sono referenziati con percorsi relativi (img/..., audio/...):
# mi sposto nella cartella dello script cosi' funziona da qualunque punto lo lanci.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

# Console Windows: evita crash su emoji/accenti nei log
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    level=logging.INFO,
)
logging.getLogger("httpx").setLevel(logging.WARNING)
log = logging.getLogger("pandamem")

import costant as key
import Responses as r

try:
    from telegram import BotCommand, LinkPreviewOptions
    from telegram.constants import ParseMode
    from telegram.ext import Application, CommandHandler, MessageHandler, filters
except ImportError:
    print(
        "\nManca la libreria python-telegram-bot (o e' installata la versione sbagliata).\n"
        "Lancia avvia_bot.bat oppure esegui:\n"
        "    pip uninstall -y telegram\n"
        "    pip install -r requirements.txt\n"
    )
    input("Premi INVIO per chiudere...")
    sys.exit(1)

import infocamere

# --- Moduli opzionali: se manca una libreria il relativo comando viene disabilitato
# ma il bot parte lo stesso.
try:
    import text_on_img as toi          # /GenPanda  (pillow)
except Exception as e:
    toi = None
    log.warning("text_on_img non disponibile (/GenPanda disattivato): %s", e)

try:
    import Family_API                  # /waifu     (pillow)
except Exception as e:
    Family_API = None
    log.warning("Family_API non disponibile (/waifu disattivato): %s", e)

try:
    import llm_gemini as llm           # /gpt       (Gemini, chiave in env.ini)
except Exception as e:
    llm = None
    log.warning("llm_gemini non disponibile (/gpt disattivato): %s", e)

# import img_down as bing_downloader   # /find (bing_image_downloader) - non usato
# import auto_relply_quotes as autoreply  # servizio auto reply QUOTES, va lanciato a parte

print("Bot start")


def _args_text(context):
    """Unisce gli argomenti del comando in una stringa ('' se non ce ne sono)."""
    return " ".join(context.args).strip() if context.args else ""


# --- Preparazione foto -------------------------------------------------------
# Telegram rifiuta le foto sopra i 10 MB e quelle con lati troppo grandi
# (larghezza+altezza max 10000). Diverse immagini in img/waifu superano i 28 MB,
# quindi prima di spedire le rimpicciolisco in una copia temporanea.
MAX_BYTES = 5 * 1024 * 1024
MAX_LATO = 2560
TMP_DIR = os.path.join(BASE_DIR, "tmp")


def _prepara_foto(path):
    """Ritorna il path da inviare: l'originale se e' gia' ok, altrimenti una copia ridotta."""
    try:
        size = os.path.getsize(path)
        from PIL import Image

        with Image.open(path) as im:
            w, h = im.size
            serve = size > MAX_BYTES or max(w, h) > MAX_LATO or (w + h) > 10000
            if not serve:
                return path

            im = im.convert("RGB")
            im.thumbnail((MAX_LATO, MAX_LATO), Image.LANCZOS)
            os.makedirs(TMP_DIR, exist_ok=True)
            out = os.path.join(TMP_DIR, "send_" + os.path.splitext(os.path.basename(path))[0] + ".jpg")
            im.save(out, "JPEG", quality=85, optimize=True)

        log.info("Foto ridotta: %s (%.1f MB, %dx%d) -> %s (%.1f MB)",
                 os.path.basename(path), size / 1048576, w, h,
                 os.path.basename(out), os.path.getsize(out) / 1048576)
        return out
    except Exception as e:
        log.warning("Non riesco a ridimensionare %s (%s), provo con l'originale", path, e)
        return path


async def _send_photo(update, path, caption=None):
    """Invia una foto gestendo ridimensionamento e timeout generosi."""
    path = await asyncio.to_thread(_prepara_foto, path)
    with open(path, "rb") as f:
        await update.message.reply_photo(f, caption=caption, write_timeout=120, read_timeout=60)


# ----------------------------------------------------------------------------
# Comandi base
# ----------------------------------------------------------------------------
async def start_command(update, context):
    await update.message.reply_text("Welcome to PandaMem world, Let's rock it")
    await update.message.reply_text("/help to show what we can do! :)")


async def help_command(update, context):
    await update.message.reply_text(
        "List available cmd :\n"
        "/help\n"
        "/alcaldo\n"
        "/triviale\n"
        "/fantasia\n"
        "/GenPanda <testo>\n"
        "/gpt <domanda>  (Gemini)\n"
        "/jesolo\n"
        "/waifu <testo>\n"
        "/infocamere  - annunci di lavoro InfoCamere\n"
    )


async def handle_message(update, context):
    txt = str(update.message.text)
    ris = r.sample_response(txt)
    await update.message.reply_text(ris)


async def error_handler(update, context):
    log.error("Update %s ha causato un errore: %s", update, context.error)


# ----------------------------------------------------------------------------
# Immagini random dalle cartelle
# ----------------------------------------------------------------------------
async def _reply_random_image(update, pattern, testo=None):
    files = glob(pattern)
    if not files:
        await update.message.reply_text(f"Nessuna immagine trovata in {pattern}")
        return
    if testo:
        await update.message.reply_text(testo)
    await _send_photo(update, choice(files))


async def alcaldo_command(update, context):
    await _reply_random_image(update, "img/alcaldo/*.PNG")


async def fantasia_command(update, context):
    await _reply_random_image(update, "img/fantasia/*.jpg")


async def triviale_command(update, context):
    await _reply_random_image(update, "img/triviale/*.PNG")


async def jesolo_command(update, context):
    await _reply_random_image(update, "img/jesolo/*.jpg", "Ecco a te Jeppsolo")


# ----------------------------------------------------------------------------
# Meme generator
# ----------------------------------------------------------------------------
async def GenPanda_command(update, context):
    if toi is None:
        await update.message.reply_text("/GenPanda non disponibile (manca pillow)")
        return

    s = _args_text(context)   # testo dato dall'utente
    if s == "":
        s = "write something\nafter /genpanda"

    # escludo result.png (e' l'output del giro precedente)
    basi = [p for p in glob("img/pandamem/*.png") if not p.endswith("result.png")]
    img = choice(basi)
    await asyncio.to_thread(toi.creaCustomPandaMeme, img, s)
    await _send_photo(update, "img/pandamem/result.png")   # mandi indietro result


async def waifu_command(update, context):
    if Family_API is None:
        await update.message.reply_text("/waifu non disponibile (manca pillow)")
        return

    s = _args_text(context)
    if s == "":
        await _reply_random_image(update, "img/waifu/prova_*.png")
        return

    await asyncio.to_thread(Family_API.crea_immagine_waifu_Text, s)
    await _send_photo(update, "img/waifu/prova_testo.png")   # mandi indietro result


# ----------------------------------------------------------------------------
# GPT (Gemini) con memoria della conversazione
# ----------------------------------------------------------------------------
# Lo storico sta in context.chat_data, quindi e' separato per ogni chat/gruppo
# e sparisce al riavvio del bot. Si azzera da solo dopo un po' di silenzio.
MEMORIA_BATTUTE = max(0, int(getattr(key, "LLM_MEMORIA_BATTUTE", 12)))
MEMORIA_SECONDI = max(0, int(getattr(key, "LLM_MEMORIA_MINUTI", 30))) * 60


def _storico_chat(context):
    """Ritorna lo storico della chat, svuotandolo se e' passato troppo tempo."""
    if MEMORIA_BATTUTE == 0:
        return []

    dati = context.chat_data.setdefault("gpt", {"battute": [], "ultimo": 0.0})
    adesso = time.time()
    if MEMORIA_SECONDI and dati["battute"] and (adesso - dati["ultimo"]) > MEMORIA_SECONDI:
        log.info("Memoria /gpt scaduta, riparto da zero")
        dati["battute"] = []
    return dati["battute"]


def _aggiorna_storico(context, domanda, risposta):
    if MEMORIA_BATTUTE == 0:
        return
    dati = context.chat_data.setdefault("gpt", {"battute": [], "ultimo": 0.0})
    dati["battute"].append({"role": "user", "text": domanda})
    dati["battute"].append({"role": "model", "text": risposta})
    # tengo solo le ultime N battute
    dati["battute"] = dati["battute"][-MEMORIA_BATTUTE:]
    dati["ultimo"] = time.time()


async def gpt_command(update, context):
    if llm is None:
        await update.message.reply_text("/gpt non disponibile (modulo llm_gemini non caricato)")
        return

    s = _args_text(context)
    if s == "":
        await update.message.reply_text("write something\nafter /gpt")
        return

    # nei gruppi metto davanti il nome, cosi' il modello sa chi sta parlando
    domanda = s
    if update.effective_chat.type != "private":
        nome = update.effective_user.first_name or update.effective_user.username or "Anonimo"
        domanda = f"{nome}: {s}"

    print(domanda)
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    storico = _storico_chat(context)
    try:
        risposta = await asyncio.to_thread(llm.chiedi, domanda, list(storico))
        _aggiorna_storico(context, domanda, risposta)
    except Exception as e:
        log.exception("Errore /gpt")
        risposta = f"Errore Gemini: {e}"

    print(risposta)
    for chunk in infocamere.split_message(risposta):
        await update.message.reply_text(chunk)


# ----------------------------------------------------------------------------
# InfoCamere
# ----------------------------------------------------------------------------
NO_PREVIEW = LinkPreviewOptions(is_disabled=True)


async def infocamere_command(update, context):
    """Manda la lista degli annunci di lavoro InfoCamere."""
    await update.message.reply_text("Controllo gli annunci InfoCamere...")
    try:
        jobs = await asyncio.to_thread(infocamere.get_job_listings)
    except Exception as e:
        log.exception("Errore /infocamere")
        await update.message.reply_text(f"Errore nel recupero degli annunci: {e}")
        return

    text = infocamere.build_listing_message(jobs)
    for chunk in infocamere.split_message(text):
        await update.message.reply_text(
            chunk, parse_mode=ParseMode.HTML, link_preview_options=NO_PREVIEW
        )


async def infocamere_periodic_check(context):
    """Job periodico: avvisa il canale se il numero di annunci e' cambiato."""
    try:
        message, count = await asyncio.to_thread(infocamere.check_for_changes)
    except Exception as e:
        log.warning("Controllo InfoCamere fallito: %s", e)
        return

    if message is None:
        log.info("InfoCamere: nessuna variazione (%s annunci)", count)
        return

    log.info("InfoCamere: numero annunci cambiato -> %s, invio notifica", count)
    await context.bot.send_message(
        chat_id=key.INFOCAMERE_CHANNEL_ID,
        text=message,
        parse_mode=ParseMode.HTML,
        link_preview_options=NO_PREVIEW,
    )


# ----------------------------------------------------------------------------
# Setup
# ----------------------------------------------------------------------------
# Menu che Telegram mostra quando scrivi "/" nella chat: tengo solo i comandi
# "seri". Tutti gli altri (/alcaldo, /triviale, /fantasia, /jesolo, /waifu, /help)
# continuano a funzionare scrivendoli a mano, semplicemente non compaiono in lista.
# I nomi devono essere minuscoli (Telegram accetta solo a-z, 0-9 e _).
MENU_COMANDI = [
    ("gpt", "Chiedi qualcosa a Gemini"),
    ("genpanda", "Meme panda con il tuo testo"),
    ("infocamere", "Annunci di lavoro InfoCamere"),
]


async def _post_init(application):
    """Registra il menu dei comandi su Telegram all'avvio."""
    try:
        await application.bot.set_my_commands(
            [BotCommand(nome, descrizione) for nome, descrizione in MENU_COMANDI]
        )
        log.info("Menu comandi registrato (%s voci)", len(MENU_COMANDI))
    except Exception as e:
        log.warning("Non sono riuscito a registrare il menu comandi: %s", e)


def build_application():
    application = Application.builder().token(key.API_KEY).post_init(_post_init).build()

    # Commands
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))

    application.add_handler(CommandHandler("GenPanda", GenPanda_command))
    application.add_handler(CommandHandler("alcaldo", alcaldo_command))
    application.add_handler(CommandHandler("triviale", triviale_command))
    application.add_handler(CommandHandler("fantasia", fantasia_command))
    application.add_handler(CommandHandler("jesolo", jesolo_command))
    # application.add_handler(CommandHandler("find", find_command))
    application.add_handler(CommandHandler("gpt", gpt_command))
    # application.add_handler(CommandHandler("aiimg", aiimg_command))
    application.add_handler(CommandHandler("waifu", waifu_command))
    application.add_handler(CommandHandler("infocamere", infocamere_command))

    # Risposte ai messaggi normali (non comandi): scommenta per attivare
    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.add_error_handler(error_handler)

    # Controllo automatico annunci InfoCamere
    minutes = int(getattr(key, "INFOCAMERE_CHECK_MINUTES", 0) or 0)
    if minutes > 0:
        if application.job_queue is None:
            log.warning(
                "JobQueue non disponibile: installa python-telegram-bot[job-queue] "
                "per il controllo automatico InfoCamere"
            )
        else:
            application.job_queue.run_repeating(
                infocamere_periodic_check,
                interval=minutes * 60,
                first=30,
                name="infocamere_check",
            )
            log.info("Controllo InfoCamere ogni %s minuti", minutes)

    return application


def main():
    application = build_application()
    log.info("Bot avviato. Ctrl+C per fermarlo.")
    application.run_polling(drop_pending_updates=True)


######################################
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception:
        traceback.print_exc()
        print("\nIl bot si e' fermato per un errore (vedi sopra).")
        input("Premi INVIO per chiudere...")
