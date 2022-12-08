import os
import sys
import traceback
from pathlib import Path
from modules import Functions

name_of_parent_folder = str(os.path.basename(Path.cwd()))
path=str(Path.cwd()).replace(f'{name_of_parent_folder}', '')

app = Functions(path=path, name=name_of_parent_folder)

if __name__ == '__main__':
    try:
        app.run(path)
    except Exception:
        traceback.print_exc()
    else:
        input('Clean up complete! Press Enter to quit program.')
        sys.exit('Quitting...') 
