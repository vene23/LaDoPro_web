import os

print("📁 Archivos visibles en el entorno de Render:")
for root, dirs, files in os.walk(".", topdown=True):
    level = root.replace(os.getcwd(), "").count(os.sep)
    indent = " " * 2 * level
    print(f"{indent}{os.path.basename(root)}/")
    subindent = " " * 2 * (level + 1)
    for f in files:
        print(f"{subindent}{f}")
