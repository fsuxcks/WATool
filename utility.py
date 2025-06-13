import os
import sys
import time
import json
import shutil
import subprocess
from datetime import datetime, timedelta, timezone

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from cryptography.fernet import Fernet

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from tkinter import messagebox

drivers = []

def CreateNewUser(name, tg):
    serial = GetSerial()
    try:
        with open("Bin/credentials.enc", "rb") as enc_file:
            encrypted = enc_file.read()
    except:
        return 1,0,False, 0, 0,0,0

    key = "2bTU75QG_VOmNudJy0Pxe136argjyejOBwu3gYgSGEQ="
    fernet = Fernet(key)

    decrypted = fernet.decrypt(encrypted)
    creds_dict = json.loads(decrypted)
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        sheet = client.open("Activation").sheet1
    except:
        return False

    trialusers = sheet.col_values(5)

    names = sheet.col_values(2)
    if name in names:
        return 2

    if serial in trialusers:
        all_serials = sheet.col_values(1)
        user = len(all_serials) + 1
        sheet.update_cell(user, 1, serial)
        sheet.update_cell(user, 2, name)
        sheet.update_cell(user, 6, tg)
        sheet.update_cell(user, 3, "Trial")
        messagebox.showinfo("Регистрация", "Срок вашего пробного периода закончился. Вам доступна только Trial версия. Пожалуйста перезапустите программу.")
        return 3
    else:
        newuser = len(trialusers) + 1
        newusersid = sheet.col_values(6)
        newuserid = len(newusersid) + 1
        ID = newuserid-1
        sheet.update_cell(newuser,5,serial)

    all_serials = sheet.col_values(1)
    user = len(all_serials) + 1
    sheet.update_cell(user, 1, serial)
    sheet.update_cell(user, 2, name)
    sheet.update_cell(user, 6, tg)
    sheet.update_cell(user, 3, "Pro")
    return True


def GetSerial():
    try:
        output = subprocess.check_output("wmic diskdrive get SerialNumber", shell=True)
        serial = output.decode().split("\n")[1].strip()

        return serial
    except Exception as e:
        return None

def CheckSerial(serial, currentversion):    
    try:
        with open("Bin/credentials.enc", "rb") as enc_file:
            encrypted = enc_file.read()
    except:
        return 1,False, 0, 0,0,0

    key = "2bTU75QG_VOmNudJy0Pxe136argjyejOBwu3gYgSGEQ="
    fernet = Fernet(key)

    decrypted = fernet.decrypt(encrypted)
    creds_dict = json.loads(decrypted)
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        sheet = client.open("Activation").sheet1
    except:
        return 3,0,0,0,0,0

    all_serials = sheet.col_values(1)
    serialcell = sheet.find(serial, in_column=1)

    if not serial in all_serials:
        return 0, False, 0, 0,0,0

    name = sheet.cell(serialcell.row, serialcell.col+1).value
    status = sheet.cell(serialcell.row, serialcell.col+2).value
    version = sheet.cell(2,7).value

    logs = sheet.col_values(8)
    newlog = len(logs) + 1
    localtime = datetime.now().astimezone()
    convertedtime = localtime.astimezone(timezone(timedelta(hours=4)))
    sheet.update_cell(newlog,8,f"{name} : {convertedtime.hour}:{convertedtime.minute}")
    if version != currentversion:
        changelog = sheet.cell(2,9).value
        return 2, False, name, version,status, changelog

    return 0, serial in all_serials, name, version, status, 0

def CheckSub(serial, currentversion):
    if serial is None:
        return 3,0,0,0 ,0,# Не удалось получить серийный номер
    error, sub, name, version, status, changelog = CheckSerial(serial, currentversion)
    if error == 1:
        return 4,0,0,0,0 # Не удалось найти нужные файлы
    if error == 2:
        return 5,version,name,status,changelog # Версия устарела
    if error == 3:
        return 6,0,0,0,0
    if not sub:
        return 2,0,0,0,0
    return 1,0,name,status,0


def load_numbers(filename):
    try:
        with open(f"Settings/{filename}", "r") as file:
            return [line.strip() for line in file.readlines() if line.strip()]
    except:
        return 2

def load_texts(filename):
    try:
        with open(f"Settings/{filename}", "r", encoding="utf-8") as file:
            return [line.strip() for line in file.readlines()]
    except:
        return 2


def StartNewProfiles(i, script_dir):
    profile_dir = os.path.join(script_dir, "profiles", f"wa_user{i}")
    options = Options()
    #options.add_argument("--headless")
    options.add_argument("--window-size=350,700")
    options.add_argument("--log-level=3")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument(f"--user-data-dir={profile_dir}")
    service = Service(log_path=os.devnull)
    driver = webdriver.Chrome(options=options, service=service)
    driver.get("https://web.whatsapp.com")
    return driver

def StartSelenium(i, script_dir):
    profile_dir = os.path.join(script_dir, "profiles", f"wa_user{i}")
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1000,700")
    options.add_argument("--log-level=1")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument(f"--user-data-dir={profile_dir}")
    service = Service(log_path=os.devnull)
    options.add_argument('--remote-debugging-pipe')
    driver = webdriver.Chrome(options=options, service=service)
    return driver

def CreateProfiles(profile_dir, amount):
    shutil.rmtree(profile_dir)
    os.makedirs(profile_dir)
    for i in range(amount):
        driver = StartNewProfiles(i, profile_dir)
        drivers.append(driver)
        time.sleep(1)
    messagebox.showinfo("Профили WhatsApp", "Войдите в свои аккаунты WhatsApp и нажмите ОК")
    for driver in drivers:
        driver.quit()
    drivers.clear()

def CheckProfiles(script_dir, amount):
    if os.path.exists(f"{script_dir}/profiles"):
        count = 0
        for item in os.listdir(f"{script_dir}/profiles"):
            if os.path.isdir(os.path.join(f"{script_dir}/profiles", item)):
                count += 1
        if amount > count or amount < count:
            result = messagebox.askyesno("Профили WhatsApp", "Количество указанных профилей больше/меньше чем количество существующих профилей. Создать новые?")
            if not result:
                return False
            if result:
                CreateProfiles(script_dir, amount)
                return True
        if amount == count:
            result = messagebox.askyesno("Профили WhatsApp", "Хотите оставить текущие профили?")
            if not result:
                shutil.rmtree(f"{script_dir}/profiles")
                CreateProfiles(script_dir, amount)
                return True
            if result:
                return True
    else:
        CreateProfiles(script_dir, amount)
        return True