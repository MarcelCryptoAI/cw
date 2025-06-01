import os
import ast

# (1) Standaard Python-modules, deze worden gefilterd
STANDARD_LIBS = {
    # Uitgebreide, actuele lijst (hier een subset, uitbreidbaar)
    'abc','argparse','array','asyncio','base64','binascii','bisect','calendar','collections','concurrent','contextlib',
    'copy','csv','ctypes','datetime','decimal','difflib','dis','enum','errno','faulthandler','filecmp','fileinput',
    'fnmatch','fractions','functools','gc','getopt','getpass','gettext','glob','gzip','hashlib','heapq','hmac','html',
    'http','imaplib','imp','importlib','inspect','io','itertools','json','logging','lzma','math','mimetypes','msilib',
    'multiprocessing','numbers','operator','os','pathlib','pickle','platform','plistlib','pprint','profile','pstats',
    'queue','random','re','sched','secrets','select','selectors','shlex','shutil','signal','site','socket','sqlite3',
    'ssl','stat','string','struct','subprocess','sys','tempfile','textwrap','threading','time','timeit','tkinter','trace',
    'traceback','tracemalloc','types','typing','unicodedata','unittest','urllib','uuid','venv','warnings','wave','weakref','webbrowser','xml','zipfile','zipimport','zoneinfo'
}

def find_imports_in_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        node = ast.parse(f.read(), filename)
    imports = set()
    for item in ast.walk(node):
        if isinstance(item, ast.Import):
            for alias in item.names:
                imports.add(alias.name.split('.')[0])
        elif isinstance(item, ast.ImportFrom):
            if item.module:
                imports.add(item.module.split('.')[0])
    return imports

def is_stdlib(module):
    return module in STANDARD_LIBS

def find_python_files(path):
    pyfiles = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.py'):
                pyfiles.append(os.path.join(root, file))
    return pyfiles

if __name__ == "__main__":
    project_dir = os.path.dirname(os.path.abspath(__file__))
    py_files = find_python_files(project_dir)
    all_imports = set()

    for pyfile in py_files:
        all_imports |= find_imports_in_file(pyfile)

    # Filter standaard modules eruit
    third_party = sorted([imp for imp in all_imports if not is_stdlib(imp)])

    # Voor sommige modules is de pip-naam anders (handmatige mapping toevoegen indien nodig)
    pip_map = {
        "cv2": "opencv-python",
        "sklearn": "scikit-learn",
        "PIL": "Pillow",
        "yaml": "pyyaml",
        "Crypto": "pycryptodome",
        "keras_tuner": "keras-tuner",
        "imblearn": "imbalanced-learn"
    }

    with open("requirements.txt", "w") as reqf:
        for module in third_party:
            pip_name = pip_map.get(module, module)
            reqf.write(f"{pip_name}\n")
    print(f"[✔] requirements.txt aangemaakt met {len(third_party)} pakketten.")

    if third_party:
        print("Geïdentificeerde pakketten:")
        print("\n".join(third_party))
    else:
        print("Geen externe dependencies gevonden!")
