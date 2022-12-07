import os
import shutil
import json
import sys
import traceback
from pathlib import Path

name = str(os.path.basename(Path.cwd()))

# Searches directory for files
def search(path:str, name:str) -> list:

    # Creates list of files in path directory
    container = []
    for f in os.listdir(path):
        container.append(str(f))
    container.remove(name)
    
    # Returns list of files
    return container

# Sorts files by type and appends them to dictionary
def sort(container:list) -> dict:
    sorted_items = {}

    # Loop to iterate through list of detected files
    for i in container:
        # string for extension of current file
        ext = Path(i).suffix

        # If file has no suffix, it is added to a Folders Key value list pair
        if ext == '':
            try:
                sorted_items['Folders'].append(i)
            except:
                sorted_items['Folders'] = [i]
            continue
        else:
            pass
        
        # Checks if file extension is in dictionary of known extensions
        def is_known_file():
            with open('extensions.json') as e:
                extensions:dict = json.load(e)
            # Loop to iterate through the keys of the extension dict. Expects Tuples of (String:List)
            for ext_type in extensions.items():
                # if file extension is in iterated tuple, it is added to the appropriate key value list pair
                if ext in ext_type[1]:
                    try:
                        sorted_items[ext_type[0]].append(i)
                    except:
                        sorted_items[ext_type[0]] = [i]
                    return True
            return False
                
        # If file extension is not in extensions dict, it is added to it's own unique key value list pair
        if is_known_file() == False:
            e = ext.replace(".", "")
            try:
                sorted_items[e].append(i)
            except:
                sorted_items[e] = [i]  

    # Returns dictionary of keys (File Categories), and values (File Names)
    print(sorted_items)
    return sorted_items

# Creates folders based on file type and moves files to new folders
def store(items:dict, path:str, user_input:str):

    # Creates folder for files, then moves them from old path to new one
    def move(elements:tuple, old_path:str, new_path:str):
        key = elements[0]
        files = elements[1]

        Path(f'{new_path}{os.sep}{key}').mkdir(parents=True, exist_ok=True)

        for f in files:
            shutil.move(f'{old_path}{os.sep}{f}',f'{new_path}{os.sep}{key}{os.sep}{f}')

    # If user wants to place new folders in a parent folder
    if user_input == '1':
        new_path = f'{Path(path)}{os.sep}New Folder with items'
        Path(new_path).mkdir(parents=True, exist_ok=True)

        for i in items.items():
            move(elements=i, old_path=path, new_path=new_path)
    
    # If user does not want a parent folder
    elif user_input == '2':
        new_path = path
    
        for i in items.items():
            move(elements=i, old_path=path, new_path=new_path)
    
    else:
        print('Invalid input, aborting...')
        run()

# Runs program
def run(path:str):

    if 'C:\Windows' in path or path == 'C:\\':
        input(f'HOLD UP! ⚠️ {path} is likely to have important system files ⚠️\nAlthough this could be a false alarm, the program will close after this message to avoid catastrophic system damage.\nPlease move the cleaner to a different folder and try again.')
        sys.exit('Quitting...')
    input(f'It\'s time to clean up! \nBe sure that this folder: {path} is in the directory you wish to sort. \nPress enter to continue!')

    if 'C:\Program Files' in path or 'C:\Program Files (x86)' in path:
        input(f'Just a heads up, the path: {path} could have some important data that should not be moved around. \nYou may continue, or exit the program and move the cleaner folder elsewhere.')

    elements = search(path, name=name)

    user_continue_input = input(f'There are {len(elements)} items to be sorted. Would you like to continue? \nYes: Press 1, No: Press 2, List of files: Press 3\n')

    if user_continue_input == '1':
        user_new_input = input('Would you like to place all of the sorted items in a new folder? Yes: Press 1, No: Press 2, Quit: Press 3\n')
        if user_new_input == '3':
            sys.exit('Quitting...')
        store(sort(elements), path, user_new_input)

    elif user_continue_input == '2':
        sys.exit('Quitting...')
    
    elif user_continue_input == '3':
        for e in elements:
            print(e)
        user_continue_input = input(f'There are {len(elements)} items to be sorted. Would you like to continue? \nYes: Press 1, No: Press 2\n')
    else:
        print('Invalid input')
        run(path=path)

if __name__ == '__main__':
    try:
        path=str(Path.cwd()).replace(f'{name}', '')
        run(path)
    except Exception:
        traceback.print_exc()
    else:
        input('Clean up complete! Press Enter to quit program.')
        sys.exit('Quitting...') 
