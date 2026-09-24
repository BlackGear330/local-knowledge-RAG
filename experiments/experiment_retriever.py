# Эксперимент 4 — BM25
# Статус: ЗАВЕРШЁН
# Результат: на практике проверил работу BM25 на корпусе документов. Выявил проблему чанкинга: RecursiveCharacterTextSplitter может разрезать строки Markdown-таблиц между чанками.

from chunker import all_chunks
import string
import bm25s

## BM25 Score = Ценность слова (IDF) * (Частота слова / Корректировка на длину чанка)

prep = input("Введите ваш вопрос: ").lower().strip().translate(str.maketrans('', '', string.punctuation))


text_strings = [doc.page_content for doc in all_chunks]

text_tokens = bm25s.tokenize(text_strings)

retriever = bm25s.BM25()
retriever.index(text_tokens)


query_tokens = bm25s.tokenize([prep])

results, scores = retriever.retrieve(query_tokens, k=3)


for number, (doc_idx, score) in enumerate(zip(results[0], scores[0]), 1) :
    print(f"------- Number Chunk {doc_idx+1} -------")
    print(f"{text_strings[doc_idx]}")
    print(f"------- Score Chunk {doc_idx+1} -------")
    print(f'{score:.4f}')

