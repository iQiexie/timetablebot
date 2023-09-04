class EmptyArgumentsError(RuntimeError):
    def __init__(self, arguments: tuple[str]):
        msg = f"Provide at least one argument of {arguments}"
        super().__init__(msg)
