from markdown_it import MarkdownIt
from pathlib import Path

md = MarkdownIt('commonmark')

m = Path('Doc/Md')


def build_blocks(tokens):
    blocks = []

    current_block = None
    for token in tokens:
        if token.type == 'heading_open' and current_block is None:
            current_block = 'heading'
        if token.type == 'inline' and current_block =='heading':
            item_dict = {"type": 'heading', "content": token.content}
            blocks.append(item_dict)
        if token.type == 'heading_close' and current_block =='heading':
            current_block = None
        if token.type == 'paragraph_open' and current_block is None:
            current_block = 'paragraph'
        if token.type == 'inline' and current_block == 'paragraph':
            item_dict = {"type": 'paragraph', "content": token.content}
            blocks.append(item_dict)
        if token.type == 'paragraph_close' and current_block == 'paragraph':
            current_block = None
    return blocks

for i in m.glob("*.md"):
    with open(i, 'r', encoding='utf-8') as f:
        content = f.read()

    tokens = md.parse(content)
    result = build_blocks(tokens)
    print(result)