# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 10:02:26 2023

@author: Ye Jian_cheng

Generazione immagini con DALL-E (libreria openai >= 1.0).
Non viene importato da main.py: usalo a parte se ti serve.
La chiave va in costant.OPENAI_API_KEY.
"""
import os

import costant as key


def _client():
    from openai import OpenAI
    api_key = getattr(key, "OPENAI_API_KEY", "") or os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        raise RuntimeError("chiave OpenAI non configurata (costant.OPENAI_API_KEY)")
    return OpenAI(api_key=api_key)


def get_image_url_openai(input_string):
    response = _client().images.generate(
        prompt=input_string,
        n=1,
        size="1024x1024",
    )
    return response.data[0].url


def Gen_AI_image_and_download(prompt, nomefile):
    import requests

    url = get_image_url_openai(prompt)
    response = requests.get(url, timeout=60)

    os.makedirs("generato", exist_ok=True)
    with open(os.path.join("generato", nomefile), "wb") as f:
        f.write(response.content)

    print(f"Image downloaded as {nomefile}")


if __name__ == "__main__":
    try:
        Gen_AI_image_and_download("2 girl eat cake ", "prova.png")
    except Exception as e:
        print("non accetto:", e)
