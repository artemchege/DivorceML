
class Observer:
    """ Implementation of observer pattern, event handling """

    subscribers = dict()

    @classmethod
    def subscribe(cls, event_type: str, fn):
        if event_type not in cls.subscribers:
            cls.subscribers[event_type] = []
        cls.subscribers[event_type].append(fn)

    @classmethod
    async def post_event(cls, event_type: str, data: dict):
        if event_type not in cls.subscribers:
            return
        for fn in cls.subscribers[event_type]:
            await fn(data)
