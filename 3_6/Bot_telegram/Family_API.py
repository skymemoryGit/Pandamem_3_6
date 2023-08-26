# -*- coding: utf-8 -*-
"""
Created on Sat May 20 17:35:57 2023

@author: Ye Jian_cheng
"""
import json
import text_on_img 
import random




def get_waifu_url(): #METODO MAIN DA CHIAMARE
    import requests
    
    api_result = requests.get('https://api.waifu.im/search')
    #print(api_result.content)
    # Parse the JSON response
    data = json.loads(api_result.content)
    
    # Access the source URL
    source_url = data['images'][0]['url']
    print("Source URL:", source_url)
    return source_url



def get_waifu_image_and_download(nomefile):
    
    import requests
    
    # Replace the URL below with the URL of the image you want to download
    url = get_waifu_url()
    
    # Send an HTTP GET request to the image URL
    response = requests.get(url)
    
    # Extract the filename from the URL
    filename = nomefile
    
    # Open a file in binary write mode and write the contents of the response to it
    with open("img/waifu/"+filename, "wb") as f:
        f.write(response.content)
    
    print(f"Image downloaded as {filename}")
    
    
def crea_immagine_waifu_Text(text):
    index=random.randint(0, 48)
    text_on_img.crea_Image_with_Text("img/waifu/prova_testo.png","img/waifu/"+"prova_"+str(index)+".png", text)

   

#crea_immagine_waifu_Text("Sono le 10, basta lavorare, state al caldo \n-cit pandamem!")

#for i in range(10,50):
#    get_waifu_image_and_download("prova_"+str(i)+".png")
#    text_on_img.crea_Image_with_Text("img/waifu/prova_testo.png","img/waifu/"+"prova_"+str(i)+".png", "")
    
    
