# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 10:02:26 2023

@author: Ye Jian_cheng
"""
import openai
openai.api_key ="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"

def get_image_url_openai(input_string):
    response = openai.Image.create(
        prompt=input_string,
        n=1,
        size="1024x1024"
        
        )
    
    image_url=response['data'][0]['url']
    return image_url



def Gen_AI_image_and_download(prompt,nomefile):
    
    import requests
    
    # Replace the URL below with the URL of the image you want to download
    url = get_image_url_openai(prompt)
    
    # Send an HTTP GET request to the image URL
    response = requests.get(url)
    
    # Extract the filename from the URL
    filename = nomefile
    
    # Open a file in binary write mode and write the contents of the response to it
    with open("generato/"+filename, "wb") as f:
        f.write(response.content)
    
    print(f"Image downloaded as {filename}")
    
    
    
    
    



try:
    Gen_AI_image_and_download("2 girl eat cake ", "prova.png")
    

except Exception as e: 
    print("non accetto")
    
