import customtkinter as ctk
from PIL import Image, ImageDraw, ImageFont, ImageTk
from tkinter import messagebox
from threading import Thread, Event
import tkinter as tk
import subprocess
import os
import sys

class MainUI:
    def __init__(self):

        def on_close():
            try:
                from func import driversession
                if driversession:
                    for d in driversession:
                        try:
                            d.quit()
                        except:
                            pass
                self.app.quit()
                self.app.destroy()
                sys.exit(0)
            except:
                sys.exit(0)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        self.app = ctk.CTk()
        self.app.title("WhatsApp Tool")
        self.app.geometry("650x500")
        self.app.resizable("false","false")
        try:
            self.app.iconbitmap("Bin/ico.ico")
        except:
            messagebox.showerror("Ошибка", "Проверьте целостность папки Bin или скачайте заново.")
            sys.exit()
        self.app.protocol("WM_DELETE_WINDOW", on_close)

    def run(self):
        self.app.mainloop()

    def animate_dots(self, label):
        current = label.cget("text")
        if current.endswith("..."):
            label.configure(text="Проверка аккаунта")
        else:
            label.configure(text=current + ".")
        label.after(500, lambda: self.animate_dots(label))


    def start_ui(self):
        font1 = ctk.CTkFont(family="Arial", size=40, weight="bold")
        font2 = ctk.CTkFont(family="Arial", size=28, weight="bold")
        font3 = ctk.CTkFont(family="Arial", size=18, weight="bold")

        self.label = ctk.CTkLabel(self.app, text="WA", font=font1, text_color="green")
        self.label2 = ctk.CTkLabel(self.app, text="Tool", font=font2, text_color="white")
        self.label.place(x=262, y=10)
        self.label2.place(x=327, y=20)

        self.label3 = ctk.CTkLabel(self.app, text="Проверка аккаунта", font=font3)
        self.label3.place(x=15, y=75)
        self.animate_dots(self.label3)

    def mainmenu(self, name,status, version):
        font4 = ctk.CTkFont(family="Helvetica", size=14, slant="italic")
        font5 = ctk.CTkFont(family="Helvetica", size=16)
        font6 = ctk.CTkFont(family="Helvetica", size=14, weight="bold")
        self.label3.place_forget()
        self.namelabel = ctk.CTkLabel(self.app, text=f"Status: {status}", font=font4, text_color="green")
        self.namelabel.place(x=13, y=470)
        self.versionlabel = ctk.CTkLabel(self.app, text=f"V{version}", font=ctk.CTkFont(family="Helvetica", size=14), text_color="green")
        self.versionlabel.place(x=605,y=470)
        shadow = ctk.CTkFrame(self.app, width=578, height=370, fg_color="#1a1a1a", corner_radius=15)
        shadow.place(x=40, y=80)
        frame = ctk.CTkFrame(self.app, width=578, height=370, fg_color="#2e2e2e", corner_radius=15)
        frame.place(x=35, y=75)

        def on_choose(choose):
            try:
                if self.thread_running:
                    from func import driversession
                    for d in driversession:
                        try:
                            d.quit()
                        except:
                            pass
                    driversession.clear()
                if self.thread_running3:
                    from func import driversession
                    for d in driversession:
                        try:
                            d.quit()
                        except:
                            pass
                    driversession.clear()
            except:
                pass

            try:
                self.thread_running = False
                self.thread_running2 = False
                self.thread_running3 = False
                self.thread_running4 = False
            except:
                pass

            for widget in frame.winfo_children():
                if widget not in (mode_combobox, self.mode_label):
                    widget.place_forget()

            def validate_integer(text):
                if text == "":
                    return True 
                return text.isdigit()

            def cycle_switch_command():
                p = cycle_switch.get()
                if p == 1:
                    cycle_entry.place(x=260,y=112)
                if p == 0:
                    cycle_entry.place_forget()

            def randomdelay_switch_command():
                p = randomdelay_switch.get()
                if p == 1:
                    randomdelay_entry.place(x=260,y=180)
                    randomdelaychance_entry.place(x=260,y=220)
                if p == 0:
                    randomdelay_entry.place_forget()
                    randomdelaychance_entry.place_forget()

            def new_switch_command():
                p = new_switch.get()
                if p == 1:
                    custom_switch.place(x=260, y= 178)
                if p == 0:
                    custom_switch.place_forget()

            # Send Message
            self.pause_event2 = getattr(self, 'pause_even2', Event())
            self.pause_event2.set()
            self.thread_running2 = getattr(self, 'thread_running2', False)
            def start_sendmessages(event=None):
                if not self.thread_running2:
                    mindelay_val = mindelay_entry.get().strip()
                    maxdelay_val = maxdelay_entry.get().strip()
                    wpdelay_val = wpdelay_entry.get().strip()

                    if not mindelay_val or not maxdelay_val or not wpdelay_val:
                        messagebox.showwarning("Ошибка", "Пожалуйста, заполните все поля")
                        mode_combobox.place(x=20, y=44)
                        return

                    mindelay = int(mindelay_val)
                    maxdelay = int(maxdelay_val)
                    wpdelay = int(wpdelay_val)
                    if mindelay > maxdelay:
                        messagebox.showwarning("Ошибка", "Минимальная задержка не может быть больше максимальной.")
                        mode_combobox.place(x=20, y=44)
                        return
                    mode_combobox.place_forget()
                    self.total_steps = 0
                    self.current_step = 0
                    self.delaylabel = ctk.CTkLabel(frame, text="", font=ctk.CTkFont(family="Helvetica", size=12, weight="bold"))
                    self.delaylabel.place(x=445,y=300)
                    self.progress_label = ctk.CTkLabel(frame, text="Начинаем работу...", font=ctk.CTkFont(family="Helvetica", size=14, weight="bold"))
                    self.progress_label.place(x=30, y=300)
                    self.progress_bar = ctk.CTkProgressBar(frame, width=518, height=18)
                    self.progress_bar.set(0)
                    self.progress_bar.place(x=30, y=330)
                    def startthread_sendmessages():
                        from func import send_messages
                        work = send_messages("numbers.txt", mindelay, maxdelay, wpdelay, self, self.pause_event2)
                        if not work:
                            self.progress_bar.place_forget()
                            self.progress_label.place_forget()
                            mode_combobox.place(x=20, y=44)
                            start_button.configure(text="Запуск")
                            self.thread_running2 = False
                            return
                        mode_combobox.place(x=20, y=44)
                        self.thread_running2 = False
                        start_button.configure(text="Запуск")
                        self.progress_label.configure(text=f"Программа завершила свою работу")
                        self.delaylabel.configure(text="")


                    start_button.configure(text="Пауза")
                    self.thread_running2 = True
                    thread = Thread(target=startthread_sendmessages, daemon=True)
                    thread.start()
                else:
                    if self.pause_event2.is_set():
                        self.pause_event2.clear()
                        mode_combobox.place(x=20, y=44)
                        start_button.configure(text="Продолжить")
                    else:
                        self.pause_event2.set()
                        mode_combobox.place_forget()
                        start_button.configure(text="Пауза")

            # Send Messages Numbers
            self.pause_event = getattr(self, 'pause_event', Event())
            self.pause_event.set()
            self.thread_running = getattr(self, 'thread_running', False)
            def start_sendmessages_numbers(event=None):
                if not self.thread_running:
                    mindelay_val = mindelay_entry.get().strip()
                    maxdelay_val = maxdelay_entry.get().strip()
                    accounts_number_val = accounts_number_enter.get().strip()

                    if not mindelay_val or not maxdelay_val or not accounts_number_val:
                        messagebox.showwarning("Ошибка", "Пожалуйста, заполните все поля")
                        mode_combobox.place(x=20, y=44)
                        return

                    mindelay = int(mindelay_val)
                    maxdelay = int(maxdelay_val)
                    accounts = int(accounts_number_val)

                    if mindelay > maxdelay:
                        messagebox.showwarning("Ошибка", "Минимальная задержка не может быть больше максимальной.")
                        mode_combobox.place(x=20, y=44)
                        return

                    randomdelay_switch_g = randomdelay_switch.get()
                    cycle_switch_g = cycle_switch.get()
                    if randomdelay_switch_g == 1:
                        randomdelay_entry_val = randomdelay_entry.get().strip()
                        randomdelaychance_entry_val = randomdelaychance_entry.get().strip()
                        if not randomdelay_entry_val.isdigit() or not randomdelaychance_entry_val.isdigit():
                            messagebox.showwarning("Ошибка", "Пожалуйста, Введите только цифры")
                            mode_combobox.place(x=20, y=44)
                            return
                        if not randomdelay_entry_val or not randomdelaychance_entry_val:
                            messagebox.showwarning("Ошибка", "Пожалуйста, заполните все поля")
                            mode_combobox.place(x=20, y=44)
                            return
                        randomdelay = int(randomdelay_entry_val)
                        chanceofdelay = int(randomdelaychance_entry_val)
                        if chanceofdelay > 100:
                            messagebox.showwarning("Ошибка", "Шанс задержки не может быть больше 100")
                            mode_combobox.place(x=20, y=44)
                            return
                    else:
                        randomdelay = 0
                        chanceofdelay = 0

                    if cycle_switch_g == 1:
                        cycle_entry_val = cycle_entry.get().strip()
                        if not cycle_entry_val:
                            messagebox.showwarning("Ошибка", "Пожалуйста, заполните все поля")
                            mode_combobox.place(x=20, y=44)
                            return
                        cycle = int(cycle_entry_val)
                    else:
                        cycle = 0
                    mode_combobox.place_forget()

                    self.total_steps = 0
                    self.current_step = 0

                    self.delaylabel = ctk.CTkLabel(frame, text="", font=ctk.CTkFont(family="Helvetica", size=12, weight="bold"))
                    self.delaylabel.place(x=445,y=300)
                    self.cycle_label = ctk.CTkLabel(frame, text="", font=ctk.CTkFont(family="Helvetica", size=11, weight="bold"))
                    self.progress_label = ctk.CTkLabel(frame, text="Начинаем работу...", font=ctk.CTkFont(family="Helvetica", size=12, weight="bold"))
                    self.progress_label.place(x=33, y=300)
                    self.cycle_label.place(x=33, y=280)
                    self.progress_bar = ctk.CTkProgressBar(frame, width=518, height=18)
                    self.progress_bar.set(0)
                    self.progress_bar.place(x=30, y=330)

                    def startthread_sendmessages_numbers():
                        from func import send_messages_numbers
                        work = send_messages_numbers(cycle, accounts, mindelay, maxdelay, "numbers.txt", randomdelay, chanceofdelay, self, self.pause_event)
                        if not work:
                            self.progress_label.configure(text="Завершение работы...")
                            mode_combobox.place(x=20, y=44)
                            from func import driversession
                            if driversession:
                                for d in driversession:
                                    try:
                                        d.quit()
                                    except:
                                        pass
                            start_button.configure(text="Запуск")
                            self.progress_bar.place_forget()
                            self.progress_label.place_forget()
                            self.thread_running = False
                            return
                        mode_combobox.place(x=20, y=44)
                        self.thread_running = False
                        start_button.configure(text="Запуск")
                        self.progress_label.configure(text=f"Программа завершила свою работу")
                        self.delaylabel.configure(text="")

                    thread = Thread(target=startthread_sendmessages_numbers, daemon=True)
                    thread.start()
                    self.thread_running = True
                    start_button.configure(text="Пауза")
                else:
                    if self.pause_event.is_set():
                        self.pause_event.clear()
                        mode_combobox.place(x=20, y=44)
                        start_button.configure(text="Продолжить")
                    else:
                        self.pause_event.set()
                        mode_combobox.place_forget()
                        start_button.configure(text="Пауза")

            #Answer Chats
            self.pause_event3 = getattr(self, 'pause_event', Event())
            self.pause_event.set()
            self.thread_running3 = getattr(self, 'thread_running', False)
            def answer_chats(event=None):
                if not self.thread_running3:
                    delay_v = delay_entry.get().strip()
                    chats_v = chats_entry.get().strip()
                    accounts_v = accounts_number_enter.get().strip()

                    new_v = new_switch.get()
                    old_v = old_switch.get()
                    custom_v = custom_switch.get()
                    if new_v == 1:
                        new = "y"
                    else:
                        new = "n"

                    if custom_v == 1:
                        custom = "y"
                    else:
                        custom = "n"

                    if old_v == 1:
                        old = "y"
                    else:
                        old = "n"

                    if not delay_v or not chats_v or not accounts_v:
                        messagebox.showwarning("Ошибка", "Пожалуйста, заполните все поля")
                        mode_combobox.place(x=20, y=44)
                        return

                    if new_v == 0 and old_v == 0:
                        messagebox.showwarning("Ошибка", "Пожалуйста,  Выберите хотя бы один режим")
                        mode_combobox.place(x=20, y=44)
                        return
                    delay = int(delay_v)
                    chats = int(chats_v)
                    accounts = int(accounts_v)

                    mode_combobox.place_forget()

                    self.total_steps = 0
                    self.current_step = 0

                    self.delaylabel = ctk.CTkLabel(frame, text="", font=ctk.CTkFont(family="Helvetica", size=12, weight="bold"))
                    self.delaylabel.place(x=445,y=300)
                    self.cycle_label = ctk.CTkLabel(frame, text="", font=ctk.CTkFont(family="Helvetica", size=11, weight="bold"))
                    self.progress_label = ctk.CTkLabel(frame, text="Начинаем работу...", font=ctk.CTkFont(family="Helvetica", size=12, weight="bold"))
                    self.progress_label.place(x=30, y=300)
                    self.cycle_label.place(x=30, y=280)
                    self.progress_bar = ctk.CTkProgressBar(frame, width=518, height=18)
                    self.progress_bar.set(0)
                    self.progress_bar.place(x=30, y=330)


                    def startthread_answer_chats():
                        from func import answer_chats
                        work = answer_chats(chats, new, old, custom, accounts, delay, self, self.pause_event3)
                        if not work:
                            self.progress_label.configure(text="Завершение работы...")
                            mode_combobox.place(x=20, y=44)
                            from func import driversession
                            if driversession:
                                for d in driversession:
                                    try:
                                        d.quit()
                                    except:
                                        pass
                            start_button.configure(text="Запуск")
                            self.progress_bar.place_forget()
                            self.progress_label.place_forget()
                            self.thread_running3 = False
                            return
                        mode_combobox.place(x=20, y=44)
                        self.thread_running3 = False
                        start_button.configure(text="Запуск")
                        self.progress_label.configure(text=f"Программа завершила свою работу")
                        self.delaylabel.configure(text="")

                    thread = Thread(target=startthread_answer_chats, daemon=True)
                    thread.start()
                    self.thread_running3 = True
                    start_button.configure(text="Пауза")
                else:
                    if self.pause_event3.is_set():
                        self.pause_event3.clear()
                        mode_combobox.place(x=20, y=44)
                        start_button.configure(text="Продолжить")
                    else:
                        self.pause_event3.set()
                        mode_combobox.place_forget()
                        start_button.configure(text="Пауза")

            # Proqrev
            self.pause_event4 = getattr(self, 'pause_event', Event())
            self.pause_event.set()
            self.thread_running4 = getattr(self, 'thread_running', False)
            def start_proqrev(event=None):
                if not self.thread_running4:
                    delay_v = delay_entry.get().strip()
                    cycle_v = cycle_entry.get().strip()
                    wpdelay_val = wpdelay_entry.get().strip()

                    if not delay_v or not cycle_v or not wpdelay_val:
                        messagebox.showwarning("Ошибка", "Пожалуйста, заполните все поля")
                        mode_combobox.place(x=20, y=44)
                        return

                    delay = int(delay_v)
                    cycle = int(cycle_v)
                    wpdelay = int(wpdelay_val)
                    mode_combobox.place_forget()

                    self.total_steps = 0
                    self.current_step = 0
                    self.delaylabel = ctk.CTkLabel(frame, text="", font=ctk.CTkFont(family="Helvetica", size=12, weight="bold"))
                    self.delaylabel.place(x=445,y=300)
                    self.cycle_label = ctk.CTkLabel(frame, text="", font=ctk.CTkFont(family="Helvetica", size=10, weight="bold"))
                    self.cycle_label.place(x=30, y=280)
                    self.progress_label = ctk.CTkLabel(frame, text="Начинаем работу...", font=ctk.CTkFont(family="Helvetica", size=14, weight="bold"))
                    self.progress_label.place(x=30, y=300)
                    self.progress_bar = ctk.CTkProgressBar(frame, width=518, height=18)
                    self.progress_bar.set(0)
                    self.progress_bar.place(x=30, y=330)
                    def startthread_proqrev():
                        from func import proqrev
                        work = proqrev(cycle,delay,wpdelay,self,self.pause_event4)
                        if not work:
                            mode_combobox.place(x=20, y=44)
                            start_button.configure(text="Запуск")
                            self.thread_running4 = False
                            self.progress_bar.place_forget()
                            self.progress_label.place_forget()
                            return
                        mode_combobox.place(x=20, y=44)
                        self.thread_running4 = False
                        start_button.configure(text="Запуск")
                        self.progress_label.configure(text=f"Программа завершила свою работу")
                        self.delaylabel.configure(text="")

                    start_button.configure(text="Пауза")
                    self.thread_running4 = True
                    thread = Thread(target=startthread_proqrev, daemon=True)
                    thread.start()
                else:
                    if self.pause_event4.is_set():
                        self.pause_event4.clear()
                        mode_combobox.place(x=20, y=44)
                        start_button.configure(text="Продолжить")
                    else:
                        self.pause_event4.set()
                        mode_combobox.place_forget()
                        start_button.configure(text="Пауза")


            if choose == "Рассылка сообщений":
                self.app.bind("<Return>", start_sendmessages)
                vcmd = self.app.register(validate_integer)
                mindelay_label = ctk.CTkLabel(frame, text="Минимальная задержка", font=font6, height=20)
                mindelay_entry = ctk.CTkEntry(frame, validate="key", validatecommand=(vcmd, "%P"), width=80, placeholder_text="60")
                mindelay_entry.place(x=20, y=107)
                mindelay_label.place(x=20,y=82)
                maxdelay_label = ctk.CTkLabel(frame, text="Максимальная задержка", font=font6, height=20)
                maxdelay_entry = ctk.CTkEntry(frame, validate="key", validatecommand=(vcmd, "%P"), width=80, placeholder_text="120")
                maxdelay_entry.place(x=20, y=175)
                maxdelay_label.place(x=20, y=150)
                wpdelay_entry = ctk.CTkEntry(frame, validate="key", validatecommand=(vcmd, "%P"), width=80, placeholder_text="15")
                wpdelay_label = ctk.CTkLabel(frame, text="Задержка запуска WhatsApp Web", font=font6, height=20)
                wpdelay_entry.place(x=270, y=107)
                wpdelay_label.place(x=270,y=82)
                start_button = ctk.CTkButton(frame, text="Запуск", font=ctk.CTkFont(family="Helvetica", size=16), command=start_sendmessages)
                start_button.place(x=360, y=242)

            if choose == "Рассылка сообщений PRO":
                if status == "Trial":
                    messagebox.showerror("Подписки отсутствует", "Необходима подписка Pro для данной функции. Можете связаться для покупки t.me/emil_mmd")
                    mode_combobox.set("Выберите режим")
                if status == "Admin" or status == "Pro":
                    self.app.bind("<Return>", start_sendmessages_numbers)
                    vcmd = self.app.register(validate_integer)
                    mindelay_label = ctk.CTkLabel(frame, text="Минимальная задержка", font=font6, height=20)
                    mindelay_entry = ctk.CTkEntry(frame, validate="key", validatecommand=(vcmd, "%P"), width=80, placeholder_text="60")
                    mindelay_entry.place(x=20, y=107)
                    mindelay_label.place(x=20,y=82)
                    maxdelay_label = ctk.CTkLabel(frame, text="Максимальная задержка", font=font6, height=20)
                    maxdelay_entry = ctk.CTkEntry(frame, validate="key", validatecommand=(vcmd, "%P"), width=80, placeholder_text="120")
                    maxdelay_entry.place(x=20, y=175)
                    maxdelay_label.place(x=20, y=150)
                    
                    cycle_switch = ctk.CTkSwitch(frame, text="Использовать циклы", font=font6, command=cycle_switch_command)
                    cycle_entry = ctk.CTkEntry(frame, width=100, placeholder_text="Кол-во циклов")
                    cycle_switch.place(x=260, y=82)

                    randomdelay_switch = ctk.CTkSwitch(frame, text="Cлучайные задержки", font=font6, command=randomdelay_switch_command)
                    randomdelay_entry = ctk.CTkEntry(frame, placeholder_text="Задержка в минутах", width=140)
                    randomdelaychance_entry = ctk.CTkEntry(frame, placeholder_text="Шанс задержки", width=130)
                    randomdelay_switch.place(x=260, y=150)

                    accounts_number_enter = ctk.CTkEntry(frame, validate="key", validatecommand=(vcmd, "%P"), width=35, placeholder_text="1")
                    accounts_number_label = ctk.CTkLabel(frame, text="Количество аккаунтов", font=font6, height=20)
                    accounts_number_enter.place(x=20, y=242)
                    accounts_number_label.place(x=20, y=217)

                    start_button = ctk.CTkButton(frame, text="Запуск", font=ctk.CTkFont(family="Helvetica", size=16), command=start_sendmessages_numbers)
                    start_button.place(x=360, y=264)

            if choose == "Ответчик на чаты PRO":
                if status == "Trial":
                    messagebox.showerror("Подписки отсутствует", "Необходима подписка Pro для данной функции. Можете связаться для покупки t.me/emil_mmd")
                    mode_combobox.set("Выберите режим")
                if status == "Pro" or status == "Admin":
                    self.app.bind("<Return>", answer_chats)
                    vcmd = self.app.register(validate_integer)
                    delay_label = ctk.CTkLabel(frame, text="Задержка", font=font6, height=20)
                    delay_entry = ctk.CTkEntry(frame, validate="key", validatecommand=(vcmd, "%P"), width=80, placeholder_text="60")
                    delay_entry.place(x=20, y=107)
                    delay_label.place(x=20,y=82)

                    chats_label = ctk.CTkLabel(frame, text="Количество чатов", font=font6, height=20)
                    chats_entry = ctk.CTkEntry(frame, validate="key", validatecommand=(vcmd, "%P"), width=80, placeholder_text="50")
                    chats_entry.place(x=20, y=175)
                    chats_label.place(x=20, y=150)
                    
                    custom_switch = ctk.CTkSwitch(frame, text="Пользовательские ответы", font = font6)

                    new_switch = ctk.CTkSwitch(frame, text="Отвечать на новые сообщения", font=font6, command=new_switch_command)
                    new_switch.place(x=260, y=82)

                    old_switch = ctk.CTkSwitch(frame, text="Отвечать если нет новых", font=font6)
                    old_switch.place(x=260, y=130)


                    accounts_number_enter = ctk.CTkEntry(frame, validate="key", validatecommand=(vcmd, "%P"), width=35, placeholder_text="1")
                    accounts_number_label = ctk.CTkLabel(frame, text="Количество аккаунтов", font=font6, height=20)
                    accounts_number_enter.place(x=20, y=242)
                    accounts_number_label.place(x=20, y=217)

                    start_button = ctk.CTkButton(frame, text="Запуск", font=ctk.CTkFont(family="Helvetica", size=16), command=answer_chats)
                    start_button.place(x=360, y=242)

            if choose == "Прогрев аккаунта":
                self.app.bind("<Return>", start_proqrev)
                vcmd = self.app.register(validate_integer)
                delay_label = ctk.CTkLabel(frame, text="Задержка", font=font6, height=20)
                delay_entry = ctk.CTkEntry(frame, validate="key", validatecommand=(vcmd, "%P"), width=80, placeholder_text="60")
                delay_entry.place(x=20, y=107)
                delay_label.place(x=20,y=82)

                cycle_label = ctk.CTkLabel(frame, text="Количество циклов", font=font6, height=20)
                cycle_entry = ctk.CTkEntry(frame, validate="key", validatecommand=(vcmd, "%P"), width=80, placeholder_text="200")
                cycle_entry.place(x=20, y=175)
                cycle_label.place(x=20, y=150)
                wpdelay_entry = ctk.CTkEntry(frame, validate="key", validatecommand=(vcmd, "%P"), width=80, placeholder_text="15")
                wpdelay_label = ctk.CTkLabel(frame, text="Задержка запуска WhatsApp Web", font=font6, height=20)
                wpdelay_entry.place(x=270, y=107)
                wpdelay_label.place(x=270,y=82)

                start_button = ctk.CTkButton(frame, text="Запуск", font=ctk.CTkFont(family="Helvetica", size=16), command=start_proqrev)
                start_button.place(x=360, y=242)



        self.mode_label = ctk.CTkLabel(frame, text=f"Добро пожаловать, {name}", text_color="white", font=font5)
        mode_combobox = ctk.CTkOptionMenu(frame, values=["Рассылка сообщений", "Прогрев аккаунта", "Рассылка сообщений PRO", "Ответчик на чаты PRO"], command=on_choose, width=200, corner_radius=5, dropdown_font=ctk.CTkFont(family="Helvetica"), text_color="black")
        mode_combobox.set("Выберите режим")

        mode_combobox.place(x=20, y=44)
        self.mode_label.place(x=20, y=7)

    def startingerror(self, index, version, ID, current_version, LinkID, changelog):
        def regnewuser():
            errorlabel = ctk.CTkLabel(frame, text="")
            from utility import CreateNewUser
            name = nickenter.get()
            if name.strip() == "":
                errorlabel.configure(text="Пожалуйста заполните поле", font=("Arial", 12), text_color="red")
                errorlabel.place(x=20, y=130)
                return
            tg = tgenter.get()
            k = CreateNewUser(name, tg)
            if k == 2:
                errorlabel.configure(text="Имя пользователя занято", font=("Arial", 12), text_color="red")
                errorlabel.place(x=20, y=130)
                return
            errorlabel.configure(text="Успешная регистрация!", font=("Arial", 12), text_color="green")
            errorlabel.place(x=20, y=130)
            if k != 3:
                messagebox.showinfo("Регистрация", "Регистрация завершена! Пожалуйста перезапустите программу.")
            self.app.destroy()
            sys.exit()


        if index == 2:
            self.label3.place_forget()
            font3 = ctk.CTkFont(family="Arial", size=18, weight="bold")
            newuserlabel1 = ctk.CTkLabel(self.app, text="Добро пожаловать!", font=font3)
            shadow = ctk.CTkFrame(self.app, width=280, height=300, fg_color="#1a1a1a", corner_radius=15)
            shadow.place(x=195, y=135)
            frame = ctk.CTkFrame(self.app, width=280, height=300, fg_color="#2e2e2e", corner_radius=15)
            frame.place(x=190, y=130)
            newuserlabel2 = ctk.CTkLabel(frame, text="Создать аккаунт", font=("Arial", 16))
            nickenter = ctk.CTkEntry(frame, placeholder_text="Имя пользователя", width=180, height=30)
            tgenter = ctk.CTkEntry(frame, placeholder_text="Ваш TG (опционально)", width=180, height=30)
            tgenter.place(x=15, y=100)
            regbutton = ctk.CTkButton(frame, text="Регистрация", font=("Arial", 16), command=regnewuser, width=130, height=30)
            newuserlabel1.place(x=25, y=75)
            newuserlabel2.place(x=15, y=15)
            nickenter.place(x=15,y=55)
            regbutton.place(x=77, y=230)

        if index == 3:
            messagebox.showerror("Ошибка", "Не удалось получить серийный номер")
            self.app.quit()
        if index == 4:
            messagebox.showerror("Ошибка", "Не удалось обнаружить необходимые файлы. Попробуйте перескачать t.me/watoolx")
            self.app.quit()
        if index == 5:
            def update():
                import subprocess
                import sys
                update_path = "update.exe"
                try:
                    subprocess.Popen([update_path, current_version, LinkID])
                except Exception as e:
                    print(e)
                    messagebox.showerror("Ошибка", "update.exe не обнаружен")
                sys.exit()
            self.label3.place_forget()
            cleaner = " ".join(changelog.split())
            label_update = ctk.CTkLabel(self.app, text=f"Доступна новая версия v{version}", font=ctk.CTkFont(family="Arial", size=18, weight="bold"))
            label_update.place(x=15, y=75)
            changelod_label = ctk.CTkLabel(self.app, text=changelog, font=ctk.CTkFont(family="Arial", size=15), justify="left", anchor="w")
            changelod_label.place(x=23, y=110)
            update_button = ctk.CTkButton(self.app, text="Обновить",font=("Arial", 16), command=update)
            update_button.place(x=23, y=380)
        if index == 6:
            messagebox.showerror("Ошибка подключения", "Не удалось установить соединения. Возможно отсутствует подключение к интернету.")
            self.app.quit()
            sys.exit(0)