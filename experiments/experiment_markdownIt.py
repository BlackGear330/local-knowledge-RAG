# Эксперимент 3 — визуальный вывод токенов
# Статус: ЗАВЕРШЁН
# Результат: наглядно исследована вложенность токенов Markdown через level

from markdown_it import MarkdownIt
from pathlib import Path

md = MarkdownIt('commonmark')

m = Path('../Doc/Md')
file_path = m / 'FAQ Namecheck.md'


content = open(file_path, 'r', encoding='utf-8').read()

tokens = md.parse(content)



def print_tokens(tokens):
    for token in tokens:
        if token.level == 0:
            print(token.type, token.content)
        elif token.level == 1:
            print('\t' + token.type, token.content)
        elif token.level == 2:
            print(('\t' * 2) + token.type, token.content)
        elif token.level == 3:
            print(('\t' * 3 )+ token.type, token.content)
        else:
            print("тут другая вложенность ", token.type, token.content, token.level)

print_tokens(tokens)