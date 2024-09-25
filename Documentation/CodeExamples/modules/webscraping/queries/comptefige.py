import logging
import requests
import src.config as config

lg = logging.getLogger()
lg.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s;%(levelname)s;%(message)s;')

async def get_CEFigees(sessionID : str, siren : str, nic : str, dt : str, se : str, aproNoRisque : str):
    lg.info("Requête d'extraction 'CEFigées' : "+ siren+ nic+ se)
    cookies = dict(JSESSIONID = sessionID)
    form_data = {"siren": siren, "nic": nic, "se" : se, "de" : "" , "dt": dt,"aproNoRisque" : aproNoRisque}
    r = requests.get(config.SCRAPER_URL_AMELI_CF, cookies = cookies, params = form_data)
    
    if r.ok == False or r.status_code != 200:
        raise Exception("La requête d'extraction des CEFigées à échouée")
    lg.info("Récupération réussie")
    return r.json()