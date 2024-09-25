from typing import Optional

from pydantic import BaseModel,  field_validator


class AccountBase(BaseModel):
    siret : str
    nom : str
    prenom : str
    password : str

    @field_validator("siret")
    def siret_validator(cls, v):
        assert v.isnumeric()
        if len(v) != 14:
            raise ValueError("Le siret doit être une valeur de 14 chiffres")
        return v