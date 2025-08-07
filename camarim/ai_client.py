# import os
# import openai
# from django.conf import settings
# from abc import ABC, abstractmethod

# SYSTEM_HELP = """
# Você é o assistente de ajuda do InventárioPro.
# Responda de forma clara e objetiva às dúvidas do usuário sobre funcionalidades, fluxos e telas do sistema.
# """

# class BaseAIClient(ABC):
#     @abstractmethod
#     def send_chat(self, prompt: str) -> str:
#         """Envia um prompt e retorna a resposta."""
#         pass

# class OpenAIClient(BaseAIClient):
#     def __init__(self):
#         openai.api_key = getattr(settings, 'OPENAI_API_KEY', os.getenv('OPENAI_API_KEY'))

#     def send_chat(self, prompt: str) -> str:
#         messages = [
#             {"role": "system", "content": SYSTEM_HELP},
#             {"role": "user",   "content": prompt},
#         ]
#         resp = openai.ChatCompletion.create(
#             model='gpt-3.5-turbo',
#             messages=messages,
#             temperature=0.5,
#             max_tokens=300,
#         )
#         return resp.choices[0].message.content.strip()

# class OpenRouterClient(BaseAIClient):
#     def __init__(self):
#         openai.api_key = getattr(settings, 'OPENROUTER_API_KEY', os.getenv('OPENROUTER_API_KEY'))
#         openai.api_base = "https://openrouter.ai/api/v1"

#     def send_chat(self, prompt: str) -> str:
#         messages = [
#             {"role": "system", "content": SYSTEM_HELP},
#             {"role": "user",   "content": prompt},
#         ]
#         resp = openai.ChatCompletion.create(
#             model='deepseek-r1:free',
#             messages=messages,
#             temperature=0.7,
#             max_tokens=300,
#         )
#         return resp.choices[0].message.content.strip()


# def get_ai_client() -> BaseAIClient:
#     """
#     Retorna uma instância de cliente de IA de acordo com a configuração.
#     Use settings.AI_PROVIDER ('openai' ou 'openrouter') ou a variável de ambiente AI_PROVIDER.
#     """
#     provider = getattr(settings, 'AI_PROVIDER', os.getenv('AI_PROVIDER', 'openai')).lower()
#     if provider == 'openrouter':
#         return OpenRouterClient()
#     return OpenAIClient()
