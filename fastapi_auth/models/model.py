class ExternalBaseModel:
    def __call__(cls, *args, **kwargs):
        if cls.__name__ == 'ExternalBaseModel':
            raise TypeError(f"Cannot instantiate class {cls.__name__}")
        return super().__call__(*args, **kwargs)

    @classmethod
    def create(cls, **kwargs):
        raise NotImplementedError(f"FastApiAuth doesn't provide a DB representation for {cls.__class__.__name__}.")

    def save(self, created: bool = False, **kwargs):
        raise NotImplementedError(f"FastApiAuth doesn't provide a DB representation for {self.__class__.__name__}.")

    def delete(self, **kwargs):
        raise NotImplementedError(f"FastApiAuth doesn't provide a DB representation for {self.__class__.__name__}.")
