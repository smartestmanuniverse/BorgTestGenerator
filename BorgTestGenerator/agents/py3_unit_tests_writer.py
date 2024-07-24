#coding: utf-8
from ..assistant import Assistant

import os


def codeBlocksParser(data: str|bytes, language: str|bytes|list|None = None) -> list:
    import re
    # function to convert bytes to string
    def bytes_to_string(data: bytes) -> str:
        return data.decode()

    # function with regex to match code blocks into a string
    def match_code_blocks(data: str|bytes) -> list:
        return re.findall(r"```(.+?)```", data, re.DOTALL)

    # function to match single code blocks
    def match_single_code_blocks(data: str|bytes) -> list:
        # individual blocks delimited on same line only matched
        # exemple delimited : "`command line --option`"
        # the individual block is matched if it is on the same line, 
        # and after the delim of beginning and before the delim of end no "`" is found withoyt line return found
        return re.findall(r"`([^`\n]+)`", data)

    def split_code_block(code_block: str) -> dict:
        block = code_block.split('\n')
        # remove the first line if it is empty
        # and define the language if it is not defined
        if block[0] == '':
            language = None
            block = block[1:]
        elif block[0] != '':
            language = block[0]
            block = block[1:]
        # remove the last line if it is empty
        if block[-1] == '':
            block = block[:-1]
        return {
            'language': language,
            'code': '\n'.join(block)
        }

    def parse_blocks(data: str|bytes) -> dict:
        if type(data) == bytes:
            data = bytes_to_string(data)

        single_code_blocks = match_single_code_blocks(data)
        code_blocks = match_code_blocks(data)
        splited_code_blocks = [split_code_block(block) for block in code_blocks]
        return {
            'single_code_blocks': single_code_blocks,
            'code_blocks': splited_code_blocks
        }

    def keep_only_blocks_by_language(parsed_blocks: dict, language: str|bytes|list|None) -> dict:
        if language == None:
            return parsed_blocks
        elif type(language) == str:
            language = [language]
        elif type(language) == bytes:
            language = [language.decode()]

        keeped_blocks = []
        for parsed_block in parsed_blocks['code_blocks']:
            if parsed_block['language'] in language:
                keeped_blocks.append(parsed_block)
        return {
            'single_code_blocks': parsed_blocks['single_code_blocks'],
            'code_blocks': keeped_blocks
        }

    # ############# MAIN FUNCTION #############
    parsed_blocks = parse_blocks(data)
    return keep_only_blocks_by_language(parsed_blocks, language)


    



"""
IDEAS:

```python
    # Regex to match file paths and associated code blocks
    regex = r"(\S+)\n\s*```[^\n]*\n(.+?)```"
```

```python
# # Regex to match individual diff blocks
# r"```.*?\n\s*?--- .*?\n\s*?\+\+\+ .*?\n(?:@@ .*? @@\n(?:[-+ ].*?\n)*?)*?```",
        re.DOTALL
```

```python
    # Clean and standardize the file path
    path = re.sub(r'[\:<>"|?*]', "", match.group(1))
    path = re.sub(r"^\[(.*)\]$", r"\1", path)
    path = re.sub(r"^`(.*)`$", r"\1", path)
   
    path = re.sub(r"[\]\:]$", "", path)
```

```python
Parses the header of a hunk from a diff.
pattern = re.compile(r"^@@ -\d{1,},\d{1,} \+\d{1,},\d{1,} @@$")
```
"""


def read_text_file(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Le fichier {file_path} est manquant")
    
    with open(file_path, 'r') as in_file:
        return in_file.read()

class py3UnitTestFileWriter(object):
    def __init__(self, assistant_id=None):
        self.agent_model = "gpt-4o"
        self.agent_name = "py3UnitTestFileWriter"
        self.agent_act_as = read_text_file("agents/prompts/roles/linus_torvald.txt")
        self.agent_instructions = read_text_file("agents/prompts/instructions/py3_unit_tests_writer.txt")
        # 0. Définir l'assistant
        
        self.define_assistant(assistant_id)


    def define_assistant(self, assistant_id):
        if assistant_id == None:
            self.assistant = Assistant(assistant_id)
            self.assistant.create_assistant(self.agent_name, self.agent_instructions, self.agent_model, tool_code_interpreter=True, tool_file_search=True)
            self.assistant.load_assistant(self.assistant.get_assistant_id())
        else:
            self.assistant = Assistant(assistant_id)
            self.assistant.load_assistant()
        return self
    
    def search_and_retreive_assistant(self):
        self.assistant = Assistant(assistant_id=None)
        assistant = self.assistant.exact_search_assistant(
                                                            self.agent_name,
                                                            self.agent_model,
                                                            self.agent_instructions
                                                         )
        if assistant:
            self.define_assistant(assistant.id)
        else:
            self.define_assistant(None)
            self.define_assistant(self.assistant.create_assistant(self.agent_name, self.agent_instructions, self.agent_model, tool_code_interpreter=True).get_assistant_id())
        return self

    def upload_files(self, vector_store_name, files_to_upload):
        missing_files = [f for f in files_to_upload if not os.path.exists(f)]
        if missing_files:
            raise FileNotFoundError(f"Les fichiers suivants sont manquants : {missing_files}")
        
        print(f"Téléchargement des fichiers : {files_to_upload} vers {vector_store_name}")
        try:
            self.assistant.upload_files(files_to_upload, f"{vector_store_name}")
            print("Fichiers téléchargés avec succès.")
        except Exception as e:
            print(f"Erreur lors du téléchargement des fichiers : {e}")

        # 4. Mettre à jour l'assistant avec le vector store
        try:
            self.assistant.update_assistant_with_vector_store()
            print("Assistant mis à jour avec le vector store.")
        except Exception as e:
            print(f"Erreur lors de la mise à jour de l'assistant avec le vector store : {e}")
        return self


    def create_new_thread(self):
        print("Création d'un nouveau thread")
        self.assistant.create_thread()
        return self

    def create_new_user_message(self):
        print("Création d'un message utilisateur")
        self.assistant.create_message("user", "Écrit le code du fichier test correspondant a ce script python")
        return self

    def run(self):
        print("Exécution du run")
        self.assistant.create_run()
        return self

    def print_assistant_result(self):
        # 8. Récupérer les messages de l'assistant
        print(self.assistant.get_assistant_messages())
        return self
    
    def get_assistant_result(self):
        return self.assistant.get_assistant_messages()

    

    # #### [BEG] #### 
    # # [INCORRECT] #
    # def save_assistant_response_to_file(self, file_path, remove_block_delimiters=False):
    #     data = self.assistant.get_assistant_messages()
        
    #     if remove_block_delimiters:
    #         lines = data.split('\n')
    #         if re.match(r'.*```.*', lines[0]):
    #             lines = lines[1:]
    #         if re.match(r'.*```.*', lines[-1]):
    #             lines = lines[:-1]
    #         data = '\n'.join(lines)
        
    #     print(f"Sauvegarde de la réponse de l'assistant dans le fichier : {file_path}")
    #     with open(file_path, 'w') as out_file:
    #         out_file.write(data)
    #     return self
    # # [INCORRECT] #
    # #### [END] ####



