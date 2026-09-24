# Эксперимент 5 — Embeddings
# Статус: ЗАВЕРШЁН
# Результат: подключил локальную embedding-модель Qwen3-Embedding-0.6B через LM Studio, получил векторы для всех чанков. Проверил размерность эмбеддингов и сопоставление векторов с исходными чанками.


from chunker import all_chunks
from openai import OpenAI

client = OpenAI (
    base_url="http://127.0.0.1:1234/v1",
    api_key="lm-studio"
)
text = [chunk.page_content for chunk in all_chunks]

response = client.embeddings.create(
    model="text-embedding-qwen3-embedding-0.6b",
    input = text
)

for idx, item in enumerate(response.data):
    vector = item.embedding
    chunk_idx = item.index
    all_chunks[chunk_idx].metadata["embedding"] = vector

with_embeddings = sum(1 for c in all_chunks if "embedding" in c.metadata)

embedding_size = len(all_chunks[0].metadata["embedding"])

print(f"Всего чанков в списке: {len(all_chunks)}")
print(f"Из них с эмбеддингами: {with_embeddings}")
print(f"Количество чисел в 1 эмбеддинге: {embedding_size}")