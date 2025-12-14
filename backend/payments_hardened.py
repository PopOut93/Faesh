from marketplace import Marketplace
from ai_personalization import AIPersonalization
from avatar_engine import Avatar

class PaymentsHardened:
    def __init__(self, marketplace: Marketplace, personalization: AIPersonalization):
        self.marketplace = marketplace
        self.personalization = personalization
        self.transactions = []

    def process_payment(self, avatar: Avatar, product_id: int, payment_info: dict):
        # Placeholder: real system would encrypt and validate payment
        product = next((p for p in self.marketplace.products if p.id == product_id), None)
        if not product:
            raise ValueError("Product not found")
        # Simple fraud check
        if payment_info.get("amount") != product.price:
            raise ValueError("Payment amount mismatch – possible fraud")
        txn = {
            "user_id": avatar.user_id,
            "product_id": product_id,
            "amount": payment_info.get("amount"),
            "status": "approved"
        }
        self.transactions.append(txn)
        return txn
