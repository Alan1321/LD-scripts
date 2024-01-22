import re

def extract_variable_name(filename):
    pattern = "[a-zA-Z]_flash[a-zA-Z_]+"
    match = re.findall(pattern, filename)
    return match[0][2:]