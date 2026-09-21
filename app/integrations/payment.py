class PaymentGateway:
    """Placeholder payment integration for transaction processing."""

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key

    def create_intent(self, amount: float, currency: str = "USD") -> dict:
        return {
            "amount": amount,
            "currency": currency,
            "status": "pending",
        }

    def verify(self, payment_reference: str) -> dict:
        return {
            "payment_reference": payment_reference,
            "status": "verified",
        }
