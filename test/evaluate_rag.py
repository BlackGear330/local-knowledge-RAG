from evaluation_set import evaluation_set
from openai import OpenAI, APIConnectionError
from qdrant_client import QdrantClient
import sys


client = OpenAI(
    base_url='http://127.0.0.1:1234/v1',
    api_key='LM'
)

client_base = QdrantClient(path = './qdrant_local_db')

ok = 0
for question in evaluation_set:
    try:
        response = client.embeddings.create(
            model = 'text-embedding-qwen3-embedding-0.6b',
            input = question['question'],
        )
    except APIConnectionError:
        print("LM Studio недоступен")
        sys.exit(1)

    vector = response.data[0].embedding

    search_collection =  client_base.query_points(
        collection_name = 'new_collection',
        query = vector,
        limit = 3,
    ).points

    doc_id = []
    for hit in search_collection:
        if hit.payload and 'metadata' in hit.payload:
            if hit.payload['metadata']  and 'document_id' in hit.payload['metadata']:
                doc_id.append(hit.payload['metadata']['document_id'])



    if all(doc in doc_id for doc in question['expected_docs']):
        ok += 1
        print("OK")
    else:
        print(f"ERROR: not found: {question['expected_docs']}")

print(f"recall@3 = {ok}/{len(evaluation_set)}")

client_base.close()
client.close()