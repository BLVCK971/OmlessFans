from fastapi import APIRouter, status
from src.modules.webscraping.schemas import AccountBase
import src.modules.webscraping.services as services

import logging

router = APIRouter()

lg = logging.getLogger()
lg.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s;%(levelname)s;%(message)s;")

@router.post("/account-details")
async def get_account_details(account: AccountBase):
    lg.info("Début récupération de la liste des Taux du client")
    details = await services.get_account_details(
        account.siret, account.nom, account.prenom, account.password)
    return details


@router.post("/sirens")
async def get_siren_list(account: AccountBase) :

    sirenlist = await services.get_siren_list(
        account.siret, account.nom, account.prenom, account.password)
    
    return sirenlist

@router.post("/sirets")
async def get_siret_list(account: AccountBase) :

    siretlist = await services.get_siret_list(
        account.siret, account.nom, account.prenom
    )
    return siretlist


@router.post("/ce-courants")
async def get_ce_courants(account: AccountBase):
    lg.info("Début récupération de la liste des CECourants")

    CECList = await services.get_ce_courants(
        account.siret, account.nom, account.prenom, account.password)
    return CECList


@router.post("/taux")
async def get_taux(account: AccountBase):
    lg.info("Début récupération de la liste des Taux du client")

    TauxList = await services.get_taux(
        account.siret, account.nom, account.prenom, account.password)
    return TauxList


