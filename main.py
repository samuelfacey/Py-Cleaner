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
def store(items:dict, path:str):

    # Creates folder for files, then moves them from old path to new one
    def move(elements:tuple, old_path:str, new_path:str):
        key = elements[0]
        files = elements[1]

        Path(f'{new_path}{os.sep}{key}').mkdir(parents=True, exist_ok=True)

        for f in files:
            shutil.move(f'{old_path}{os.sep}{f}',f'{new_path}{os.sep}{key}{os.sep}{f}')
    
    new_path = f'{Path(path)}{os.sep}New Folder with items'
    Path(new_path).mkdir(parents=True, exist_ok=True)

    for i in items.items():
        move(elements=i, old_path=path, new_path=new_path)

# Runs program
def run(path:str):

    elements = search(path, name=name)

    with open('messages.json') as m:
        message:dict = json.load(m)


    def input_controller(action:str, prompt:str):
        
        if action == 'quit':
            input(prompt)
            sys.exit('Qutting...')
        
        elif action == 'continue':
            input(prompt)

        elif action == 'store':
            print(prompt)
            store(items=sort(elements), path=path)
            return
        
        elif action == 'list':
            for e in elements:
                print(e)
            input_controller(action='selection', prompt=message['continue_selector'].replace('$NUM$', f'{len(elements)}'))
            
        elif action == 'selection':
            user_choice = input(prompt)

            if user_choice == '1':
                input_controller(action='store', prompt=message['storing'])

            elif user_choice == '2':
                input_controller(action='quit', prompt='Press Enter to exit program.')
            
            elif user_choice == '3':
                input_controller(action='list', prompt='')
            
            else:
                print('Invalid input')
                input_controller(action='selection', prompt=message['continue_selector'].replace('$NUM$', f'{len(elements)}'))


    if 'C:\Windows' in path or path == 'C:\\':
        input_controller(action='quit', prompt=message['danger'].replace('$PATH$', f'{path}'))

    elif 'C:\Program Files' in path or 'C:\Program Files (x86)' in path:
        input_controller(action='continue', prompt=message['warning'].replace('$PATH$', f'{path}'))

    input_controller(action='continue', prompt=message['welcome'].replace('$PATH$', f'{path}'))

    input_controller(action='selection', prompt=message['continue_selector'].replace('$NUM$', f'{len(elements)}'))


if __name__ == '__main__':
    try:
        path=str(Path.cwd()).replace(f'{name}', '')
        run(path)
    except Exception:
        traceback.print_exc()
    else:
        input('Clean up complete! Press Enter to quit program.')
        sys.exit('Quitting...') 
