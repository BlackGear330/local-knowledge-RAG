from pathlib import Path
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter
import yaml
from langchain_core.documents import Document

m = Path('./Doc/Md')

all_chunks = []
for i in m.glob('*.md'):
    with open(i, 'r', encoding='utf-8') as f:
        content = f.read()
        if content.startswith('---'):
            parts = content.split('---', 2)
            metadata = parts[1]
            content = parts[2]
    result_dict_metadata = yaml.load(metadata, Loader=yaml.FullLoader)
    headers_split = [("#" * i, f"Header {i}") for i in range(1, 7)]
    content_without_table = []
    current_table = []
    in_table = False
    for line in content.splitlines():
        if line.strip() == "TABLE_OPEN":
            in_table = True
            current_table = []
        elif line.strip() == "TABLE_CLOSE":
            in_table = False
            table_text = '\n'.join(current_table)
            table_doc = Document(
                page_content=table_text,
                metadata=result_dict_metadata.copy()
            )
            all_chunks.append(table_doc)
            current_table = []
        elif in_table:
            current_table.append(line)
        else:
            content_without_table.append(line)
    content_without_table = "\n".join(content_without_table)

    splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_split)
    main_output = splitter.split_text(content_without_table)
    for i in main_output:
        i.metadata.update(result_dict_metadata)

# TODO: проверить оптимальные chunk_size и chunk_overlap на этапе embeddings + retrieval
    recursive_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
    )

    final_chunks = recursive_splitter.split_documents(main_output)
    all_chunks.extend(final_chunks)


if __name__ == "__main__":
    for idx, chunk in enumerate(all_chunks, 1) :
        print(f"------- Number Chunk {idx} -------")
        print("TEXT:")
        print(chunk.page_content)
        print(f"------- Metadata Chunk {idx} -------")
        print("TEXT:")
        print(chunk.metadata)
        print("-" * 40)

