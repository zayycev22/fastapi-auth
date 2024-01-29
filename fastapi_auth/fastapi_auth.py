from fastapi_auth.signals.signal import Signal, main_signal


class FastApiAuth:
    def __init__(self):
        self._main_signal = main_signal

    def listen_signals(self, *signals: Signal) -> None:
        self._main_signal.subscribe_signals(signals)

