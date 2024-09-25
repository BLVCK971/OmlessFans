import logging
from datetime import datetime, timedelta
from typing import List, Optional


from .queries.decisionstaux import get_decisionsTaux
from .queries.habilitations import get_habilitations
from .queries.cecourants import get_cptEmplDyn
from .queries.accreditations import get_accreditations
from .queries.tauxcalcule import get_tauxCalcule
from .queries.comptefige import get_CEFigees

from src.modules.storage.services import get_valid_SessionID, save_sessionID

from .scenarios.connexion import Authentification
from .scenarios.getaccountdetails import get_accountdetails


lg = logging.getLogger()
lg.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s;%(levelname)s;%(message)s;")


async def get_sessionID(siret: str, nom: str, prenom: str, password: str) -> tuple[str,str] :
    lg.info("Récupération du SessionID")
    expiration = (datetime.now() + timedelta(minutes=30)).strftime("%d%m%Y-%H-%M-%S")
    sessionID, netetoken = await get_valid_SessionID(siret)
    if sessionID and netetoken:
        lg.info("SessionID en Cache : Récupération réussie")
        return sessionID, netetoken
    else:
        lg.info("Récupération du SessionID via Scraping")
        sessionId, netetoken = await Authentification(siret, nom, prenom, password)
        lg.info("SessionID : Récupération réussie")
        await save_sessionID(siret, sessionId,netetoken, expiration)
        return sessionId,netetoken
    
async def get_account_details(siret: str, nom: str, prenom: str, password: str):
    lg.info("Récupération des détails du compte")
    details = {}
    details["tel"],details["telp"],details["mail"] = await get_accountdetails(siret, nom, prenom, password)
    lg.info("AccountDetails : Récupération réussie")
    return details

async def get_siren_list(siret: str, nom: str, prenom: str, password : str):
    lg.info("Récupération des entreprises et établissements du compte")
    _, netetoken = await get_sessionID(siret, nom, prenom, password)
    habilitations = await get_habilitations(nom, prenom, siret,netetoken)
    lg.info("entreprises : Récupération réussie")
    return habilitations

async def get_siret_list(siret: str, nom: str, prenom: str):
    lg.info("Récupération des établissements du compte")
    accreditations = await get_accreditations(nom, prenom, siret)
    lg.info("établissements : Récupération réussie")
    return accreditations   


async def get_ce_courants(siret: str, nom: str, prenom: str, password : str):
    sessionId,netetoken = await get_sessionID(siret, nom, prenom, password)
    lg.info("Récupération des entreprises du compte")
    habilitations = await get_habilitations(nom, prenom, siret,netetoken)
    lg.info("Nombre entreprises : " + str(len(habilitations)))
    CECList = []
    for ent in habilitations:
        siren = ent['siren']
        lg.info("Entreprise : " + siren)
        lg.info("Nombre établissements de l'entreprise : " + str(len(ent["etablissements"])))
        for etb in ent["etablissements"]:
            nic = etb['siret'][9:]
            lg.info("Etablissement : " + siren + nic)
            jsonCEC = await get_cptEmplDyn(sessionId,siren,nic)
            CECList.extend(jsonCEC)
    return CECList


async def get_taux(siret: str, nom: str, prenom: str, password : str):
    sessionId,netetoken = await get_sessionID(siret, nom, prenom, password)
    habilitations = await get_habilitations(nom, prenom, siret,netetoken)
    TauxList = []
    for ent in habilitations:
        siren = ent['siren']
        lg.info("Entreprise : " + siren)
        lg.info("Nombre établissements de l'entreprise : " + str(len(ent["etablissements"])))
        for etb in ent["etablissements"]:
            nic = etb['siret'][9:]
            lg.info("Etablissement : " + siren + nic)
            jsonTaux = await get_decisionsTaux(sessionId,siren,nic)
            for taux in jsonTaux["listTaux"] :
                dateEffet = str(datetime.fromtimestamp(int(taux["tseDtEffet"]/1000)).strftime('%d%m%Y'))
                taux["tauxCalcule"] = await get_tauxCalcule(sessionId, siren, nic, dateEffet, taux["dateTraitement"], taux["se"])
                taux["CEFigées"] = await get_CEFigees(sessionId, siren, nic, taux["dateTraitement"], taux["se"], taux["aproNoRisque"])
            TauxList.append(jsonTaux)
    return TauxList
