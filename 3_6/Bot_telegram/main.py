# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 15:13:17 2023

@author: Ye Jian_cheng
"""
import random
import time
from random import choice
from glob import glob
import costant as key
import Responses as r
from telegram.ext import *
import nest_asyncio
import Openai_Dalle_E_img_model as openai_img

from bing_image_downloader import downloader
import  TelegramPushFunction as telegram_Push_Audio   #quest modulo alternativo send audio


import img_down as bing_downloader
nest_asyncio.apply()

import text_on_img as toi
import chatgpt as gpt
import Family_API
#import auto_relply_quotes as autoreply  #quando parte server main, parte anche il servio auto reply QUOTES .)

print("Bot start")

async def start_commmand(update, context):
    await update.message.reply_text("Welcome to PandaMem world, Let's rock it")
    await update.message.reply_text("/help to show what we can do! :)")




def help_cmd(update,context):
    update.message.reply_text("scrivi qualcosa")


async def handle_message(update,context ):
    txt=str(update.message.text).lower()
    ris=r.sample_response(txt )

    update.message.relpy_text(ris)


def error(update,context):
    print(f"Update {update} caused cerror {context.error}")


async def help_command(update, context):
    await update.message.reply_text("List available cmd :\n"
                                    "/help \n"

                                    "/alcaldo \n"
                                    "/triviale \n"
                                    "/fantasia \n"
                                    "/GenPanda \n"
                                    "/gpt \n"
                                    "/jesolo \n"
                                    "/waifu \n"






                                    )



async def zanon_command(update, context):
    await update.message.reply_text("Zanon? No join No potato per lui :(")


async def zanonScarso_command(update, context):
    #await update.message.reply_text("Ecco cosa ne penso")

    ls=[1,2,3,4,5,6,7]
    index=random.choice(ls)
    fileaudio="audio/zanon_"+str(6)+".mp3"  #scelgo sempre la sei va... metti index se vuoi varianti
    telegram_Push_Audio.reply_audio(fileaudio,"-1001941753443","Ecco cosa ne penso")








async def alcaldo_command(update, context):
    #await update.message.reply_text("Quanto ""al caldo"" siete trivialmente oggi da 0-5?")
    img=choice(glob("img/alcaldo/*.PNG"))
    await update.message.reply_photo(img)


async def fantasia_command(update, context):
    img=choice(glob("img/fantasia/*.jpg"))
    await update.message.reply_photo(img)

async def aiimg_command(update, context):
    arg=context.args

    s=""
    for i in arg:
        s=s+" "+i

    if(s==""):
        s="write something\nafter /aiImg"
        await update.message.reply_text(s)
    else:

        await update.message.reply_text("funzia e ora implementalo")





async def jesolo_command(update, context):

    arg=context.args

    s="idol porn javh"
    #for i in arg:
        #s=s+" "+i

    #print(s)

    #bing_downloader.Download_Image(s,"img/pythonImgDownload",10)

    #path="img/pythonImgDownload/"+s+"/Image_1.jpg"
    #print("path: ",path)
    #img=choice(glob("img/pythonImgDownload/"+s+"/Image_*.jpg"))
    img=choice(glob("img/jesolo/*.jpg"))

    #print(img)
    await update.message.reply_text("Ecco a te Jeppsolo")
    await update.message.reply_photo(img)
    #bing_downloader.remove_directory

async def find_command(update, context):

    arg=context.args

    s=""
    for i in arg:
        s=s+" "+i

    if(s==""):
        s="write something\nafter /find"
        await update.message.reply_text(s)
    else:
        n=3 #n immagini

        bing_downloader.Download_Image(s,"img/pythonImgDownload",n)
        for i in range(1,n+1):

            img=img=choice(glob("img/pythonImgDownload/"+s+"/Image_"+str(i)+".jpg"))
            await update.message.reply_photo(img)
            #print(i)
        bing_downloader.remove_directory("img/pythonImgDownload/")

    #print(s)
    #path="img/pythonImgDownload/"+s+"/Image_1.jpg"
    #print("path: ",path)
    #img=choice(glob("img/pythonImgDownload/"+s+"/Image_*.jpg"))


    #print(img)
    #await update.message.reply_photo(img)
    #bing_downloader.remove_directory


async def GenPanda_command(update, context):
    arg=context.args


    s=""   # in sto caso s è il testo dato dall'utente
    for i in arg:
        s=s+" "+i


    if(s==""):
        s="write something\nafter /genpanda"
    #print(s)
    #await update.message.reply_text(s)

    img=choice(glob("img/pandamem/*.png"))
    toi.creaCustomPandaMeme(img, s)
    await update.message.reply_photo("img/pandamem/result.png")  #mandi indietro result




async def waifu_command(update, context):
    arg=context.args


    s=""   # in sto caso s è il testo dato dall'utente
    for i in arg:
        s=s+" "+i


    if(s==""):
        img=choice(glob("img/waifu/prova_*.png"))
        await update.message.reply_photo(img)

    #print(s)
    #await update.message.reply_text(s)


    Family_API.crea_immagine_waifu_Text(s)
    #time.sleep(10)
    await update.message.reply_photo("img/waifu/prova_testo.png")  #mandi indietro result





async def eco_command(update, context):
    #await update.message.reply_text("Quanto ""al caldo"" siete trivialmente oggi da 0-5?")
    #await update.message.reply_text("prova eco")

    arg=context.args

    s=""
    for i in arg:
        s=s+" "+i

    print(s)
    await update.message.reply_text(s)






async def triviale_command(update, context):
    #await update.message.reply_text("Quanto ""al caldo"" siete trivialmente oggi da 0-5?")
    img=choice(glob("img/triviale/*.PNG"))
    await update.message.reply_photo(img)

async def lina_command(update, context):
    #await update.message.reply_text("Quanto ""al caldo"" siete trivialmente oggi da 0-5?")
    img=choice(glob("img/lina/*.png"))
    await update.message.reply_photo(img)

async def gpt_command(update, context):
    arg=context.args


    s=""   # in sto caso s è il testo dato dall'utente
    for i in arg:
        s=s+" "+i


    if(s==""):
        s="write something\nafter /gpt"
        await update.message.reply_text(s)
    else:
        print(s)
        ris_daGpt=gpt.GetRispostaGpt(s)
        print(ris_daGpt)
        await update.message.reply_text(ris_daGpt)

    #print(s)
    #await update.message.reply_text(s)







def main():
    application = Application.builder().token(key.API_KEY).build()

    # Commands
    application.add_handler(CommandHandler('start', start_commmand))
    application.add_handler(CommandHandler('help', help_command))

    application.add_handler(CommandHandler('eco',eco_command))

    application.add_handler(CommandHandler('zanon', zanon_command))
    application.add_handler(CommandHandler('zanonScarso', zanonScarso_command))
    application.add_handler(CommandHandler('GenPanda', GenPanda_command))
    application.add_handler(CommandHandler('alcaldo', alcaldo_command))
    application.add_handler(CommandHandler('triviale', triviale_command))
    application.add_handler(CommandHandler('fantasia', fantasia_command))
    application.add_handler(CommandHandler('lina', lina_command))
    application.add_handler(CommandHandler('jesolo', jesolo_command))
    #application.add_handler(CommandHandler('find', find_command))
    application.add_handler(CommandHandler('gpt', gpt_command))
    #application.add_handler(CommandHandler('aiimg', aiimg_command))
    application.add_handler(CommandHandler('waifu', waifu_command))


    # create bot instance
    # import necessary libraries






    # Run bot
    application.run_polling()

######################################
main()