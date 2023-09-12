from pathlib import Path
import json
import re

def parse(ae_str : str) -> dict:
    r_dict = {}

    re_h = re.compile(r".*?\n\n", re.DOTALL)
    re_k = re.compile(r".*?(?=[(:)])")
    re_v = re.compile(r"(?<=[(:)]).*") 

    header = re_h.match(ae_str).group()

    for s in header.split('\n'):
        
        mk = re_k.search(s)
        if (mk is None):
            break

        k = mk.group()
        if (k == "poll"):
            break
        
        mv = re_v.search(s)
        v = mv.group().strip()

        r_dict[k] = v

    return r_dict

def validate(post : Path, config : dict) -> dict:

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

        r_ch = re.compile(r"(?<=[#]).*") 
        r_t = re.compile(r".*(?=[#])")

        in_ch_n = int(r_ch.search(input_headers['title']).group())
        en_ch_n = int(r_ch.search(en_headers['title']).group())

        # print(f"English chapter n: {en_ch_n}")
        # print(f"Input chapter n: {in_ch_n}")

        if (en_ch_n != in_ch_n):
            errors["fields_wrong"].append('title')


        return errors

def display_errors(errors : dict) -> None:
    print(errors)
    return

if __name__ == "__main__":
    # Load RU config
    conf = {}
    with open("scripts\helper\config.json", "r", encoding="utf8") as f:
        conf = json.load(f)

    chapter_num = int(input("Chapter: "))
    en_posts = Path(f"./en/Chapter {chapter_num}").glob("*.md")
    ru_posts = Path(f"./ru/{chapter_num}").glob("*.md")

    
    for p in ru_posts:
        p_errors = {}
        p_errors[p.name] = validate(p, conf)

        errors_n = 0
        for v in p_errors[p.name].values():
            errors_n += len(v)

        if (errors_n == 0):
            print(f"{p.name} is OK")
        else:
            display_errors(p_errors)