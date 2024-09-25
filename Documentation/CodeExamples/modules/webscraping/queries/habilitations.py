import logging
from typing import List, Optional
import uuid
import src.config as config
import requests
from urllib.parse import unquote

lg = logging.getLogger()
lg.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s;%(levelname)s;%(message)s;')

async def get_habilitations(nom : str, prenom : str, siret : str, nettoken : str):
    headers = {
        "nete-token" : unquote(nettoken), 
        "x-api-key" : config.X_API_KEY,
        "correlation-id" : str(uuid.uuid1())
        }
    
    r1 = requests.get(config.SCRAPER_URL_AMELI_JWTTOKEN,headers = headers)

    headers = {"Authorization" : "Bearer " + str(r1.content)[2:-1], "nom": nom, "prenom": prenom, "siret": siret}
    r2 = requests.get(config.SCRAPER_URL_AMELI_SIRENS, headers = headers)
    
    if r2.ok == False or r2.status_code != 200:
        raise Exception("La requête d'extraction des sirens à échouée : Not OK response")
    if r2.headers['content-type'] != "application/json":
        raise Exception("La requête d'extraction des sirens à échouée : Target didn't send a valid json")


    lg.info("Récupération réussie")
    return r2.json()

