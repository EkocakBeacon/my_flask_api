import zipfile
import os

def create_zip(zip_name="flask_deploy.zip"):
    with zipfile.ZipFile(zip_name, "w") as zipf:
        for foldername, subfolders, filenames in os.walk("."):
            if "venv" in foldername or "__pycache__" in foldername:
                continue
            for filename in filenames:
                if filename.endswith(".py") or filename == "requirements.txt":
                    filepath = os.path.join(foldername, filename)
                    zipf.write(filepath, arcname=os.path.relpath(filepath, "."))

create_zip()
