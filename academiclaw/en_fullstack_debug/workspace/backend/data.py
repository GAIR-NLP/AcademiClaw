from models import Verb, Conjugations, Indikativ, Tense

VERBS: list[Verb] = [
    Verb(
        id=1,
        word="gehen",
        meaning="走",
        conjugations=Conjugations(
            indikativ=Indikativ(
                prasens=Tense(
                    ich="gehe",
                    du="gehst",
                    er="geht",
                    wir="gehen",
                    ihr="geht",
                    sie="gehen",
                ),
                prateritum=Tense(
                    ich="ging",
                    du="gingst",
                    er="ging",
                    wir="gingen",
                    ihr="gingt",
                    sie="gingen",
                ),
                perfekt=Tense(
                    ich="bin gegangen",
                    du="bist gegangen",
                    er="ist gegangen",
                    wir="sind gegangen",
                    ihr="seid gegangen",
                    sie="sind gegangen",
                ),
            )
        ),
    )
]
