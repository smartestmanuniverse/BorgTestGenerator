import unittest
from unittest.mock import patch, MagicMock
from assistant import Assistant

class TestAssistant(unittest.TestCase):

    @patch('assistant.OpenAI')
    @patch('assistant.getenv')
    def setUp(self, mock_getenv, MockOpenAI):
        mock_getenv.return_value = "fake_api_key"
        self.mock_client = MockOpenAI()
        self.assistant = Assistant(assistant_id=None)
        self.assistant.client = self.mock_client
        
    def test_create_assistant(self):
        self.mock_client.beta.assistants.create.return_value = MagicMock(id="1234", name="TestAssistant")
        self.assistant.create_assistant(name="TestAssistant", instructions="Test instructions")

        self.assertEqual(self.assistant.get_assistant_id(), "1234")
        self.assertEqual(self.assistant.get_assistant_name(), "TestAssistant")

    def test_load_assistant(self):
        mock_assistant = MagicMock(id="1234")
        self.mock_client.beta.assistants.retrieve.return_value = mock_assistant

        self.assistant.load_assistant(assistant_id="1234")
        self.assertEqual(self.assistant.assistant_id, "1234")

    def test_save_assistant(self):
        with patch("builtins.open", unittest.mock.mock_open()) as mock_file:
            mock_assistant = MagicMock(id="1234", to_dict=lambda: {"tools": []})
            self.mock_client.beta.assistants.retrieve.return_value = mock_assistant

            self.assistant.save_assistant(backup_folder="/tmp", assistant_id="1234", file_name="test.json")
            mock_file.assert_called_once_with("/tmp/test.json", 'w')

    # Ajoutez d'autres méthodes de test pour chaque fonction de la classe Assistant

    def test_list_assistants(self):
        mock_assistants = [MagicMock(id="1234"), MagicMock(id="5678")]
        self.mock_client.beta.assistants.list.return_value = MagicMock(data=mock_assistants)

        assistants = self.assistant.list_assistants()
        self.assertEqual(len(assistants), 2)
        self.assertEqual(assistants[0].id, "1234")
        self.assertEqual(assistants[1].id, "5678")

    def test_delete_assistant(self):
        self.assistant.delete_assistant(assistant_id="1234")
        self.mock_client.beta.assistants.delete.assert_called_once_with("1234")

    # Ajoutez des tests pour les autres méthodes ...

if __name__ == '__main__':
    unittest.main()