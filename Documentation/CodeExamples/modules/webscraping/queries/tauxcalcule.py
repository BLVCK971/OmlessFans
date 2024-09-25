import logging
import requests
import src.config as config

lg = logging.getLogger()
lg.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s;%(levelname)s;%(message)s;')

async def get_tauxCalcule(sessionID : str, siren : str, nic : str, de : str, dt : str, se : str):
    lg.info("Requête d'extraction 'tauxCalcule' : "+ siren+ nic+ se)
    cookies = dict(JSESSIONID = sessionID)
    form_data = {"siren": siren, "nic": nic, "se" : se, "de" : de , "dt": dt}
    r = requests.get(config.SCRAPER_URL_AMELI_ELEMENT_TAUX_CALCULE, cookies = cookies, params = form_data)
    
    if r.ok == False or r.status_code != 200:
        raise Exception("La requête d'extraction des tauxCalcule à échouée")
    lg.info("Récupération réussie")
    return r.json()