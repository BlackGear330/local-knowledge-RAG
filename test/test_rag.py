from evaluation_set import evaluation_set
from openai import OpenAI
from qdrant_client import QdrantClient


client = OpenAI(
    base_url='http://127.0.0.1:1234/v1',
    api_key='LM'
)

client_base = QdrantClient(path = './qdrant_local_db')

for question in evaluation_set:
        response = client.embeddings.create(
            model = 'text-embedding-qwen3-embedding-0.6b',
            input = question['question'],
        )
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


        for doc in question['expected_docs']:
                if doc in doc_id:
                    print("OK")
                else:
                    print("ERROR")
                    #Для выявления причины почему else.
                    print("----doc----")
                    print(doc)
                    print("--------")
                    print("----doc_id----")
                    print(doc_id)
                    print("--------")
                    print("----question----")
                    print(question["expected_docs"])
