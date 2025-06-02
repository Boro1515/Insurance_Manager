# api.server.py
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from mysql_database import (
    get_all_insured,
    add_insured,
    delete_insured,
    update_insured,
    get_insured_by_id
)

app = FastAPI()

# Define input data model
class Insured(BaseModel):
    jmeno: str
    prijmeni: str
    vek: int
    telefon: str

# GET all insured people
@app.get("/insured")
def get_insured():
    try:
        result = get_all_insured()
        return [
            {"id": r[0], "jmeno": r[1], "prijmeni": r[2], "vek": r[3], "telefon": r[4]}
            for r in result
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# POST - Add new insured
@app.post("/insured", status_code=status.HTTP_201_CREATED)
def add_insured_api(person: Insured):
    try:
        add_insured(person.jmeno, person.prijmeni, person.vek, person.telefon)
        return {"message": "Pojištěnec úspěšně přidán."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# DELETE - Remove insured by ID
@app.delete("/insured/{insured_id}")
def delete_insured_api(insured_id: int):
    try:
        existing = get_insured_by_id(insured_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Pojištěnec nebyl nalezen.")
        
        delete_insured(insured_id)
        return {"message": f"Pojištěnec s ID {insured_id} byl smazán."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# PUT - Update insured by ID
@app.put("/insured/{insured_id}")
def update_insured_api(insured_id: int, person: Insured):
    try:
        existing = get_insured_by_id(insured_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Pojištěnec nebyl nalezen.")
        
        update_insured(insured_id, person.jmeno, person.prijmeni, person.vek, person.telefon)
        return {"message": f"Pojištěnec s ID {insured_id} byl aktualizován."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
