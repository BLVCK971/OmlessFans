import asyncio
from asyncio.windows_events import NULL
from typing import Optional

from playwright.async_api import async_playwright, expect

import logging
import src.config as config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

async def get_accountdetails(siret, nom, prenom, pwd) -> tuple[str, str, str]:
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

                await page.wait_for_timeout(500)
                # Vérification des erreurs de connexion

                try:
                    await expect(page.get_by_text("Vous avez ")).to_have_count(0)
                except:
                    logger.error("Trop de tentative sur ce compte. Veuillez patienter")
                    attempt = config.MAX_RETRIES - 1
                    raise Exception("Trop de tentative sur ce compte. Veuillez patienter")


                try:
                    await expect(page.get_by_role("heading", name="Erreur rencontr")).to_have_count(0)
                except:
                    logger.error("MDP Incorrect ou périmé")
                    attempt = config.MAX_RETRIES - 1
                    raise Exception("MDP Incorrect ou périmé")
                    

                try:
                    await expect(page.get_by_text("Votre mot de passe arrivera")).to_have_count(0)
                except:
                    logger.warning("Changement du MDP à faire !!!")

                # Récupération des détails du compte
                await page.locator("#btn-espace-connecte-modal span").first.click()
                await page.get_by_role("img", name="Modifier vos coordonnées").click()

                tel = await page.get_by_label("Téléphone *").input_value()
                telp = await page.get_by_text("Tél. portable").input_value()

                mail = await page.get_by_label("Adresse électronique *", exact=True).input_value()

                await context.close()
                await browser.close()
                
                return tel,telp,mail

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