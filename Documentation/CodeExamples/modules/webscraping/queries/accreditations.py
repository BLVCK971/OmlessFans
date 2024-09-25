import logging
from typing import List, Optional
import src.config as config
import requests

lg = logging.getLogger()
lg.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s;%(levelname)s;%(message)s;')

async def get_accreditations(nom : str, prenom : str, siret : str):

    lg.info("Accréditations : Requête ")
    headers = {"nom": nom, "prenom": prenom, "siret": siret}
    r = requests.post(config.SCRAPER_URL_AMELI_SIRETS, headers = headers)
    
    if r.ok == False or r.status_code != 200:
        raise Exception("La requête d'extraction des sirets à échouée : Not OK response")
    if r.headers['content-type'] != "application/json":
        raise Exception("La requête d'extraction des sirets à échouée : Target didn't send a valid json")


    lg.info("Accréditations : Récupération réussie")
    return r.json()

