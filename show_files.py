import os

print("📁 Contenido de inventario/static:")
for root, dirs, files in os.walk("inventario/static"):
    for f in files:
        print(os.path.join(root, f))

print("\n📁 Contenido de sitio_publico/static:")
for root, dirs, files in os.walk("sitio_publico/static"):
    for f in files:
        print(os.path.join(root, f))

