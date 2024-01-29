from typing import Type, Awaitable, Any, Callable
from fastapi_auth.utils.utils import prepare_kwargs


class Signal:
    def __init__(self):
        self._after_create: dict[type, list] = {}
        self._before_create: dict[type, list] = {}
        self._signals: list[Signal] = []

    def subscribe_signals(self, *signals) -> None:
        self._signals.extend(*signals)

    def before_create(self, model: Type):
        def wrapper(receiver: Awaitable):
            if model not in self._before_create.keys():
                self._before_create[model] = []
            self._before_create[model].append(receiver)
            return receiver

        return wrapper

    def after_create(self, model: Type):
        def wrapper(receiver: Awaitable):
            if model not in self._after_create.keys():
                self._after_create[model] = []
            self._after_create[model].append(receiver)
            return receiver

        return wrapper

    def disconnect(self, model: Type) -> Callable:
        def wrapper(receiver: Callable) -> Callable:
            if model in self._before_create:
                self._before_create[model].remove(receiver)
            if model in self._after_create:
                self._after_create[model].append(receiver)
            return receiver

        return wrapper

    async def emit_before_create(self, instance: Any, created: bool = False, **kwargs) -> None:
        instance_type = type(instance)
        for signal in self._signals:
            if instance_type in signal._before_create:
                for receiver in signal._before_create[instance_type]:
                    await receiver(instance, created, **prepare_kwargs(receiver, kwargs))

    async def emit_after_create(self, instance: Any, created: bool = False, **kwargs) -> None:
        instance_type = type(instance)
        for signal in self._signals:
            if instance_type in signal._after_create:
                for receiver in signal._after_create[instance_type]:
                    await receiver(instance, created, **prepare_kwargs(receiver, kwargs))


main_signal = Signal()
