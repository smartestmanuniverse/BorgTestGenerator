# BorgTestGenerator

> OpenAI assistants automations to generate python3 unittest files

BorgTestGenerator is a Python library that generates unit test files from Python scripts using the OpenAI API.

## Installation

### Installation from pip ( with venv )

This section provides instructions for installing the librarie package from pip using a virtual environment (venv).

1. **Create a virtual environment:**
    ```sh
    python3 -m venv venv
    ```

2. **Activate the virtual environment:**
    - On Linux or macOS:
        ```sh
        source venv/bin/activate
        ```
    - On Windows:
        ```sh
        .\venv\Scripts\activate
        ```

3. **Update pip from pip:**
    ```sh
    python3 -m pip install --upgrade pip
    ```

4. **Install the package from pip:**
    ```sh
    python3 -m pip install -U BorgTestGenerator
    ```


## Usage of BorgTestGenerator python library

To use the `Assistant` class from the `BorgTestGenerator` module in your code, you need to follow these steps:

1. Import the `Assistant` class from the `BorgTestGenerator` module in your Python file. Make sure the `BorgTestGenerator` module is installed in your Python environment using the `pip install BorgTestGenerator` command.

    ```python
    from BorgTestGenerator.assistant import Assistant
    ```

2. Create an instance of the `Assistant` class using the constructor. You can provide additional arguments to the constructor based on your application's needs.

    ```python
    assistant = Assistant()
    ```

3. Set the user input that describes the task to be performed using the `set_user_input` method.
    ```python
    assistant.create_assistant(
        name="Test Assistant",
        instructions="This is a test assistant.",
        model="gpt-4o",
        tool_code_interpreter=True,
        tool_file_search=True
    )
    ```


### How To Use AssistantBackupManager

Pour utiliser la classe [`AssistantBackupManager`]("README.md") du module `BorgTestGenerator.assistant`, suivez les étapes ci-dessous :

1. **Importer la classe [`AssistantBackupManager`]("README.md")** :
    ```python
    from BorgTestGenerator.assistant import AssistantBackupManager
    ```

2. **Créer une instance de la classe `AssistantBackupManager`** :
    ```python
    assistant_backup_manager = AssistantBackupManager()
    ```

3. **Définir l'entrée utilisateur qui décrit la tâche à effectuer** :
    ```python
    assistant_backup_manager.backup()
    ```

Ces étapes permettent de configurer et d'utiliser le `AssistantBackupManager` pour gérer les sauvegardes de manière automatisée.


### How to use unittestwriter in your code

The following example shows how to use the `UnitTestWriter` class from the `BorgTestGenerator.agents.unittestwriter` module to generate unit test files for Python scripts.

```python
# Import the UnitTestWriter class from the BorgTestGenerator.agents.unittestwriter module
from BorgTestGenerator.agents.unittestwriter import UnitTestWriter

# Create an instance of the UnitTestWriter class with the code language specified as Python
testWriter = UnitTestWriter(code_language="python")

# Set the user input that describes the task to be performed
testWriter.set_user_input("Write the code for the test file corresponding to this Python script")

# Add the Python files for which unit tests should be generated
testWriter.add_upload(["/path/to/file1.py", "/path/to/file2.py"])

# Define the vector store name
testWriter.define_vector_store_name("test_vector_store")

# Generate the unit test files
testWriter.generate()
```

In this example:

1. **Import**: The `UnitTestWriter` class is imported from the `BorgTestGenerator.agents.unittestwriter` module.
2. **Instance**: An instance of `UnitTestWriter` is created with the `code_language` parameter set to `"python"`.
3. **User input**: The `set_user_input` method is used to set a task description in French.
4. **File addition**: The `add_upload` method adds the paths of the Python files for which tests should be generated.
5. **Vector store name**: The `define_vector_store_name` method defines the name of the vector store used.
6. **Generation**: The `generate` method triggers the generation of the unit test files.

This example demonstrates how to automate the generation of unit tests for Python scripts using the `UnitTestWriter` class.
