from json import loads
from sys import argv
import re

import os.path

try:
    from json_validator import is_valid_resume
    from resume import Resume
except ImportError:
    from .json_validator import is_valid_resume
    from .resume import Resume


def get_file(file, is_package_file=True):
    if is_package_file:
        file = os.path.join(os.path.dirname(__file__), file)

    try:
        with open(file, encoding="utf8") as f:
            data = f.read()
            return data
    except FileNotFoundError:
        print("File not found")
        return 1


def main():
    if len(argv) < 2:
        print("Requires a Json file as an argument")
        exit(1)
    page = None
    if "--page=1" in argv:
        page = 1
        argv.pop(argv.index("--page=1"))
    elif "--page=2" in argv:
        page = 2
        argv.pop(argv.index("--page=2"))
    regex = re.compile(r'--page=\d')
    bad = [i for i in argv if regex.search(i)]
    if len(bad) > 0:
        argv.pop(argv.index(bad[0]))
    if len(argv) == 3:
        print("Generating resume with " + argv[1] + " and style " + argv[2])
        json_string = get_file(argv[1], False)
        if not is_valid_resume(json_string):
            print("invalid JSON")
            exit(1)  # type: ignore
        print("Valid Json")  # delete this later
        resume = Resume(False)
        if argv[2] == "1":
            print("applying default theme 1")
            resume.apply_theme(loads(get_file(os.path.join("themes", "default.json"))))
        elif argv[2] == "2":
            resume.apply_theme(loads(get_file(os.path.join("themes", "default2.json"))))
        elif argv[2] == "3":
            resume.apply_theme(loads(get_file(os.path.join("themes", "default3.json"))))
        else:
            # todo: schema checks ones schema is complete (sprint 5?)
            resume.apply_theme(loads(get_file(argv[2], False)))
        
        resume.set_page(page)
        resume.generate_resume(loads(json_string))

    elif len(argv) == 2:
        print("Generating resume with " + argv[1])
        data = get_file(argv[1], False)
        theme = loads(get_file(os.path.join("themes", "default.json")))
        if is_valid_resume(data):   # type: ignore
            data = loads(data)   # type: ignore
            print("Valid Json")  # delete later
            resume = Resume(False)
            resume.apply_theme(theme)
            resume.set_page(page)
            resume.generate_resume(data)
        else:
            print("Invalid Json")
            exit(1)

    else:
        print("Too many args")


# if name == "main":
if __name__ == '__main__':
    main()
