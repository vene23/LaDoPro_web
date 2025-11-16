import subprocess

print("=== Running migrations on Railway ===")
subprocess.run(["python", "manage.py", "migrate", "--noinput"], check=True)
print("=== DONE ===")
