from fastapi import FastAPI, HTTPException
from typing import List

from models import Verb, VerbCreate
from data import VERBS

app = FastAPI(title="German Verb Notebook API")


def sort_verbs():
    VERBS.sort(key=lambda v: v.word.lower())


@app.get("/verbs", response_model=List[Verb])
def get_verbs():
    """
    获取所有动词，按字母顺序排列
    """
    sort_verbs()
    return VERBS


@app.get("/verbs/{verb_id}", response_model=Verb)
def get_verb(verb_id: int):
    """
    获取单个动词详情
    """
    for verb in VERBS:
        if verb.id == verb_id:
            return verb
    raise HTTPException(status_code=404, detail="Verb not found")


@app.post("/verbs", response_model=Verb)
def create_verb(payload: VerbCreate):
    """
    新增动词
    """
    new_id = max(v.id for v in VERBS) + 1 if VERBS else 1

    new_verb = Verb(
        id=new_id,
        word=payload.word,
        meaning=payload.meaning,
        conjugations=payload.conjugations,
    )

    VERBS.append(new_verb)
    sort_verbs()
    return new_verb
