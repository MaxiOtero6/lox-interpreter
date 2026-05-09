class ReturnException(Exception):
    def __init__(self, value):
        super().__init__(f"Return with value {value}")
        self.value = value