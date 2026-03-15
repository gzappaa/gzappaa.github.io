import os

OLD = "books_by_category.json"
NEW = "books_by_category.json"
ROOT = "."

for dirpath, dirnames, filenames in os.walk(ROOT):
    for fname in filenames:
        if fname.endswith(".py") or fname.endswith(".json") or fname.endswith(".ipynb"):
            path = os.path.join(dirpath, fname)
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
            if OLD in text:
                text = text.replace(OLD, NEW)
                with open(path, "w", encoding="utf-8") as f:
                    f.write(text)