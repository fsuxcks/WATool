import os
import sys
import time
import random
import shutil
from datetime import datetime,timezone,timedelta
import pywhatkit as kit
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from tkinter import messagebox
import configparser

from utility import *

driversession = []


def proqrev(cycle, ping, waittime, ui, pause_event):
    try:
        numbers = load_numbers(numbers_file)
    except:
        messagebox.showerror("Ошибка", "Не удалось загрузить файл numbers.txt")
        return False
    try:
        messages = load_texts("text.txt")
    except:
        messagebox.showerror("Ошибка", "x x Не удалось загрузить файл text.txt")
        return False

    if len(numbers) == 0:
        messagebox.showerror("Ошибка", "Файл numbers.txt пустой!")
        return False
    if numbers == 2:
        messagebox.showerror("Ошибка", "Не удалось обнаружить файл numbers.txt")
        return False

    if len(messages) == 0:
        messagebox.showerror("Ошибка", "Файл text.txt пустой!")
        return False
    if messages == 2:
        messagebox.showerror("Ошибка", "Не удалось обнаружить файл text.txt")
        return False

    ui.total_steps = cycle * len(numbers)
    for n in range(cycle):
        pause_event.wait()
        ui.cycle_label.configure(text=f"Цикл №{n+1}")
        for i, number in enumerate(numbers, 1):
            pause_event.wait()
            message = random.choice(messages)
            ui.progress_label.configure(text=f"{i}/{len(numbers)} Отправка на {number}...")
            phone = str(number).strip()
            msg = str(message)
            try:
                kit.sendwhatmsg_instantly(number, msg, wait_time=waittime, tab_close=True)
                ui.progress_label.configure(text=f"{i}/{len(numbers)} Отправлено в {datetime.now().hour}:{datetime.now().minute}:{datetime.now().second} на {number}")
                ui.current_step += 1
                progress = ui.current_step / ui.total_steps
                ui.progress_bar.set(progress)
                for i in range(ping):
                    pause_event.wait()
                    ui.delaylabel.configure(text=f"Задержка:  {ping-i}с")
                    time.sleep(1)
            except Exception as e:
                ui.progress_label.configure(text=f"Ошибка при отпрвке на {number}")
                time.sleep(3)
    return True

def send_messages(numbers_file,min,max,wait_time, ui, pause_event):

    try:
        numbers = load_numbers(numbers_file)
    except:
        messagebox.showerror("Ошибка", "Не удалось загрузить файл numbers.txt")
        return False
    try:
        messages = load_texts("text.txt")
    except:
        messagebox.showerror("Ошибка", "x x Не удалось загрузить файл text.txt")
        return False

    if len(numbers) == 0:
        messagebox.showerror("Ошибка", "Файл numbers.txt пустой!")
        return False
    if numbers == 2:
        messagebox.showerror("Ошибка", "Не удалось обнаружить файл numbers.txt")
        return False

    if len(messages) == 0:
        messagebox.showerror("Ошибка", "Файл text.txt пустой!")
        return False
    if messages == 2:
        messagebox.showerror("Ошибка", "Не удалось обнаружить файл text.txt")
        return False

    ui.total_steps = len(numbers)
    ui.current_step = 0

    for i, number in enumerate(numbers, 1):
        pause_event.wait()
        message = random.choice(messages)
        ui.progress_label.configure(text=f"{i}/{len(numbers)} Отправка на {number}")
        pause_event.wait()

        ping = random.randint(min,max)
        try:
            phone = str(number).strip()
            if not phone.startswith("+"):
                raise ValueError(f"[!] Номер должен начинаться с '+': {phone}")
                time.sleep(10)
                sys.exit()
            msg = str(message)

            kit.sendwhatmsg_instantly(
                phone_no=phone,
                message=msg,
                wait_time=wait_time,
                tab_close=True
            )

            ui.current_step += 1
            progress = ui.current_step / ui.total_steps
            ui.progress_bar.set(progress)
            ui.progress_label.configure(text=f"{i}/{len(numbers)} Отправлено на {number}")
            with open("sent_numbers_trial.txt", 'a', encoding='utf-8') as file:
                        file.write(f"{phone}\n")

            for i in range(ping):
                pause_event.wait()
                ui.delaylabel.configure(text=f"Задержка:  {ping-i}с")
                time.sleep(1)
        except Exception as e:
            ui.progress_label.configure(text=f"Ошибка при отпрвке на {phone}")
            with open("failed_numbers_trial.txt", 'a', encoding='utf-8') as file:
                        file.write(f"{phone}\n")
            time.sleep(3)
    return True

