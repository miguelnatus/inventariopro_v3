# # utils.py

# import requests

# def call_z_ai_api(user_message, api_key):
#     url = "https://api.z.ai/api/paas/v4/chat/completions"
#     headers = {
#         "Content-Type": "application/json",
#         "Accept-Language": "en-US,en",
#         "Authorization": f"Bearer {api_key}"
#     }
#     data = {
#         "model": "glm-4.5",
#         "messages": [
#             {
#                 "role": "system",
#                 "content": "You are a helpful AI assistant."
#             },
#             {
#                 "role": "user",
#                 "content": user_message
#             }
#         ]
#     }

#     response = requests.post(url, headers=headers, json=data)

#     if response.status_code == 200:
#         return response.json()
#     else:
#         return {"error": f"Request failed with status code {response.status_code}", "details": response.text}