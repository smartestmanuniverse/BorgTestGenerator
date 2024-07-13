#!/usr/bin/env python3
#coding: utf-8

from openai import OpenAI
from os import getenv
from os import path
from os import makedirs
import json
import tempfile

class Assistant(object):
    def __init__(self, assistant_id):
        self.client = OpenAI(api_key=getenv("OPENAI_API_KEY"))
        self.assistant_id = assistant_id

    def load_assistant(self, assistant_id=None):
        if assistant_id:
            self.assistant_id = assistant_id
            self.assistant = self.client.beta.assistants.retrieve(f"{self.assistant_id}")
        return self
    
    def create_assistant(self, name, instructions, model="gpt-4o", tool_code_interpreter=False, tool_file_search=True):
        tools_ = []
        if tool_code_interpreter:
            tools_.append({"type": "code_interpreter"})
        if tool_file_search:
            tools_.append({"type": "file_search"})

        self.assistant = self.client.beta.assistants.create(
            name=f"{name}",
            instructions=f"{instructions}",
            tools=tools_,
            model=f"{model}"
        )
        return self
    
    def get_assistant_id(self):
        return self.assistant.id
    
    def get_assistant_name(self):
        return self.assistant.name
    
    def get_assistant_model(self):
        return self.assistant.model
    
    def get_assistant_instructions(self):
        return self.assistant.instructions
    
    def get_thread_id(self):
        return self.thread.id
    
    def list_assistants(self):
        args = {
            'after': None,
            'limit': 100,
            'order': 'asc',
            'timeout': 30
        }

        all_assistants = []
        while True:
            # Récupère la liste des assistants avec les arguments spécifiés
            response = self.client.beta.assistants.list(**args)
            assistants = response.data

            if not assistants:
                break

            all_assistants.extend(assistants)

            # Met à jour l'argument 'after' pour récupérer la page suivante
            args['after'] = assistants[-1].id

        return all_assistants
    
    def save_assistants_list(self, file_name):
        with open(file_name, 'w') as file:
            json.dump(self.list_assistants(), file)
        return self
    
    def print_assistants_list(self):
        all_assistants = self.list_assistants()
        for assistant in all_assistants:
            print(f"ID: {assistant.id}, Nom: {assistant.name}")
        return self
    
    def exact_search_assistant(self, name, model, instructions):
        assistants = self.list_assistants()
        for assistant in assistants:
            if assistant.name == name and assistant.model == model and assistant.instructions == instructions:
                return assistant
        return None

    def delete_assistant(self, assistant_id):
        self.client.beta.assistants.delete(assistant_id)
        return self

    def create_thread(self):
        self.thread = self.client.beta.threads.create()
        return self

    def create_message(self, role, content):
        self.message = self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role=f"{role}",
            content=f"{content}"
        )
        return self

    def create_run(self):
        self.run = self.client.beta.threads.runs.create_and_poll(
            assistant_id=self.assistant.id,
            thread_id=self.thread.id
        )
        return self

    def upload_files(self, files_to_upload, vector_store_name):
        if type(files_to_upload) == str:
            files_to_upload = [files_to_upload]


        # Create a vector store caled "Financial Statements"
        self.vector_store = self.client.beta.vector_stores.create(name=vector_store_name)
 
        # Ready the files for upload to OpenAI
        self.file_paths = files_to_upload
        self.file_streams = [open(path, "rb") for path in self.file_paths]
 
        # Use the upload and poll SDK helper to upload the files, add them to the vector store,
        # and poll the status of the file batch for completion.
        self.file_batch = self.client.beta.vector_stores.file_batches.upload_and_poll(
            vector_store_id=self.vector_store.id, files=self.file_streams
        )
 
        print(self.file_batch.status)
        print(self.file_batch.file_counts)
        return self

    def update_assistant_with_vector_store(self):
        self.assistant = self.client.beta.assistants.update(
            assistant_id = self.assistant.id,
            tool_resources = {"file_search": {"vector_store_ids": [self.vector_store.id]}},
        )
        return self

    def get_assistant_messages(self):
        if self.run.status == 'completed': 
            self.messages = self.client.beta.threads.messages.list(
                thread_id=self.thread.id
            )
            return self.messages.data[0].content[0].text.value
        else:
            return self.run.status


class AssistantBackupManager(object):
    def __init__(self, backup_file = "assistants_list.json", init_refresh = True):
        self.Assitant_Client = Assistant(assistant_id=None)
        self.assistants_list = []
        self.assistant_backup_file = f"{backup_file}"
        self.backup_folder = "/tmp/assistants_backup"
        if init_refresh:
            self.refresh_assistants_list()

    def refresh_assistants_list(self):
        self.assistants_list = []
        self.assistants_list = self.Assitant_Client.list_assistants()
        return self
    
    def save_assistants_from_list(self, backup_folder):
        with open(f"{backup_folder}/{self.assistant_backup_file}", 'w') as file:
            json.dump(self.assistants_list.to_json(), file)
        return self
    
    def delete_assistants_from_list(self):
        for assistant in self.assistants_list.data:
            self.Assitant_Client.delete_assistant(assistant.id)
        self.assistants_list = []
        return self
    
    def save_assistant(self, backup_folder, assistant_id, file_name):
        # function to convert the assistant object to json ( if you need you can import libraries to do this )
        def assistant_to_json(assistant_object):
            try: 
                json_assistant_data_ = {
                    "id": str(assistant_object.id),
                    "created_at": int(assistant_object.created_at),
                    "description": assistant_object.description,
                    "instructions": assistant_object.instructions,
                    "metadata": assistant_object.metadata,
                    "model": assistant_object.model,
                    "name": assistant_object.name,
                    "object": f"{assistant_object.object}",
                    "tools": assistant_object.to_dict()["tools"],
                    "response_format": assistant_object.response_format,
                    "temperature": assistant_object.temperature,
                    "tool_resources": assistant_object.tool_resources.to_dict(),
                    "top_p": assistant_object.top_p
                }
            except Exception as e:
                print( f"Error: {e}" )
                exit(1)

            try:
                json_assistant_data = json.dumps(json_assistant_data_ ,
                                                    indent=4,
                                                    sort_keys=False)
            except Exception as e:
                print( f"Error: {e}" )
                exit(1)        

            return json_assistant_data
        
        client = OpenAI(api_key=getenv("OPENAI_API_KEY"))
        assistant_object = client.beta.assistants.retrieve(assistant_id)
        assistant_object_data = assistant_to_json(assistant_object)
        # ##############################################
        #    Save the assistant object to a json file
        # ##############################################
        with open(f"{backup_folder}/{file_name}", 'w') as file:
            file.write(assistant_object_data)
            file.close()
        return self
    
    def delete_assistant(self, assistant_id):
        self.Assitant_Client.delete_assistant(assistant_id)
        return self
        
    def backup(self, backup_root_folder="/tmp/assistants_backup"):
        # check if the backup root folder exists
        if not path.exists(backup_root_folder):
            makedirs(backup_root_folder)

        # genreate name for the new backup folder ( with a random name )
        backup_folder = tempfile.mkdtemp(dir=backup_root_folder)
        
        # refresh the list of assistants
        self.refresh_assistants_list()

        # save all assistants to the backup folder.
        self.save_assistants_from_list(backup_folder)

        # save each individual assistant to the backup folder.
        for assistant in self.assistants_list:
            self.save_assistant(
                backup_folder,
                assistant.id,
                f"{assistant.name}_{assistant.id}.json"
            )
            # self.delete_assistant(assistant.id)
        # recresh assistants list again
        self.refresh_assistants_list()
        return self
