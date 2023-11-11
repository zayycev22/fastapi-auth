from fastapi_auth.strategies.base import Strategy


class DbStrategy(Strategy):
    def __init__(self, token_repo):
        self.token_repo = token_repo
