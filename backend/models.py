from database import Base
from sqlalchemy import Integer, Float, DateTime, String, Column
import datetime

class Shipment(Base):
    __tablename__ = "shipments"
    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String)
    amount = Column(Float)
    supplier_bank_name = Column(String)
    supplier_acc_num = Column(String)
    status = Column(String, default="PENDING_PAYMENT")
    ai_score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)