from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
import models, database, squad_service, ai_vision, shutil


app = FastAPI()

@app.post("/create-shipment")
def create(product: str, amount: float, bank_name: str, acc: str, db: Session = Depends(database.get_db)):
    shipment = models.Shipment(product_name=product, amount=amount, supplier_bank_name = bank_name, supplier_acc_num=acc)
    db.add(shipment)
    db.commit()
    db.refresh(shipment)

    squad = squad_service.initiate_escrow(amount, shipment.id)
    return {"id": shipment.id, "payment_url": squad['data']['checkout_url']}

@app.post("/verify/{shipment_id}")
async def verify(shipment_id: int, file: UploadFile = File(...), db: Session = Depends(database.get_db)):
    shipment = db.query(models.Shipment).filter(models.Shipment.id == shipment_id).first()
    path = f"uploads/{file.filename}"
    with open(path, "wb") as buffer: shutil.copyfileobj(file.file, buffer)

    score = ai_vision.compare_images("reference.jpg", path)
    shipment.ai_score = score

    if score > 85:
        shipment.status = "VERIFIED"
        squad_service.payout_to_supplier(shipment.amount, shipment.supplier_bank_name, shipment.supplier_acc_num, shipment.id)
        shipment.status = "RELEASED"
        db.commit()
        return {"status": "AUTHENTIC", "score": score, "action": "Payment Released"}
    
    shipment.status = "REJECTED"
    db.commit()
    return {"status": "COUNTERFEIT", "score": score, "action": "Payment Frozen"}