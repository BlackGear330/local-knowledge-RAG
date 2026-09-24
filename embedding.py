from chunker import all_chunks
from openai import OpenAI


client = OpenAI(
    base_url='http://127.0.0.1:1234/v1',
    api_key='LM'
)

content = [chunk.page_content for chunk in all_chunks]

response = client.embeddings.create(
    model = 'text-embedding-qwen3-embedding-0.6b',
    input= content
)

