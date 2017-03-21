# Input and Output folders
import os

PROJECT_DIR = os.path.dirname(__file__)
print("PROJECT DIR: " + PROJECT_DIR)
GOOGLE_BOOKS_FOLDER = PROJECT_DIR+"/../data/input/gap-html"
EXTRACTION_FOLDER = PROJECT_DIR+"/../data/extracted/json-text-only-plus-extras"
EXTRACTION_COMPILED_FILE = PROJECT_DIR+"/../data/extracted/collection.json"
