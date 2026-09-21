class EmailClient:
    """Placeholder email client for outbound notifications."""

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key

    def send(self, to_email: str, subject: str, body: str) -> dict:
        return {
            "to": to_email,
            "subject": subject,
            "body": body,
            "status": "queued",
        }
