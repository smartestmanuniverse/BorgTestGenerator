#coding: utf-8
from ..assistant import Assistant
import re

class py3UnitTestFileWriter(object):
    def __init__(self, assistant_id=None) -> None:
        if assistant_id:
            # 1. Créer une instance de l'assistant
            self.assistant = Assistant(assistant_id=f"{assistant_id}")
        else:
            self.assistant = Assistant(assistant_id=None)
        
        # 2. Charger l'assistant
        self.assistant.load_assistant()

    def upload_files(self, vector_store_name, files_to_upload):
        # 3. Upload des fichiers
        self.assistant.upload_files(files_to_upload, f"{vector_store_name}")

        # 4. Mettre à jour l'assistant avec le vector store
        self.assistant.update_assistant_with_vector_store()
        return self

    def create_new_thread(self):
        # 5. Créer un thread
        self.assistant.create_thread()
        return self

    def create_new_user_message(self, message_type, message_content):
        # 6. Créer un message
        self.assistant.create_message("user", "Écrit le code du fichier test correspondant a ce script python")
        return self

    def run(self):
        # 7. Créer un run
        self.assistant.create_run()
        return self

    def print_assistant_result(self):
        # 8. Récupérer les messages de l'assistant
        print(self.assistant.get_assistant_messages())
        return self
    
    def get_assistant_result(self):
        return self.assistant.get_assistant_messages()

    def save_assistant_response_to_file(self, file_path, remove_block_delimiters=False):
        data = self.assistant.get_assistant_messages()

        if remove_block_delimiters == True:
            # Verifie si la premiere ligne contient des caracteres de debut de bloc ( doit commencer par et contenir au moins 3 caracteres "```" ) ; alors supprime la ligne, sinon laisse la ligne
            if re.match(r'^```{3,}', data.split('\n')[0]):
                data = '\n'.join(data.split('\n')[1:])
            
            # Verifie si la derniere ligne contient des caracteres de fin de bloc ( doit contenir au moins 3 caracteres "```" ) ; alors supprime la ligne, sinon laisse la ligne
            if re.match(r'^```{3,}', data.split('\n')[-1]):
                data = '\n'.join(data.split('\n')[:-1])
            
        # 9. Sauvegarder la réponse de l'assistant dans un fichier
        with open(file_path, 'w') as out_file:
            out_file.write(data)
            out_file.close()
        
        return self
    

