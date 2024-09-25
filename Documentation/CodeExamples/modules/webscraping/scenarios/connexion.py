import asyncio
from typing import Optional

from playwright.async_api import async_playwright, expect

import logging
import src.config as config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

async def Authentification(siret, nom, prenom, pwd) -> tuple[str,str]:
    validate_input(siret, nom, prenom, pwd)
    for attempt in range(config.MAX_RETRIES):
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=False)
                context = await browser.new_context()
                page = await context.new_page()

                await page.goto("https://www.net-entreprises.fr/", timeout=config.TIMEOUT)
                
                # Use try-except for each interaction to handle potential issues
                try:
                    await page.get_by_role("button", name="Tout accepter").click(timeout=config.TIMEOUT)
                except:
                    logger.warning("Cookie acceptance button not found or not clickable")

                await page.get_by_role("banner").get_by_text("Votre compte").click(timeout=config.TIMEOUT)
                await page.get_by_label("Siret").fill(siret, timeout=config.TIMEOUT)
                await page.get_by_label("Nom", exact=True).fill(nom, timeout=config.TIMEOUT)
                await page.get_by_label("Prénom").fill(prenom, timeout=config.TIMEOUT)
                await page.get_by_label("Mot de passe").fill(pwd, timeout=config.TIMEOUT)
                await page.get_by_role("button", name="Je me connecte").click(timeout=config.TIMEOUT)
                
                
                # Vérification des erreurs de connexion
                ## Vérification excès de tentatives
                try:
                    await expect(page.get_by_text("Vous avez ")).to_be_hidden(timeout=500)
                except:
                    logger.error("Trop de tentative sur ce compte. Veuillez patienter")
                    attempt = config.MAX_RETRIES - 1
                    raise Exception("Trop de tentative sur ce compte. Veuillez patienter")

                ## Vérification du MDP périmé ou invalide
                try:
                    await expect(page.get_by_role("heading", name="Erreur rencontrée")).to_be_hidden(timeout=500)
                except:
                    logger.error("MDP Incorrect ou périmé")
                    attempt = config.MAX_RETRIES - 1
                    raise Exception("MDP Incorrect ou périmé")
                    
                ## Vérification du MDP à changer
                try:
                    await expect(page.get_by_text("Votre mot de passe arrivera")).to_be_hidden(timeout=500)
                except:
                    logger.warning("Changement du MDP à faire !!!")

                # Accès Compte ATMP
                async with page.expect_popup() as page1_info:
                    await page.get_by_role("link", name="Consulter ses taux AT/MP").click(timeout=config.TIMEOUT)
                page1 = await page1_info.value
                
                ## Vérification des CGU à valider
                try:
                    await expect(page1.get_by_text("À propos des conditions générales d'utilisation Conditions d'utilisation du tél")).to_be_hidden(timeout=500)
                except:
                    logger.error("CGU à valider")
                    attempt = config.MAX_RETRIES - 1
                    raise Exception("CGU à valider")

                await page1.get_by_text("Consulter les AT/MP passés").click(timeout=config.TIMEOUT)

                cookies = await context.cookies()
                jsessionID = next((x["value"] for x in cookies if x["name"] == "JSESSIONID"), None) # type: ignore
                netetoken = next((x["value"] for x in cookies if x["name"] == "JTD"), None) # type: ignore
                if not jsessionID:
                    raise Exception("JSESSIONID not found in cookies")
                if not netetoken:
                    raise Exception("netetoken not found in cookies")

                await context.close()
                await browser.close()
                return jsessionID,netetoken

        except Exception as e:
            logger.error(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt == config.MAX_RETRIES - 1:
                raise
            await asyncio.sleep(2 ** attempt)  # Exponential backoff
    raise


def validate_input(siret, nom, prenom, mdp):
    if not siret.isdigit() or len(siret) != 14:
        raise ValueError("SIRET must be a 14-digit number")
    if not nom or not prenom or not mdp:
        raise ValueError("Nom, prénom, and mdp cannot be empty")