import os
from openai import AzureOpenAI

endpoint = "https://admin-m9ku0l1z-eastus2.cognitiveservices.azure.com/"
model_name = "o4-mini"
deployment = "o4-mini"

subscription_key = "7Ra9O1T4QLlMY6KGlwBgb9vHD9579h1AwpSRgNiAvqB4Drru9ZNwJQQJ99BDACHYHv6XJ3w3AAAAACOGAewE"
api_version = "2024-12-01-preview"

client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=subscription_key,
)

response = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant.",
        },
        {
            "role": "user",
            "content": "天空为什么是蓝色的?",
        }
    ],
    max_completion_tokens=100000,
    model=deployment
)

print(response.choices[0].message.content)