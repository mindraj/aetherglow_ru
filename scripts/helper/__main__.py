from pathlib import Path
import os
import json
import re

def parse(ae_str : str) -> dict:
    r_dict = {} # return object

    # Regular expressions to parse the header
    re_h = re.compile(r".*?\n\n", re.DOTALL) # to get the header
    re_k = re.compile(r".*?(?=[(:)])") # to get key
    re_v = re.compile(r"(?<=[(:)]).*") # to get value

    header_match = re_h.match(ae_str)
    if header_match is None: 
        return r_dict

    header = header_match.group()   

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

def validate_post(post : Path, config : dict) -> dict:

    errors = {}

    with open(f"./en/Chapter {chapter_num}/{post.name[:len('_ru.md')]}.md", "r", encoding="utf8") as f:

        input_headers = parse(post.read_text(encoding="utf8"))
        en_headers = parse(f.read())

        errors = {
            "fields_absent" : [],
            "fields_wrong" : []
        }
        
        for h in en_headers.keys():
            if not input_headers.get(h):
                errors["fields_absent"].append(h)

        if input_headers.get('date'):
            if (input_headers.get('date') != en_headers['date']):
                errors["fields_wrong"].append('date')

        if input_headers.get("title"):

            r_ch = re.compile(r"(?<=[#]).*") 

            in_ch_n = int(r_ch.search(input_headers['title']).group())
            en_ch_n = int(r_ch.search(en_headers['title']).group())

            if (en_ch_n != in_ch_n):
                errors["fields_wrong"].append('title')
        
        # r_t = re.compile(r".*(?=[#])")

        return errors
    
def display_p_errors(posts : dict) -> None:
    for p in posts:
        p_errors = {}
        p_errors[p.name] = validate_post(p, conf)

        errors_n = 0
        for v in p_errors[p.name].values():
            errors_n += len(v)

        if (errors_n == 0):
            print(f"{p.name} is OK")
        else:
            print(p_errors)

def generate_posts(ch_num, conf):
    en_posts = Path(f"./en/Chapter {chapter_num}").glob("*.md")
    #new_path = f"./{conf.keys()[0]}"
    for p in en_posts:

        new_file_name = p.name[:len(".md")] + "_ru.md"
        with open(f"./{conf['lang']}/{ch_num}/{new_file_name}", "w") as output_f:

            errors = validate_post(output_f, conf)
            for e in errors[new_file_name]["fields_absent"]:
                pass
            
if __name__ == "__main__":
    # Load RU config
    conf = {}
    directory=os.path.dirname(__file__)
    with open(directory+"/config.json", "r", encoding="utf8") as f:
        conf = json.load(f)

    chapter_num = int(input("Chapter: "))
    ru_posts = Path(f"./{conf['lang']}/{chapter_num}").glob("*.md")

    action = input("Command: ")

    match action.lower():
        case "val":
            display_p_errors(ru_posts)
        case "gen":
            generate_posts(chapter_num)

