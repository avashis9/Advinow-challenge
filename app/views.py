from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from sqlalchemy.orm import Session
from typing import Optional, List
import csv
import io
from starlette.responses import JSONResponse

from models import Business, Symptom, BusinessSymptom
from database import get_db

router = APIRouter()


@router.get("/business-symptoms")
def get_business_symptoms(
        business_id: Optional[int] = None,
        diagnostic: Optional[bool] = None,
        db: Session = Depends(get_db)
):
    """
    Get business symptoms data with optional filtering by business_id and/or diagnostic value
    """
    query = (
        db.query(
            Business.id.label("business_id"),
            Business.name.label("business_name"),
            Symptom.code.label("symptom_code"),
            Symptom.name.label("symptom_name"),
            BusinessSymptom.diagnostic
        )
        .join(BusinessSymptom, Business.id == BusinessSymptom.business_id)
        .join(Symptom, BusinessSymptom.symptom_code == Symptom.code)
    )

    if business_id is not None:
        query = query.filter(Business.id == business_id)

    if diagnostic is not None:
        query = query.filter(BusinessSymptom.diagnostic == diagnostic)

    results = query.all()

    return [
        {
            "business_id": row.business_id,
            "business_name": row.business_name,
            "symptom_code": row.symptom_code,
            "symptom_name": row.symptom_name,
            "symptom_diagnostic": row.diagnostic
        }
        for row in results
    ]


@router.post("/import-csv")
async def import_csv(
        file: UploadFile = File(...),
        db: Session = Depends(get_db)
):
    """
    Import business symptom data from a CSV file
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")

    def normalize_bool(val):
        return str(val).strip().lower() in ["true", "yes", "1"]

    contents = await file.read()
    buffer = io.StringIO(contents.decode('utf-8'))
    csv_reader = csv.DictReader(buffer)

    businesses = {}
    symptoms = {}
    business_symptoms = []

    for row in csv_reader:
        business_id = int(row["Business ID"])
        business_name = row["Business Name"]
        symptom_code = row["Symptom Code"]
        symptom_name = row["Symptom Name"]
        diagnostic = normalize_bool(row["Symptom Diagnostic"])

        if business_id not in businesses:
            businesses[business_id] = business_name

        if symptom_code not in symptoms:
            symptoms[symptom_code] = symptom_name

        business_symptoms.append({
            "business_id": business_id,
            "symptom_code": symptom_code,
            "diagnostic": diagnostic
        })

    for business_id, business_name in businesses.items():
        if not db.query(Business).filter(Business.id == business_id).first():
            db.add(Business(id=business_id, name=business_name))

    for symptom_code, symptom_name in symptoms.items():
        if not db.query(Symptom).filter(Symptom.code == symptom_code).first():
            db.add(Symptom(code=symptom_code, name=symptom_name))

    db.commit()

    for bs in business_symptoms:
        exists = db.query(BusinessSymptom).filter_by(
            business_id=bs["business_id"],
            symptom_code=bs["symptom_code"]
        ).first()
        if not exists:
            db.add(BusinessSymptom(**bs))

    db.commit()

    return {"message": "Successfully imported business symptom data."}


@router.get('/status')
async def get_status():
    try:
        return {"Health OK"}

    except Exception as e:
        return {'Error: ' + str(e)}
