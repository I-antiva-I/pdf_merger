
from typing import Callable, Dict, List, Any

from enums.message_type import MessageType


class Subscription:
    def __init__(self, subscriber: object, action: Callable):
        self.subscriber: object = subscriber
        self.action: Callable = action


class MessageManager:
    subscriptions: Dict[MessageType, List[Subscription]] = {}

    @classmethod
    def subscribe(cls, message_type: MessageType, subscriber: object, action: Callable) -> None:
        if message_type not in cls.subscriptions:
            cls.subscriptions[message_type] = list()

        subscription = Subscription(subscriber, action)
        cls.subscriptions[message_type].append(subscription)

    @classmethod
    def unsubscribe(cls, message_type: MessageType, subscriber: object) -> None:
        if message_type in cls.subscriptions:
            cls.subscriptions[message_type] = [sub for sub in cls.subscriptions[message_type]
                                               if sub.subscriber != subscriber]

    @classmethod
    def send(cls, message_type: MessageType, *args: Any, **kwargs: Any) -> None:
        if message_type not in cls.subscriptions:
            return

        for subscription in cls.subscriptions[message_type]:
            try:
                subscription.action(*args, **kwargs)
            except Exception as e:
                print(f"Unexpected error: {e} during {message_type}")


