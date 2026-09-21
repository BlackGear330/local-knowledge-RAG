# ЭКСПЕРИМЕНТ - Разбиение с учетом структуры
# Статус: ПРИОСТАНОВЛЕН
# Причина: сложность превысила рамки текущей версии.
# Результат: получено полезное понимание структуры Markdown



from markdown_it import MarkdownIt
from pathlib import Path

md = MarkdownIt('commonmark')

m = Path('../Doc/Md')


def build_blocks(tokens):
    blocks = []
    bullet_list = []
    ordered_list = []
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
        if token.type == 'bullet_list_open' and current_block is None:
            current_block = 'bullet'
        if token.type == 'inline' and current_block == 'bullet':
            bullet_list.append(token.content)
        if token.type == 'bullet_list_close' and current_block == 'bullet':
            current_block = None
            item_dict = {"type": 'bullet_list', "content": '\n'.join(bullet_list)}
            blocks.append(item_dict)
        if token.type ==  'ordered_list_open' and current_block is None:
            current_block = 'ordered_list'
        if token.type == 'inline' and current_block == 'ordered_list':
            ordered_list.append(token.content)
        if token.type == 'ordered_list_close' and current_block == 'ordered_list':
            current_block = None
            item_dict = {"type": 'ordered_list', "content": '\n'.join(ordered_list)}
            blocks.append(item_dict)
    return blocks

for i in m.glob("*.md"):
    with open(i, 'r', encoding='utf-8') as f:
        content = f.read()
        if content.startswith('---'):
            parts = content.split('---',2)
            metadata = parts[1]
            content = parts[2]


    tokens = md.parse(content)
    result = build_blocks(tokens)
    print(result)