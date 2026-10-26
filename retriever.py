import openai
from openai import OpenAI
from qdrant_client import QdrantClient
from promt import system_prompt
import sys


prep = input("Введите ваш вопрос: ").strip()

client = OpenAI(
    base_url='http://127.0.0.1:1234/v1',
    api_key='LM'
)

try:
    response = client.embeddings.create(
        model = 'text-embedding-qwen3-embedding-0.6b',
        input= prep
    )
except openai.OpenAIError:
    print("LM Studio недоступен")
    sys.exit(1)


vector = response.data[0].embedding

client_base = QdrantClient(path = './qdrant_local_db')

search_collection =  client_base.query_points(
    collection_name = 'new_collection',
    query = vector,
    limit = 3,
).points

context_chunk  = []
for hit in search_collection:
    if hit.payload and 'text' in hit.payload:
        context_chunk.append(hit.payload['text'] + "\n"+ str(hit.payload['metadata']))


context = "\n---\n".join(context_chunk)

formatted_prompt = system_prompt.format(context=context)

metadata_chunk = []
for hit in search_collection:
    if hit.payload and 'metadata' in hit.payload:
        metadata_chunk.append(hit.payload['metadata'])


try:
    reply = client.chat.completions.create(
        model = "google/gemma-4-12b-qat",
        messages = [
            {"role": "system", "content": formatted_prompt },
            {"role": "user", "content": prep }
        ],
        max_tokens=2048,
        extra_body={"chat_template_kwargs": {"enable_thinking": False}},
    )
except openai.OpenAIError:
    print("Модель недоступна")
    sys.exit(1)

print("\nОтвет модели:")
print(reply.choices[0].message.content)
print("\n========== RETRIEVAL ==========")
doc_idx = []
sources = []
tags = []
depts = []

for chunk in metadata_chunk:
    if chunk['document_id'] not in doc_idx:
        doc_idx.append(chunk['document_id'])

    if chunk['source'] not in sources:
        sources.append(chunk['source'])

    if chunk['dept'] not in depts:
        depts.append(chunk['dept'])

    for tag in chunk['tags']:
        if tag not in tags:
            tags.append(tag)

print(f"Id: {', '.join(doc_idx)}")
print(f"Source: {', '.join(sources)}")
print(f"Tags: {tags}")
print(f"Dept: {', '.join(depts)}")
for hit in search_collection:
    print(hit.score)

client_base.close()
client.close()