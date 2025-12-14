from payments_hardened import PaymentsHardened
from marketplace import Marketplace
from avatar_engine import Avatar

class FraudAIMonitor:
    def __init__(self, payments: PaymentsHardened, marketplace: Marketplace):
        self.payments = payments
        self.marketplace = marketplace
        self.suspicious_activity = []

    def monitor_transaction(self, avatar: Avatar, product_id: int, payment_info: dict):
        # Call existing payment processor
        txn = self.payments.process_payment(avatar, product_id, payment_info)
        # Simple fraud heuristic example
        if payment_info.get("amount") > 1000:  # arbitrary high amount
            txn["status"] = "flagged"
            self.suspicious_activity.append(txn)
        return txn

    def get_alerts(self):
        return self.suspicious_activity
