from markitdown import MarkItDown
from pathlib import Path

md = MarkItDown()


d = Path('Doc')
m = Path('Doc/Md')


for i in d.iterdir():
    if i.suffix == '.docx':
        name = i.stem
        namemd = name + '.md'
        output = m/namemd
        result = md.convert(i)
        with open(output, "w", encoding="utf-8") as f:
            f.write(result.text_content)