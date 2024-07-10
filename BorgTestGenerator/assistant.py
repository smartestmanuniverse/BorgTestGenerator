#!/usr/bin/env python3
#coding: utf-8

from openai import OpenAI
from os import getenv
import json

class Assistant(object):
    def __init__(self, assistant_id):
        self.client = OpenAI(api_key=getenv("OPENAI_API_KEY"))
        self.assistant_id = assistant_id

    def load_assistant(self, assistant_id=None):
        if assistant_id:
            self.assistant_id = assistant_id
        self.assistant = self.client.beta.assistants.retrieve(f"{self.assistant_id}")
        return self
    
    def create_assistant(self, name, instructions, model="gpt-4o", tool_code_interpreter=False):
        tools_ = []
        if tool_code_interpreter:
            tools_.append({"type": "code_interpreter"})

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
            assistants = response['data']

            if not assistants:
                break

            all_assistants.extend(assistants)

            # Met à jour l'argument 'after' pour récupérer la page suivante
            args['after'] = assistants[-1]['id']

        return all_assistants
    
    def save_assistants_list(self, file_name):
        with open(file_name, 'w') as file:
            json.dump(self.list_assistants(), file)
        return self
    
    def print_assistants_list(self):
        all_assistants = self.list_assistants()
        for assistant in all_assistants:
            print(f"ID: {assistant['id']}, Nom: {assistant['name']}")
        return self
    
    def exact_search_assistant(self, name, model, instructions):
        assistants = self.list_assistants()
        for assistant in assistants:
            if assistant['name'] == name and assistant['model'] == model and assistant['instructions'] == instructions:
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
 
        #print(self.file_batch.status)
        #print(self.file_batch.file_counts)
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