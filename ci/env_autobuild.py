import ast

def extract_imports(file_path):
    with open(file_path, "r") as f:
        tree = ast.parse(f.read())

    imports = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for n in node.names:
                imports.add(n.name.split(".")[0])

        if isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module.split(".")[0])

    return imports


def build_env(files):
    all_imports = set()

    for f in files:
        try:
            all_imports |= extract_imports(f)
        except:
            pass

    core = {"os", "sys", "json", "time", "math", "ast"}

    libs = sorted(list(all_imports - core))

    with open("requirements.auto.txt", "w") as f:
        for lib in libs:
            f.write(lib + "\n")

    print("AUTO ENV GENERATED")