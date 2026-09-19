# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 19:21:39 2023

@author: Ye Jian_cheng

/gpt - usa la libreria openai >= 1.0 (client nuovo).
La chiave va messa in costant.OPENAI_API_KEY (o variabile d'ambiente OPENAI_API_KEY).
"""
import os

import costant as key

_client = None


def _get_client():
    global _client
    if _client is None:
        from openai import OpenAI   # import qui: se manca la libreria fallisce solo /gpt
        api_key = getattr(key, "OPENAI_API_KEY", "") or os.environ.get("OPENAI_API_KEY", "")
        if not api_key:
            raise RuntimeError("chiave OpenAI non configurata (costant.OPENAI_API_KEY)")
        _client = OpenAI(api_key=api_key)
    return _client


def GetRispostaGpt(query):
    client = _get_client()
    response = client.chat.completions.create(
        model=getattr(key, "OPENAI_MODEL", "gpt-4o-mini"),
        messages=[{"role": "user", "content": query}],
    )
    return response.choices[0].message.content


# ris=GetRispostaGpt("mi riassumi la prima guerra mondiale in poche parole")
# print(ris)
