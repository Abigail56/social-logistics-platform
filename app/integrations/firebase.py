class FirebaseClient:
    """Placeholder Firebase client for notifications and realtime updates."""

    def __init__(self, project_id: str | None = None):
        self.project_id = project_id

    def send_notification(self, device_token: str, message: str) -> dict:
        return {
            "device_token": device_token,
            "message": message,
            "status": "queued",
        }
