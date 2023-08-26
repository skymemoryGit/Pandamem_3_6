import requests
import time
import meteo as meteo





def reply_audio(file,chatid,caption): 
    base_url = "https://api.telegram.org/bot5994787878:AAFWZpMQ4FkuPpBko0uwL9_6n1zWbID0hmM/sendAudio"
    my_file = open(file, "rb")
    parameters = {
        "chat_id" : chatid,  #questo è il codice chat lo trovi con RAWDATABOT BOT DI TELEGRAM AGGIUNGENDO IN CHAT
        "caption" : caption
    }
    
    files = {
        "audio" : my_file
    }
    
    resp = requests.get(base_url, data = parameters, files=files)
    print(resp.text)
    


def send_telegram_message(chat_id, text):
    base_url = "https://api.telegram.org/bot5994787878:AAFWZpMQ4FkuPpBko0uwL9_6n1zWbID0hmM/sendMessage"
    parameters = {
        "chat_id": chat_id,
        "text": text
    }
    resp = requests.get(base_url, params=parameters)
    return resp.text


def send_telegram_image(file,chat_id):
    base_url = "https://api.telegram.org/bot5994787878:AAFWZpMQ4FkuPpBko0uwL9_6n1zWbID0hmM/sendPhoto"
    parameters = {
        "chat_id" : chat_id,  #questo è il codice chat lo trovi con RAWDATABOT BOT DI TELEGRAM AGGIUNGENDO IN CHAT
        
    }
    my_file = open(file, "rb")
    files = {
    "photo" : my_file
    }
    resp = requests.get(base_url, data = parameters, files=files)
    print(resp.text)
    

    
#reply_audio("prova.mp3","-1001941753443" , "here is an audio file for you")
#send_telegram_message("-1001941753443",meteo.get_meteo_info("scorzè") )
#send_telegram_image("img/waifu/prova_testo.png","-1001941753443")