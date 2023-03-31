import os

with open("scripts/version", "r") as f:
    version = int(f.read().strip())

next_version = version + 1

os.system(f"docker build . -t h2magic/super_continent_user:v{next_version}")
os.system(f"docker push h2magic/super_continent_user:v{next_version}")

with open("scripts/version", "w") as f:
    f.writelines(str(version + 1))
