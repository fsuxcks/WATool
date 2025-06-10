import os
import sys
import pyzipper
import customtkinter as ctk
import gdown
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from cryptography.fernet import Fernet
import json
from tkinter import messagebox
from threading import Thread

def getversion():
    try:
        with open("Bin/credentials.enc", "rb") as enc_file:
            encrypted = enc_file.read()
    except:
        messagebox.showerror("Ошибка", "Проверьте целостность папки Bin или скачайте заново.")
        sys.exit()

    key = "2bTU75QG_VOmNudJy0Pxe136argjyejOBwu3gYgSGEQ="
    fernet = Fernet(key)

    decrypted = fernet.decrypt(encrypted)
    creds_dict = json.loads(decrypted)

    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)

    sheet = client.open("Activation").sheet1
    return sheet.cell(2,7).value

def download_and_extract():
    url = f"https://drive.google.com/uc?export=download&id={sys.argv[2]}"
    print(url)
    archive_path = "update.zip"
    password = "watool"

    label_status.configure(text="Скачивание...")
    
    gdown.download(url, archive_path, quiet=True)
    
    label_status.configure(text="Распаковка архива...")
    try:
        with pyzipper.AESZipFile(archive_path) as zf:
            zf.setpassword(password.encode())
            zf.extractall(path=os.getcwd())
    except Exception as e:
        pass
    os.remove(archive_path)
    label_status.configure(text="Обновление завершено!")

def start_thread():
    download_button.place_forget()
    thread = Thread(target=download_and_extract, daemon=True)
    thread.start()


app = ctk.CTk()
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")
app.title("Обновление программы")
app.geometry("420x180")
app.resizable("false","false")
try:
    app.iconbitmap("Bin/ico.ico")
except:
    messagebox.showerror("Ошибка", "Проверьте целостность папки Bin или скачайте заново.")
    sys.exit()
if len(sys.argv) < 2:
    label_status = ctk.CTkLabel(app, text=f"Программа запущена вручную, параметры не заданы")
    label_status.place(relx=0.5, rely=0.3, anchor="center")
else:
    currentversion = sys.argv[1]
    version = getversion()
    if version != currentversion:

        download_button = ctk.CTkButton(app, text="Скачать и установить", command=start_thread)
        download_button.place(relx=0.5, rely=0.6, anchor="center")

        label_status = ctk.CTkLabel(app, text=f"Доступна новая версия V{version}")
        label_status.place(relx=0.5, rely=0.3, anchor="center")
    else:
        label_status = ctk.CTkLabel(app, text=f"У вас установлена самая последняя версия V{version}")
        label_status.place(relx=0.5, rely=0.3, anchor="center")

app.mainloop()
