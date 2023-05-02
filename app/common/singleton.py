class Singleton:

    instance = None

    def __new__(cls):
        if cls.isinstance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        if Singleton.isinstance is None:
            Singleton.instance = self
