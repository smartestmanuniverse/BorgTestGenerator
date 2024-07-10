#coding: utf-8
from agents.py3_unit_tests_writer import py3UnitTestFileWriter
import os


class unittestwriter(py3UnitTestFileWriter):
    def __init__(self, assistant_id=None):
        super().__init__(assistant_id)
        self.check_and_retreive()

    def check_and_retreive(self):
        if ( type(self.assistant) == None ) or ( self.assistant.assistant_id == None ):
            self.search_and_retreive_assistant()
        return self
    
    def run_generation( self, 
                        vector_store_name, 
                        files_to_upload
                      ):
        try:
            self.upload_files(vector_store_name, files_to_upload)
            self.create_new_thread()
            self.run()
        except Exception as e:
            print(e)
        return self
    
    def save_generation(self, output_filename, overwrite=False):
        if os.path.exists(output_filename):
            if overwrite:
                os.remove(output_filename)
            else:
                print(f"Le fichier {output_filename} existe déjà !")

                return self
            
        self.save_assistant_response_to_file(output_filename, remove_block_delimiters=True)

        return self
    
