#coding: utf-8
from ..assistant import Assistant

class py3UnitTestFileWriter(object):
    def __init__(self, assistant_id=None) -> None:
        if assistant_id:
            # 1. Créer une instance de l'assistant
            self.assistant = Assistant(assistant_id=f"{assistant_id}")
        else:
            self.assistant = Assistant(assistant_id=None)
        
        # 2. Charger l'assistant
        self.assistant.load_assistant()

