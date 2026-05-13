from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models, database, squad_service, ai_vision
app = FastAPI()

@app.post("/create-shipment")
def create(product: str, amount: float, bank_name: str, acc: str, db: Session = Depends(database.get_db)):
    shipment = models.Shipment(product_name=product, amount=amount, supplier_bank_name = bank_name, supplier_acc_num=acc)
    db.add(shipment)
    db.commit()
    db.refresh(shipment)

    squad = squad_service.initiate_escrow(amount, shipment.id)
    return {"id": shipment.id, "payment_url": squad['data']['checkout_url']}