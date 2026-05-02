from typing import Dict, Optional
from pydantic import BaseModel


Person = str  # ich / du / er / wir / ihr / sie


class Tense(BaseModel):
    ich: Optional[str] = None
    du: Optional[str] = None
    er: Optional[str] = None
    wir: Optional[str] = None
    ihr: Optional[str] = None
    sie: Optional[str] = None


class Indikativ(BaseModel):
    prasens: Optional[Tense] = None
    prateritum: Optional[Tense] = None
    perfekt: Optional[Tense] = None


class Conjugations(BaseModel):
    indikativ: Optional[Indikativ] = None


class Verb(BaseModel):
    id: int
    word: str
    meaning: str
    conjugations: Optional[Conjugations] = None


class VerbCreate(BaseModel):
    word: str
    meaning: str
    conjugations: Optional[Conjugations] = None
