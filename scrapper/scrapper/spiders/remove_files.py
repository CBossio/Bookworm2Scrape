import os
import shutil

#Remove old csv and excels
def remove_old():
    try:
        current_dir = os.getcwd()
        export_dir = os.path.join(current_dir, "scrapper", "spiders", "exports")
        for f in os.listdir(export_dir):
            if f.endswith(".csv") or f.endswith(".xlsx"):
                os.remove(os.path.join(export_dir, f))
    except Exception as e:
        print("Folder does not exist")