def send_messages_numbers(cycle, amount, mindelay, maxdelay,numbers_file,bigdelay,chanceofdelay, ui, pause_event):
    try:
        numbers = load_numbers(numbers_file)
    except:
        messagebox.showerror("Ошибка", "Не удалось загрузить файл numbers.txt")
        return False
    try:
        messages = load_texts("text.txt")
    except:
        messagebox.showerror("Ошибка", "x x Не удалось загрузить файл text.txt")
        return False

    if len(numbers) == 0:
        messagebox.showerror("Ошибка", "Файл numbers.txt пустой!")
        return False
    if numbers == 2:
        messagebox.showerror("Ошибка", "Не удалось обнаружить файл numbers.txt")
        return False

    if len(messages) == 0:
        messagebox.showerror("Ошибка", "Файл text.txt пустой!")
        return False
    if messages == 2:
        messagebox.showerror("Ошибка", "Не удалось обнаружить файл text.txt")
        return False

    ui.total_steps = len(numbers) if cycle == 0 else len(numbers) * cycle

    drivers = []
    profile_dir = os.path.join(os.getenv("APPDATA"), "WATool")
    if not os.path.exists(profile_dir):
        os.makedirs(profile_dir)
    script_dir = profile_dir


    def checkforbigdelay():
        chance = random.randint(1,100)
        if chance > chanceofdelay or chance == chanceofdelay:
            return False
        else:
            return True
    ui.progress_label.configure(text="Запускаем профили...")
    check = CheckProfiles(script_dir, amount)
    if not check:
        return
    ui.progress_label.configure(text="Запускаем сессии...")
    driversession.clear()
    for i in range(amount):
        drivernew = StartSelenium(i, script_dir)
        driversession.append(drivernew)
        time.sleep(2)
    time.sleep(2)
    cycle = cycle+1
    for m in range(cycle):
        ui.current_step = 0
        if cycle > 1:
            ui.cycle_label.configure(text=f"Цикл №{m+1}")
        for i, number in enumerate(numbers):
            pause_event.wait()
            msg = random.choice(messages)
            if len(driversession) == 1:
                profilenum = 1
            else:
                profilenum = i+1
                if profilenum > len(driversession):
                    profilenum = profilenum - len(driversession)
            ui.delaylabel.configure(text="")
            ui.progress_label.configure(text=f"{i+1}/{len(numbers)} Отправка на {number} через профиль #{profilenum}")
            driverfor = driversession[i % len(driversession)]
            driverfor.execute_script(f"window.open('https://web.whatsapp.com/send?phone={number}&text={msg}', '_blank');")
            driverfor.switch_to.window(driverfor.window_handles[1])
            time.sleep(2)
            try:
                WebDriverWait(driverfor, 12).until(EC.presence_of_element_located((By.ID, "pane-side")))
                time.sleep(2.5)
            except:
                driverfor.quit()
                driversession.remove(driverfor)
                if not driversession:
                    messagebox.showinfo("Профили WhatsApp", "Программа завершила свою работу так как все текущие профили потеряли доступ либо получили бан")
                    return False
                ui.progress_label.configure(text="Не удалось войти в профиль #{profilenum}, возможно аккаунт заблокирован или потерял доступ")
                time.sleep(3)
                continue
            try:
                send_button = driverfor.find_element(By.XPATH, '/html/body/div[1]/div/div/div[3]/div/div[4]/div/footer/div[1]/div/span/div/div[2]/div/div[4]/button/span')
                send_button.click()

                with open("sent_numbers.txt", 'a', encoding='utf-8') as file:
                        file.write(f"{number}\n")
                if chanceofdelay > 0:
                    if checkforbigdelay():
                        ui.progress_label.configure(text=f"{i+1}/{len(numbers)} Отправлено на {number} в {datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}")
                        ui.current_step += 1
                        progress = ui.current_step / ui.total_steps
                        ui.progress_bar.set(progress)
                        if i+1 == len(numbers) and cycle == 1:
                            time.sleep(2)
                            break
                        for i in range(bigdelay):
                            pause_event.wait()
                            ui.delaylabel.configure(text=f"Задержка:  {bigdelay-i}м")
                            time.sleep(60)
                            k = driverfor.title
                    else:
                        delay = random.randint(mindelay,maxdelay)    
                        ui.progress_label.configure(text=f"{i+1}/{len(numbers)} Отправлено на {number} в {datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}")
                        ui.current_step += 1
                        progress = ui.current_step / ui.total_steps
                        ui.progress_bar.set(progress)
                        if i+1 == len(numbers) and cycle == 1:
                            time.sleep(2)
                            break
                        for i in range(delay):
                            pause_event.wait()
                            ui.delaylabel.configure(text=f"Задержка:  {delay-i}с")
                            k = driverfor.title
                            time.sleep(1)
                if chanceofdelay == 0:
                    delay = random.randint(mindelay,maxdelay)
                    ui.progress_label.configure(text=f"{i+1}/{len(numbers)} Отправлено на {number} в {datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}")
                    ui.current_step += 1
                    progress = ui.current_step / ui.total_steps
                    ui.progress_bar.set(progress)
                    if i+1 == len(numbers) and cycle == 1:
                        time.sleep(2)
                        break
                    for i in range(delay):
                        pause_event.wait()
                        ui.delaylabel.configure(text=f"Задержка:  {delay-i}с")
                        k = driverfor.title
                        time.sleep(1)
            except:
                try:
                    send_button = driverfor.find_element(By.XPATH, '/html/body/div[1]/div/div/div[3]/div/div[4]/div/footer/div[1]/div/span/div/div[2]/div[2]/button/span')
                    send_button.click()
                    
                    with open("sent_numbers.txt", 'a', encoding='utf-8') as file:
                        file.write(f"{number}\n")
                    if chanceofdelay > 0:
                        if checkforbigdelay():
                            ui.progress_label.configure(text=f"{i+1}/{len(numbers)} Отправлено на {number} в {datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}")
                            ui.current_step += 1
                            progress = ui.current_step / ui.total_steps
                            ui.progress_bar.set(progress)
                            if i+1 == len(numbers) and cycle == 1:
                                time.sleep(2)
                                break
                            for i in range(bigdelay):
                                pause_event.wait()
                                ui.delaylabel.configure(text=f"Задержка:  {bigdelay-i}м")
                                time.sleep(60)
                                k = driverfor.title
                        else:
                            delay = random.randint(mindelay,maxdelay)
                            ui.progress_label.configure(text=f"{i+1}/{len(numbers)} Отправлено на {number} в {datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}")
                            ui.current_step += 1
                            progress = ui.current_step / ui.total_steps
                            ui.progress_bar.set(progress)
                            if i+1 == len(numbers) and cycle == 1:
                                time.sleep(2)
                                break
                            for i in range(delay):
                                pause_event.wait()
                                ui.delaylabel.configure(text=f"Задержка:  {delay-i}с")
                                k = driverfor.title
                                time.sleep(1)
                    if chanceofdelay == 0:
                        delay = random.randint(mindelay,maxdelay)
                        ui.progress_label.configure(text=f"{i+1}/{len(numbers)} Отправлено на {number} в {datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}")
                        ui.current_step += 1
                        progress = ui.current_step / ui.total_steps
                        ui.progress_bar.set(progress)
                        if i+1 == len(numbers) and cycle == 1:
                            time.sleep(2)
                            break
                        for i in range(delay):
                            pause_event.wait()
                            ui.delaylabel.configure(text=f"Задержка:  {delay-i}с")
                            k = driverfor.title
                            time.sleep(1)
                except Exception as e:
                    ui.delaylabel.configure(text="")
                    print(e)
                    ui.progress_label.configure(text=f"{i+1}/{len(numbers)} Не удалось отправить на номер {number}")
                    with open("failed_numbers.txt", 'a', encoding='utf-8') as file:
                        file.write(f"{number}\n")
                    time.sleep(3)
            
            driverfor.close()
            driverfor.switch_to.window(driverfor.window_handles[0])
    for drivers in driversession:
        drivers.quit()
    driversession.clear()
    return True

