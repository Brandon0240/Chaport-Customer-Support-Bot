import app.vector_longformer_chaport as vl

class AskService:
    _initialized = False

    @classmethod
    def initialize(cls):
        if not cls._initialized:
            vl.initialize()
            cls._initialized = True

    @classmethod
    def ask(cls, question: str) -> str:
        cls.initialize()
        return vl.ask(question)
