import subprocess
# 修改为指定镜像源：
subprocess.run(["pip", "install", "fastapi", "-i", " https://pypi.org/simple"])
with open(r"C:\Users\Administrator\git\h-trackpoint\trackpoint-backend\requirements.txt","r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#"):
            subprocess.run(["pip", "install", line])