def answer_chats(chatscount,ifanswer,ifnoanswer,customsettings, amount, delay, ui, pause_event):
    delaytime = delay
    config = configparser.ConfigParser()
    try:
        config.read("Settings/settings.ini", encoding="utf-8")
    except:
        messagebox.showerror("Ошибка", "Файл settings.ini отсутствует")
        return False
    try:
        answerA = config.get("general","answerA")
        answerB = config.get("general","answerB")
        vocabulary = dict(config.items('vocabulary'))
        vocabulary_lower = {k.lower(): v for k, v in vocabulary.items()}
    except Exception as e:
        messagebox.showerror("Ошибка", "Файл settings.ini настроен неверно")
        return False

    drivers = []
    ui.total_steps = chatscount

    profile_dir = os.path.join(os.getenv("APPDATA"), "WATool", "Answers")
    if not os.path.exists(profile_dir):
        os.makedirs(profile_dir)


    def send_message(text, driver):
        actions = ActionChains(driver)
        try:
            actions = ActionChains(driver)
            input_box = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[3]/div/div[4]/div/footer/div[1]/div/span/div/div[2]/div/div[3]/div[1]/p')
            input_box.click()
            text = text.encode().decode('unicode_escape')
            good_text = text.encode("latin1").decode("utf-8")
            for line in good_text.split('\n'):
                input_box.send_keys(line)
                input_box.send_keys(Keys.SHIFT, Keys.ENTER)
            input_box.send_keys(Keys.ENTER)
            actions.perform()
            return True
        except:
            try:
                input_box = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[3]/div/div[4]/div/footer/div[1]/div/span/div/div[2]/div[1]/div[2]/div[1]/p")
                input_box.click()
                text = text.encode().decode('unicode_escape')
                good_text = text.encode("latin1").decode("utf-8")
                for line in good_text.split('\n'):
                    input_box.send_keys(line)
                    input_box.send_keys(Keys.SHIFT, Keys.ENTER)
                input_box.send_keys(Keys.ENTER)
                actions.perform()
            except:
                return False

            return True

    def checkLastMessage(k, title):
        messages = drivernew.find_elements(By.XPATH, '//div[contains(@class,"message-in") or contains(@class,"message-out")]')
        if "message-in" in messages[-1].get_attribute("class"):
            if customsettings == "n" and ifanswer == "y":
                last_msg = messages[-1].text.split('\n')[0]
                if send_message(answerA, drivernew):
                    ui.progress_label.configure(text=f"{k}/{chatscount} Отправлено на {title} на новое сообщение")
                    ui.current_step += 1
                    progress = ui.current_step / ui.total_steps
                    ui.progress_bar.set(progress)
                    for i in range(delay):
                        pause_event.wait()
                        ui.delaylabel.configure(text=f"Задержка:  {delay-i}с")
                        k = drivernew.title
                        time.sleep(1)
                else:
                    ui.progress_label.configure(text=f"{k}/{chatscount} Не удалось отправить сообщение на {title}")
                    ui.current_step += 1
                    progress = ui.current_step / ui.total_steps
                    ui.progress_bar.set(progress)
                    time.sleep(3)
            if customsettings == "y":
                last_msg = messages[-1].text.split('\n')[0]
                last_msg_lower = last_msg.lower()
                response = vocabulary_lower.get(last_msg_lower)
                if response is None:
                    ui.progress_label.configure(text=f"{k}/{chatscount} Новое сообщение от {title} отсутствует в словаре")
                    ui.current_step += 1
                    progress = ui.current_step / ui.total_steps
                    ui.progress_bar.set(progress)
                else:
                    if send_message(response, drivernew):
                        ui.progress_label.configure(text=f"{k}/{chatscount} Новое сообщение от {number} отправлен ответ")
                        ui.current_step += 1
                        progress = ui.current_step / ui.total_steps
                        ui.progress_bar.set(progress)
                        for i in range(delay):
                            pause_event.wait()
                            ui.delaylabel.configure(text=f"Задержка:  {delay-i}с")
                            k = drivernew.title
                            time.sleep(1)
                    else:
                        ui.progress_label.configure(text=f"{k}/{chatscount} Не удалось отправить сообщение на {title}")
                        ui.current_step += 1
                        progress = ui.current_step / ui.total_steps
                        ui.progress_bar.set(progress)
                        time.sleep(3)

        if "message-out" in messages[-1].get_attribute("class"):
            if ifnoanswer == "y":
                if send_message(answerB, drivernew):
                    ui.progress_label.configure(text=f"{k}/{chatscount} Отправлно на {title} на старое сообщение")
                    ui.current_step += 1
                    progress = ui.current_step / ui.total_steps
                    ui.progress_bar.set(progress)
                    for i in range(delay):
                        pause_event.wait()
                        ui.delaylabel.configure(text=f"Задержка:  {delay-i}с")
                        k = drivernew.title
                        time.sleep(1)
                else:
                    ui.progress_label.configure(text=f"{k}/{chatscount} Не удалось отправить сообщение на {title}")
                    ui.current_step += 1
                    progress = ui.current_step / ui.total_steps
                    ui.progress_bar.set(progress)
                    time.sleep(3)


    def getChats(): 
        chat_titles = set()
        last_top_chat = ""
        k = 0

        def scroll_chat_list():
            chat_list = drivernew.find_element(By.ID, "pane-side")
            drivernew.execute_script("arguments[0].scrollTop += 50;", chat_list)

        def waitUntilChat(chat,k, title):
            for _ in range(100):
                try:
                    chat.click()
                    checkLastMessage(k, title)
                    return True
                except:
                    scroll_chat_list()
                    time.sleep(0.5)

        while len(chat_titles) < chatscount:
            pause_event.wait()
            chats = drivernew.find_elements(By.CSS_SELECTOR, "div[role='listitem']")
            try:
                for chat in chats:
                    k = k+1
                    top_chat_title = chat.find_element(By.CSS_SELECTOR, "div._ak8q span[title]").get_attribute("title")
                    if top_chat_title != last_top_chat:
                        title = chat.find_element(By.CSS_SELECTOR, "div._ak8q span[title]").get_attribute("title")
                        if title and title not in chat_titles:
                            chat_titles.add(title)
                            ui.progress_label.configure(text=f"{len(chat_titles)}/{len(chatscount)} Чтение чата {title}...")
                            ui.delaylabel.configure(text="")
                            if waitUntilChat(chat, k, title):
                                time.sleep(0.2)
                            if len(chat_titles) >= chatscount:
                                return
                        last_top_chat = top_chat_title
                        time.sleep(0.5)
            except:
                scroll_chat_list()
                time.sleep(0.7)
            scroll_chat_list()
            time.sleep(0.7)


    ui.progress_label.configure(text="Запускаем профили...")
    check = CheckProfiles(profile_dir, amount)
    if not check:
        return
    driversession.clear()
    for i in range(amount):
        ui.progress_label.configure(text="Запускаем сессию...")
        drivernew = StartSelenium(i, profile_dir)
        driversession.append(drivernew)
        drivernew.get("https://web.whatsapp.com")
        time.sleep(4)
        try:
            WebDriverWait(drivernew, 12).until(EC.presence_of_element_located((By.ID, "pane-side")))
        except:
            drivernew.quit()
            driversession.remove(drivernew)
            if not driversession:
                messagebox.showinfo("Профили WhatsApp", "Программа завершила свою работу так как все текущие профили потеряли доступ либо получили бан")
                return False
            ui.progress_label.configure(text="Не удалось войти в профиль #{profilenum}, возможно аккаунт заблокирован или потерял доступ")
            time.sleep(3)
            continue
        if amount > 1:
            ui.cycle_label.configure(text=f"Аккаунт #{i+1}")
        getChats()
        drivernew.quit()
    driversession.clear()
    return True