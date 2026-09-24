# Эксперимент 6 — Semantic Search
# Статус: ЗАВЕРШЁН
# Результат: на практике проверил семантический поиск по чанкам через эмбеддинги и косинусное сходство. Получил осмысленный Top-K



from chunker import all_chunks
from openai import OpenAI
import numpy as np

client = OpenAI (
    base_url="http://127.0.0.1:1234/v1",
    api_key="lm-studio"
)

response = client.embeddings.create(
    model="text-embedding-qwen3-embedding-0.6b",
    input = "Какая процедура выхода сотрудника с проекта?"
)


query_vector = response.data[0].embedding

def cosine_similarity(v1, v2):
    vec1 = np.array(v1)
    vec2 = np.array(v2)
    result = vec1 @ vec2
    vector_norm = np.linalg.norm(vec1) * np.linalg.norm(vec2)
    total = result  / vector_norm
    return total

text = [chunk.page_content for chunk in all_chunks]

response_text = client.embeddings.create(
    model="text-embedding-qwen3-embedding-0.6b",
    input = text
)

for item in response_text.data:
    vector = item.embedding
    chunk_idx = item.index
    all_chunks[chunk_idx].metadata["embedding"] = vector


result = []
for chunk in all_chunks:
    chunk_vector = chunk.metadata["embedding"]
    score = cosine_similarity(query_vector, chunk_vector)
    result.append((score, chunk))

sorted_results = sorted(result, key=lambda x: x[0], reverse=True)

sorted_num = sorted_results[:3]

for chunk in sorted_num:
    print(f"Score: {chunk[0]:.4f}")
    print(chunk[1].page_content)
    print("-" * 50)