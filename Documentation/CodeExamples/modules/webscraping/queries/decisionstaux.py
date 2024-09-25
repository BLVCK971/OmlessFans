import logging
import requests
import src.config as config

lg = logging.getLogger()
lg.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s;%(levelname)s;%(message)s;')

async def get_decisionsTaux(sessionID : str, siren : str, nic : str):
    cookies = dict(JSESSIONID = sessionID)
    form_data = {"siren": "", 
                 "nic": "",
                 "se": "", 
                 "de" : "", 
                 "dt" : "", 
                 "isTauxEnVigueur" : "", 
                 "init" : "O", 
                 "indexDeb" : "0", 
                 "indexFin" : "2500",
                 "siret" : siren + nic,
                 "orderSiret" : "ASC",
                 "orderDtTrait" : "DESC"}
    r = requests.get(config.SCRAPER_URL_AMELI_TX, cookies = cookies, params = form_data)
    
    if r.ok == False or r.status_code != 200:
        raise Exception("La requête d'extraction desdecisionsTaux à échouée")
    lg.info("Récupération réussie")
    return r.json()