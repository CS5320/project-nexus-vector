from .events import DomainEvent


class NotificationClient:
    def __init__(self) -> None:
        self.sent_messages: list[tuple[str, str]] = []

    def send(self, email: str, message: str) -> None:
        self.sent_messages.append((email, message))


class CustomerNotificationSubscriber:
    """A cleaner event-driven notification path used by newer operations."""

    def __init__(self, client: NotificationClient) -> None:
        self.client = client

    def handle(self, event: DomainEvent) -> None:
        email = event.payload.get("email")
        if not email:
            return

        if event.event_type == "customer.created":
            self.client.send(email, f"Welcome to Atlas, {event.payload.get('name', 'customer')}!")
        elif event.event_type == "customer.deactivated":
            self.client.send(email, f"Your Atlas account has been deactivated: {event.payload.get('reason', '')}")
