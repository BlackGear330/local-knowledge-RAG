from chunker import all_chunks
from qdrant_client import QdrantClient
from embedding import response
from qdrant_client.models import Distance, VectorParams, PointStruct
import hashlib
from pathlib import Path


client = QdrantClient(path='./qdrant_local_db')
collection_name = "new_collection"

hash_file = Path('./qdrant_local_db/corpus_hash.txt')


corpus = "\n".join(
    chunk.page_content + str(chunk.metadata)
    for chunk in all_chunks
)

current_hash = hashlib.sha256(
    corpus.encode("utf-8")
).hexdigest()


old_hash = None

if hash_file.exists():
    with open(hash_file, 'r', encoding='utf-8') as f:
        old_hash = f.read().strip()


if old_hash == current_hash and client.collection_exists(collection_name):
    print("База актуальна. Изменений нет.")

else:
    print("База изменилась. Обновляем базу.")

    # Если старая collection существует — удаляем её
    if client.collection_exists(collection_name):
        client.delete_collection(collection_name)

    # Создаём новую collection
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
            size=1024,
            distance=Distance.COSINE,
        ),
    )

    points = []

    for item in response.data:
        chunk = all_chunks[item.index]

        point = PointStruct(
            id=item.index,
            vector=item.embedding,
            payload={
                "text": chunk.page_content,
                "metadata": chunk.metadata,
            }
        )

        points.append(point)

    operation_info = client.upsert(
        collection_name=collection_name,
        wait=True,
        points=points,
    )

    print("Данные успешно добавлены:", operation_info)
    print(client.count(collection_name=collection_name))

    with open(hash_file, 'w', encoding='utf-8') as f:
        f.write(current_hash)


client.close()