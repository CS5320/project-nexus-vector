from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class DomainEvent:
    event_type: str
    customer_id: str
    payload: dict[str, str]


class EventSubscriber(Protocol):
    def handle(self, event: DomainEvent) -> None:
        ...


class EventBus:
    """Small observer-style event dispatcher."""

    def __init__(self) -> None:
        self._subscribers: list[EventSubscriber] = []
        self.published: list[DomainEvent] = []

    def subscribe(self, subscriber: EventSubscriber) -> None:
        self._subscribers.append(subscriber)

    def publish(self, event: DomainEvent) -> None:
        self.published.append(event)
        for subscriber in list(self._subscribers):
            subscriber.handle(event)
