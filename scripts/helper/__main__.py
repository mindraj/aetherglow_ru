from pathlib import Path
import json
import re

def parse(ae_file : str) -> dict:
    r_dict = {}

    headers = re.findall(r".*: .*", ae_file)
    for s in headers[:6]:
        sp = s.split(":")
        r_dict[sp[0]] = sp[1]

    return r_dict

def validate(post : Path):

    errors = {}

    with open(f"./en/Chapter {chapter_num}/{post.name[:len('_ru.md')]}.md", "r", encoding="utf8") as f:

        input_headers = parse(post.read_text(encoding="utf8"))
        en_headers = parse(f.read())

        errors = {
            "fields_absent" : [],
            "fields_wrong" : []
        }
        for h in en_headers.keys():
            try:
                input_headers[h]
            except KeyError:
                errors["fields_absent"].append(h)

        if (input_headers.get('date') != en_headers['date']):
            errors["fields_wrong"].append('date')


        return errors



if __name__ == "__main__":
    # Load RU config
    ru_conf = {}
    with open("scripts\helper\config.json", "r", encoding="utf8") as f:
        ru_conf = json.load(f)

    chapter_num = int(input("Chapter: "))
    en_posts = Path(f"./en/Chapter {chapter_num}").glob("*.md")
    ru_posts = Path(f"./ru/{chapter_num}").glob("*.md")

    p_errors = {}
    for p in ru_posts:
        p_errors[p.name] = validate(p)
    
    print(p_errors)


