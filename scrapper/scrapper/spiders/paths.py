import os

def absolute_paths():
    # Obtain absolute paths to work in any location
    current_dir = os.getcwd()
    export_dir = os.path.join(current_dir, "scrapper", "spiders", "exports")
    os.makedirs(export_dir, exist_ok=True)

    return export_dir
