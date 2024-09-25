


from datetime import datetime, timedelta
import json
import logging
import os
from typing import Optional

import src.config as config

lg = logging.getLogger()
lg.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s;%(levelname)s;%(message)s;')







async def save_sessionID(siret, sessionId : Optional[str],netetoken : Optional[str], expiration : str):
    expiration = (datetime.now() + timedelta(minutes=15)).strftime("%d%m%Y-%H-%M-%S")
    session = {"SessionId" : sessionId,"netetoken" : netetoken, "Expired" : expiration}
    folder_path = config.DATA_PATH +'/' + config.PROJECT_NAME +'/sirets/' + siret 
    await VerifyIfDirExistElseCreate(folder_path)
    with open(folder_path + '/sessionID_','w') as fw :
        fw.write(json.dumps(session, indent=4, default=str))
        fw.close()
        
async def get_valid_SessionID(siret: str) -> tuple[Optional[str],Optional[str]] : 
    file_path = config.DATA_PATH +'/' + config.PROJECT_NAME +'/sirets/' + siret + '/sessionID_'
    if os.path.exists(file_path):
        with open(file_path,'r') as fr :
            content = json.loads(fr.read())
            if datetime.strptime(content["Expired"],"%d%m%Y-%H-%M-%S") < datetime.now():
                return "",""
            else:
                return content["SessionId"] , content["netetoken"]
    else:
        return None,None
    
async def verify_file_exist(file):
    return os.path.isfile(file)

async def VerifyIfDirExistElseCreate(dir : str):
    if not os.path.isdir(dir):
        os.makedirs(dir)