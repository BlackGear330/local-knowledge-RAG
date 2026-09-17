from markdown_it import MarkdownIt
from pathlib import Path
import json

md = MarkdownIt('commonmark')

m = Path('../Doc/Md')
file_path = m / 'Правила работы с вендорами клиента.md'


content = open(file_path, 'r', encoding='utf-8').read()

tokens = md.parse(content)

def main_save(result_list):
    with open ('parser_4.json', 'w', encoding='utf-8') as f:
        json.dump(result_list, f, ensure_ascii=False, indent=4)

def format_save(tokens):
    result_list = []
    for token in tokens:
        item_dict = {
            "type": token.type,
            "content": token.content,
            "level": token.level,
        }
        result_list.append(item_dict)
    return result_list


if __name__ == '__main__':
    my_parsed_list = format_save(tokens)
    main_save(my_parsed_list)


