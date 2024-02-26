from typing import Type, Awaitable, Any, Callable
from fastapi_auth.utils.utils import prepare_kwargs


class Signal:
    def __init__(self):
        self._after_create: dict[type, list] = {}
        self._before_create: dict[type, list] = {}
        self._signals: list[Signal] = []

    def subscribe_signals(self, *signals) -> None:
        self._signals.extend(*signals)

    def after_save(self, model: Type):
        def wrapper(receiver: Awaitable):
            if model not in self._after_create.keys():
                self._after_create[model] = []
            self._after_create[model].append(receiver)
            return receiver

        return wrapper

    async def emit_after_save(self, instance: Any, created: bool = False, **kwargs) -> None:
        instance_type = type(instance)
        for signal in self._signals:
            if instance_type in signal._after_create:
                for receiver in signal._after_create[instance_type]:
                    await receiver(instance, created, **prepare_kwargs(receiver, kwargs))


main_signal = Signal()
