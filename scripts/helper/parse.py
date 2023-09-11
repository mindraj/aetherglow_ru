import re

def parse(ae_file : str) -> dict:
    r_dict = {}

    headers = re.findall(r".*: .*", ae_file)
    for s in headers[:6]:
        sp = s.split(":")
        r_dict[sp[0]] = sp[1]

    return r_dict