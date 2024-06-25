class MissingConfigError(Exception):
    def __init__(self, missing_config: str) -> None:
        msg: str = f"Service is missing required config: {missing_config}."
        super().__init__(msg)
