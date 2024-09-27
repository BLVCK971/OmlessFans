-- OmlessesForFanInActualPeriod(fanid : Fan):
-- Objectif : avoir une liste des Omless Actif du Fan
SELECT omless_id FROM DON as D WHERE D.fan_id = fanid AND D.start_date < now() AND D.end_date > now()

-- OmlessesNotPayedForFan(fanid : Fan):
-- Objectif : avoir une liste des Omless passé qui ne sont plus d'actualité mais qui ont déjà perçu des dons
SELECT omless_id FROM DON as D WHERE D.fan_id = fanid AND NOT D.start_date < now() AND NOT D.end_date > now()

-- SumDonForOmlessOfFan 
-- Objectif : 

-- SumDonForOmless
-- Objectif : 

-- SumDonFromFan
-- Objectif : 

-- VideosFromOmless
-- Objectif : Lorsqu'on veut charger toutes les vidéos d'une page de Omless

-- VideosFromOmlessByCategory
-- Objectif : Lorsqu'on veut avoir une vidéo de présentation vs tel ou tel vidéo spécifique

-- VideoFromOmlessByDon
-- Objectif : Lorsque l'on charge un don spécifique, affichage de la vidéo de l'Omless

-- VideoFromFanByDon
-- Objectif : Lorsque l'on charge un don spécifique, affichage de la vidéodu Fan