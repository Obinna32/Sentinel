import requests
import os

SQUAD_SECRET_KEY = "sandbox_sk_9d8e846d8cc8be31e8ba484e5d4d30a4ddbf8e013d1b"
URL_BASE = "https://sandbox-api-d.squadco.com"

def initiate_escrow(amount, shipment_id):
    url = f"{URL_BASE}/transaction/initiate"
    headers = {"Authorization": f"Bearer {SQUAD_SECRET_KEY}"}
    payload = {
        "amount": int(amount * 100), #In kobo
        "email": "buyer@gmail.com",
        "currency": "NGN",
        "initiate_type": "inline",
        "transaction_ref": f"SENTINEL-{shipment_id}"
    }
    return requests.post(url, json=payload, headers=headers).json()

def payout_to_supplier(amount, bank, acc, shipment_id):
    url = f"{URL_BASE}/transfer"
    headers = {"Authorization": f"Bearer {SQUAD_SECRET_KEY}"}
    payload = {
        "amount": int(amount * 100), #In kobo
        "bank_name": bank,
        "account_number": acc,
        "transaction_ref": f"PAY-{shipment_id}",
        "remark": "Product Verified. Payment released."
    }
    return requests.post(url, json=payload, headers=headers).json()
