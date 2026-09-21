from pathlib import Path
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter
import yaml


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
    splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_split)

    main_output = splitter.split_text(content)

    for i in main_output:
        i.metadata.update(result_dict_metadata)

    recursive_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )

    final_chunks = recursive_splitter.split_documents(main_output)
    all_chunks.extend(final_chunks)




for idx, chunk in enumerate(all_chunks, 1) :
    print(f"------- Number Chunk {idx} -------")
    print("TEXT:")
    print(chunk.page_content)
    print(f"------- Metadata Chunk {idx} -------")
    print("TEXT:")
    print(chunk.metadata)
    print("-" * 40)