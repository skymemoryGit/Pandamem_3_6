# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 18:10:10 2023

@author: Ye Jian_cheng
"""
import requests
import TelegramPushFunction as telegramPushfunction
import meteo as meteo
import concurrent.futures
import Family_API

def numero_a_giorno(numero):
    giorni_settimana = {
        1: "lunedì",
        2: "martedì",
        3: "mercoledì",
        4: "giovedì",
        5: "venerdì",
        6: "sabato",
        7: "domenica"
    }
    return giorni_settimana[numero]

def get_Diz_quotes():
    import json

    # Open the JSON file and load the data
    with open('quotes/quotes2.json', encoding="utf-8") as f:
        data = json.load(f)

    # Create an empty list to store the quotes
    quotes = []

    # Loop through each quote in the data
    import unicodedata
    for quote in data:
        # Extract the text and author of the quote
        text = quote['text']
        fixed_text= unicodedata.normalize("NFC", text)
        author = quote['author']
        # Add the quote to the list as a dictionary
        quotes.append({'text': text, 'author': author})

    return quotes





def random_numbers(dim):
    import random
    return (random.randint(0, dim), random.randint(0, dim), random.randint(0, dim))

def invioQuotes(idchat):
    diz=get_Diz_quotes()
    a,b,c = random_numbers(len(diz)-1)
    quote = diz[a]
    quote2= diz[b]
    quote3=diz[c]
    formatted_string = "Here the quotes of day \n\n"f'{quote["text"]}\n- {quote["author"]}\n\n\n'f'{quote2["text"]}\n- {quote2["author"]}\n\n\n'f'{quote3["text"]}\n- {quote3["author"]}\n'
    print(formatted_string)

    response = telegramPushfunction.send_telegram_message(idchat, formatted_string)
    print(response)



def start_work(idchat):
    import time
    import datetime

    idchat=idchat
    print("Servizio InvioQuotes Start in:"+idchat)
    telegramPushfunction.send_telegram_message("-950282631", "Avvio servizio auto-reply")
    while True:

        current_time = time.strftime("%H:%M")
        #print(current_time)
        #print("Sono le",current_time)
        now = datetime.datetime.now()
        print("Current date and time:", now)
        import datetime

        # Get the current date and time
        current_date = datetime.datetime.now()
        # Get the day of the week (0 = Monday, 6 = Sunday)
        day_of_week = current_date.weekday() +1  #parte da 0... meglio 1 lunedi e 2 martedi...
        print(current_date)
        print("Oggi è giorno settimana:",day_of_week)
        print("Sono le",current_time)




        if(current_time=="06:00"):#current_time=="06:00"
            print("entrato")
            giorno=numero_a_giorno(day_of_week)

            #Family_API.crea_immagine_waifu_Text("Buongiorno Principesse Triviali, Ecco il meteo e quotes per la giornata \n-Pandamem")
            #telegramPushfunction.send_telegram_image("img/waifu/prova_testo.png", idchat)

            #telegramPushfunction.send_telegram_message(idchat, "Buongiorno Principesse Triviali, sono le 8:00 , Ecco il meteo e quotes per la giornata")
            telegramPushfunction.send_telegram_message(idchat,meteo.get_meteo_info("verona") )
            #telegramPushfunction.send_telegram_message(idchat,meteo.get_meteo_info("scorzè") )
            #telegramPushfunction.send_telegram_message(idchat,meteo.get_meteo_info("padova") )

            invioQuotes(idchat)
            telegramPushfunction.send_telegram_message(idchat, "Buon " + giorno+", Principesse Triviali, Ecco il meteo e quotes per la giornata \n-Pandamem")
            if(day_of_week==6 or day_of_week==7):
                telegramPushfunction.send_telegram_message(idchat, "E'WEEKEND, NON SI LAVORA, SI GODE! ")

        if(current_time=="18:00" and day_of_week!=6 and day_of_week!=7):
            telegramPushfunction.send_telegram_message(idchat, "Buonasera Pandames come è stata la giornata(di merda?), VI SOLLEVO IO IL MORALE CON FRASI ora è:\n"+str(now))
            invioQuotes(idchat)
            #creo img waifu
            Family_API.crea_immagine_waifu_Text("Andrà tutto bene e Triviale! \n-Pandamem")

            telegramPushfunction.send_telegram_image("img/waifu/prova_testo.png", idchat)

        if(current_time=="11:00" and day_of_week!=6 and day_of_week!=7):
            for i in range(0,1):
                #creo img waifu
                Family_API.crea_immagine_waifu_Text("basta lavorare,pranzo time \n-Pandamem")
                telegramPushfunction.send_telegram_image("img/waifu/prova_testo.png", idchat)

                invioQuotes(idchat)

        if(current_time=="08:30" and day_of_week!=6 and day_of_week!=7 ):
            for i in range(0,1):
                telegramPushfunction.send_telegram_message(idchat, "Sono le 10:30, BASTA LAVORARE, pausa time e state al caldo")
                #creo img waifu
                Family_API.crea_immagine_waifu_Text("Sono le 10, basta lavorare state al caldo \n-Pandamem")
                telegramPushfunction.send_telegram_image("img/waifu/prova_testo.png", idchat)

        if(current_time=="02:00" and day_of_week!=6 and day_of_week!=7 ):
            print("off")
            #telegramPushfunction.send_telegram_message(idchat, " Sono le 4.00, vado a dormire che tra due ore devo prendere treno Bologna-Padova ")

        if(current_time=="22:00"):
            print("off")
            #telegramPushfunction.send_telegram_message(idchat, " Bene, sono le 0.00, vado a lavorare. Faccio un tiro fino le sei e poi treno")
            #creo img waifu
            Family_API.crea_immagine_waifu_Text("Buona notte Triviali! \n-Pandamem")
            #time.sleep(15)
            #telegramPushfunction.send_telegram_image("img/waifu/prova_testo.png", idchat)



        s="Waiting for the next Quotes renewal...at min'8.00 and 20:00"
        print(s)
        #return s #!!!!non fai ritornare nulla cosi continua XD


        time.sleep(60)  #fa uno sleep cosi almeno è sicuro che fa solo 1 volta il task se dovesse finire entro 1 min
        print("__________________________________")

with concurrent.futures.ThreadPoolExecutor() as worker :
    print("ok")
    #w1=worker.submit(start_work,"-1001496914346") #zibaldone
    w2=worker.submit(start_work,"-976517142") #pandamemm group  # -976517142 NEW jesolo group
    w3=worker.submit(start_work,"-985535170") #venezia
    #w4=worker.submit(start_work,"-950282631") #t1 prova



    #print(w1.result())
    print(w2.result())
    print(w3.result())
    #print(w4.result())


################################################################



#t1=start_work("-1001496914346")  # zibaldone =-1001496914346, pandmemem = -1001941753443 #venezia="-985535170"

#t2=start_work("-1001941753443")




