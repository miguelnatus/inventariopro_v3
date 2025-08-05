# camarim/tests/test_ai_clients.py

import pytest
from unittest.mock import patch

from camarim.ai_client import OpenAIClient, OpenRouterClient

class DummyMessage:
    def __init__(self, content):
        self.content = content

class DummyChoice:
    def __init__(self, message):
        self.message = message

class DummyResponse:
    def __init__(self, text):
        self.choices = [DummyChoice(DummyMessage(text))]

@patch('openai.ChatCompletion.create')
def test_openai_client_returns_response(mock_create):
    # prepara o retorno simulado
    mock_create.return_value = DummyResponse("Olá do OpenAI!")
    client = OpenAIClient()
    out = client.send_chat("teste")
    assert out == "Olá do OpenAI!"
    mock_create.assert_called_once()

@patch('openai.ChatCompletion.create')
def test_openrouter_client_returns_response(mock_create):
    mock_create.return_value = DummyResponse("Olá do OpenRouter!")
    client = OpenRouterClient()
    out = client.send_chat("teste")
    assert out == "Olá do OpenRouter!"
    mock_create.assert_called_once()
