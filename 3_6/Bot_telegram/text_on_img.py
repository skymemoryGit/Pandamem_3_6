# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 16:44:04 2023

@author: Ye Jian_cheng
"""
# Importing the PIL library
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from random import choice
from glob import glob

# Open an Image


import numpy as np
from PIL import Image, ImageDraw, ImageFont






def creaCustomPandaMeme(img,testo): #questo metodo prende img e testo e crea uno nuovo di nome result.png
    # Open input image


    #print(len(testo))

    if(len(testo)>15):
        parole=testo.split(" ")

        static_world= parole[0]+" "+parole[1]+" "+parole[2]+" \n"

        testoacapo=""
        for i in range(3,len(parole)):
            testoacapo= testoacapo+parole[i]+" "
        #print(testoacapo)

        final=static_world+testoacapo
        #print(final)

        testo=final


    im = Image.open(img).convert('RGB')

    # Get a drawing context
    draw = ImageDraw.Draw(im)

    pixellat=ImageFont.truetype("FreeMono",48)
    draw.text((45, 20),testo,(0,0,0),font=pixellat)


    # Save
    im.save('img/pandamem/result.png')


def crea_Image_with_Text(urlsave,img,testo): #questo metodo prende img e testo e crea uno nuovo di nome result.png
    # Open input image


    #print(len(testo))

    if(len(testo)>15):
        parole=testo.split(" ")

        static_world= parole[0]+" "+parole[1]+" "+parole[2]+" \n"

        testoacapo=""
        for i in range(3,len(parole)):
            testoacapo= testoacapo+parole[i]+" "
        #print(testoacapo)

        final=static_world+testoacapo
        #print(final)

        testo=final


    im = Image.open(img).convert('RGB')

    # Get a drawing context
    draw = ImageDraw.Draw(im)



    font=ImageFont.truetype("FreeMono",100)

    text = testo

    # get text size
    text_size = font.getsize(text)

    # set button size + 10px margins
    button_size = (text_size[0]+230, text_size[1]+260)

    # create image with correct size and black background
    button_img = Image.new('RGBA', button_size, "gray")

    # put text on button with 10px margins
    button_draw = ImageDraw.Draw(button_img)
    x=30
    y=10
    button_draw.text((x, y), text, font=font,fill=(35, 235, 155, 128))

    # put button on source image in position (0, 0)
    im.paste(button_img, (x-10, y-20))
    '''
    x=100
    y=30
    text=testo
    font=ImageFont.truetype("verdana",150)
    shadowcolor=fill=(35, 235, 155, 128)
    #draw.text((45, 20),testo,(0,0,0),font=pixellat)
    draw.rectangle(((0, 00), (100, 100)), fill="black")
    draw.text((x, y),text , font=font, fill=(35, 235, 155, 128))
    draw.text((x-1, y-1), text, font=font, fill=shadowcolor)
    draw.text((x+1, y-1), text, font=font, fill=shadowcolor)
    draw.text((x-1, y+1), text, font=font, fill=shadowcolor)
    draw.text((x+1, y+1), text, font=font, fill=shadowcolor)
    '''
    # Save
    im.save(urlsave)

creaCustomPandaMeme("img/pandamem/hhh.png", "zanon è un frocio di merda")

