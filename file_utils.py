        


from genericpath import isfile
from os import listdir
from os.path import isfile, join

from constants import RECEIPTS_FOLDER


def get_filepaths_list(folder_name):
    files = get_filepaths(folder_name)
    if not files:
        print(f'No documents found in folder "{RECEIPTS_FOLDER}"')
        return None

    return files

def get_filepaths(folder_path):
    folder_path = 'receipts'
    files = [join(folder_path, file) for file in listdir(folder_path) if
                isfile(join(folder_path, file)) and file.endswith(".pdf")]
    return files
