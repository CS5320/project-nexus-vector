class NotificationClient:
    def __init__(self) -> None:
        self.sent_messages: list[tuple[str, str]] = []

    def send(self, email: str, message: str) -> None:
        self.sent_messages.append((email, message))
