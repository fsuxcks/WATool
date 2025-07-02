import customtkinter as ctk
from PIL import Image, ImageDraw, ImageFont, ImageTk
from tkinter import messagebox
from threading import Thread, Event
import queue
import tkinter as tk
import subprocess
import os
import sys

from func import driversession

import tkinter as tk

class ToolTip:
    def __init__(self, widget, text, delay=400):  # delay в мс
        self.widget = widget
        self.text = text
        self.delay = delay
        self.tipwindow = None
        self.after_id = None

        self.widget.bind("<Enter>", self.schedule_show)
        self.widget.bind("<Leave>", self.cancel_and_hide)

    def schedule_show(self, event=None):
        self.after_id = self.widget.after(self.delay, self.show_tip)

    def cancel_and_hide(self, event=None):
        if self.after_id:
            self.widget.after_cancel(self.after_id)
            self.after_id = None
        self.hide_tip()

    def show_tip(self):
        if self.tipwindow or not self.text:
            return

        x = self.widget.winfo_rootx() + 10
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5

        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        tw.attributes("-topmost", True)

        label = tk.Label(
            tw,
            text=self.text,
            justify=tk.LEFT,
            background="#1e1e1e",
            foreground="white",
            relief=tk.SOLID,
            borderwidth=1,
            highlightthickness=1,
            highlightbackground="green",
            font=("Segoe UI", 8)
        )
        label.pack(ipadx=6, ipady=4)

    def hide_tip(self):
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None

class MainUI:
    def __init__(self):

        def on_close():
            try:
                if driversession:
                    for d in driversession:
                        try:
                            d.quit()
                        except:
                            continue
                from utility import drivers
                if drivers:
                    for d in drivers:
                        try:
                            d.quit()
                        except:
                            continue
                self.app.quit()
                sys.exit(0)
            except:
                sys.exit(0)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        self.app = ctk.CTk()
        self.app.title("WhatsApp Tool")
        self.app.geometry("650x550")
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
        self.label3.place(x=25, y=90)
        self.animate_dots(self.label3)

    def mainmenu(self, name,status, version):
        font4 = ctk.CTkFont(family="Helvetica", size=14, slant="italic")
        font5 = ctk.CTkFont(family="Helvetica", size=16, weight="bold")
        font6 = ctk.CTkFont(family="Segoe UI", size=14, weight="bold")
        font7 = ctk.CTkFont(family="Calibri", size=15, weight="bold")

        self.label3.place_forget()
        self.namelabel = ctk.CTkLabel(self.app, text=f"Status: {status}", font=font4, text_color="green")
        self.namelabel.place(x=13, y=520)
        self.versionlabel = ctk.CTkLabel(self.app, text=f"V{version}", font=font4, text_color="green")
        self.versionlabel.place(x=600,y=520)
        shadow = ctk.CTkFrame(self.app, width=578, height=420, fg_color="#1a1a1a", corner_radius=15)
        shadow.place(x=40, y=80)
        frame = ctk.CTkFrame(self.app, width=578, height=420, fg_color="#2e2e2e", corner_radius=15)
        frame.place(x=35, y=75)

        def on_choose(choose):
            try:
                if driversession:
                    for d in driversession:
                        try:
                            d.quit()
                        except:
                            pass
                driversession.clear()
            except:
                pass

            self.thread_running = False
            self.thread_running2 = False
            self.thread_running3 = False
            self.thread_running4 = False

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
                    cycle_entry.place(x=260,y=122)
                if p == 0:
                    cycle_entry.place_forget()

            def randomdelay_switch_command():
                p = randomdelay_switch.get()
                if p == 1:
                    randomdelay_entry.place(x=260,y=190)
                    randomdelaychance_entry.place(x=260,y=230)
                if p == 0:
                    randomdelay_entry.place_forget()
                    randomdelaychance_entry.place_forget()

            def new_switch_command():
                p = new_switch.get()
                if p == 1:
                    custom_switch.place(x=260, y= 168)
                    j = custom_switch.get()
                    if j == 1:
                        send_anyway.place(x=260, y=206)
                if p == 0:
                    custom_switch.place_forget()
                    send_anyway.place_forget()

            def custom_switch_command():
                p = custom_switch.get()
                if p == 1:
                    send_anyway.place(x=260, y=206)
                if p == 0:
                    send_anyway.place_forget()

            def info_proqrev():
                messagebox.showinfo("Информация", "Используется для прогрева аккаунта перед рассылкой. Вы можете сделать расширенную настройку в файле Settings/settings.ini и прочесть инструкцию в папке с программой.")

            def info_answers():
                messagebox.showinfo("Информация", "Читает и отвечает на чаты соответствующими ответами. Необходимо настроить ответы в файле Settings/settings.ini. После запуска программа читает чаты и отправляет соответствующие ответы на них. Подробнее в инструкции в папке с программой. ")

            def info_sendsms():
                messagebox.showinfo("Информация", "Простая рассылка сообщений, работает не в фоновом режиме. Необходимо войти в аккаунт WhatsApp в браузере перед запуском.")

            def info_sendsms_pro():
                messagebox.showinfo("Информация", "Более продвинутая функция рассылки сообщений. Возможность использовать несколько аккаунтов, более продвинуто настроить рассылку, сохранять профили. Подробнее в инструкции.")
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
                        return

                    mindelay = int(mindelay_val)
                    maxdelay = int(maxdelay_val)
                    wpdelay = int(wpdelay_val)
                    if mindelay > maxdelay:
                        messagebox.showwarning("Ошибка", "Минимальная задержка не может быть больше максимальной.")
                        return
                    mode_combobox.place_forget()
                    info_btn.place_forget()
                    self.total_steps = 0
                    self.current_step = 0
                    self.delaylabel = ctk.CTkLabel(frame, text="", font=ctk.CTkFont(family="Helvetica", size=12, weight="bold"))
                    self.delaylabel.place(x=445,y=350)
                    if hasattr(self, "progress_label") and self.progress_label.winfo_exists():
                        self.progress_label.configure(text="Начинаем работу...")
                        self.progress_label.place(x=33, y=350)
                    else:
                        self.progress_label = ctk.CTkLabel(frame, text="Начинаем работу...", font=ctk.CTkFont(family="Helvetica", size=12, weight="bold"))
                        self.progress_label.place(x=33, y=350)
                    self.progress_bar = ctk.CTkProgressBar(frame, width=518, height=18)
                    self.progress_bar.set(0)
                    self.progress_bar.place(x=30, y=380)
                    def startthread_sendmessages():
                        from func import send_messages
                        work = send_messages("numbers.txt", mindelay, maxdelay, wpdelay, self, self.pause_event2)
                        if not work:
                            self.progress_bar.place_forget()
                            self.progress_label.place_forget()
                            mode_combobox.place(x=20, y=50)
                            info_btn.place(x=240, y=51)
                            start_button.configure(text="Запуск")
                            self.thread_running2 = False
                            return
                        mode_combobox.place(x=20, y=50)
                        info_btn.place(x=240, y=51)
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
                        mode_combobox.place(x=20, y=50)
                        info_btn.place(x=240, y=51)
                        start_button.configure(text="Продолжить")
                    else:
                        self.pause_event2.set()
                        mode_combobox.place_forget()
                        info_btn.place_forget()
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
                        return

                    mindelay = int(mindelay_val)
                    maxdelay = int(maxdelay_val)
                    accounts = int(accounts_number_val)

                    if mindelay > maxdelay:
                        messagebox.showwarning("Ошибка", "Минимальная задержка не может быть больше максимальной.")
                        return

                    randomdelay_switch_g = randomdelay_switch.get()
                    cycle_switch_g = cycle_switch.get()
                    if randomdelay_switch_g == 1:
                        randomdelay_entry_val = randomdelay_entry.get().strip()
                        randomdelaychance_entry_val = randomdelaychance_entry.get().strip()
                        if not randomdelay_entry_val.isdigit() or not randomdelaychance_entry_val.isdigit():
                            messagebox.showwarning("Ошибка", "Пожалуйста, Введите только цифры")
                            mode_combobox.place(x=20, y=50)
                            return
                        if not randomdelay_entry_val or not randomdelaychance_entry_val:
                            messagebox.showwarning("Ошибка", "Пожалуйста, заполните все поля")
                            return
                        randomdelay = int(randomdelay_entry_val)
                        chanceofdelay = int(randomdelaychance_entry_val)
                        if chanceofdelay > 100:
                            messagebox.showwarning("Ошибка", "Шанс задержки не может быть больше 100")
                            return
                    else:
                        randomdelay = 0
                        chanceofdelay = 0

                    if cycle_switch_g == 1:
                        cycle_entry_val = cycle_entry.get().strip()
                        if not cycle_entry_val:
                            messagebox.showwarning("Ошибка", "Пожалуйста, заполните все поля")
                            return
                        cycle = int(cycle_entry_val)
                    else:
                        cycle = 0

                    mode_combobox.place_forget()
                    info_btn.place_forget()

                    self.total_steps = 0
                    self.current_step = 0

                    self.delaylabel = ctk.CTkLabel(frame, text="", font=ctk.CTkFont(family="Helvetica", size=12, weight="bold"))
                    self.delaylabel.place(x=445,y=350)
                    self.cycle_label = ctk.CTkLabel(frame, text="", font=ctk.CTkFont(family="Helvetica", size=11, weight="bold"))
                    if hasattr(self, "progress_label") and self.progress_label.winfo_exists():
                        self.progress_label.configure(text="Начинаем работу...")
                        self.progress_label.place(x=33, y=350)
                    else:
                        self.progress_label = ctk.CTkLabel(frame, text="Начинаем работу...", font=ctk.CTkFont(family="Helvetica", size=12, weight="bold"))
                        self.progress_label.place(x=33, y=350)
                    self.cycle_label.place(x=33, y=330)
                    self.progress_bar = ctk.CTkProgressBar(frame, width=518, height=18)
                    self.progress_bar.set(0)
                    self.progress_bar.place(x=30, y=380)

                    def startthread_sendmessages_numbers():
                        from func import send_messages_numbers
                        work = send_messages_numbers(cycle, accounts, mindelay, maxdelay, "numbers.txt", randomdelay, chanceofdelay, self, self.pause_event)
                        if not work:
                            self.progress_label.configure(text="Завершение работы...")
                            mode_combobox.place(x=20, y=50)
                            info_btn.place(x=240, y=51)
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
                            self.cycle_label.place_forget()
                            self.thread_running = False
                            return
                        mode_combobox.place(x=20, y=50)
                        info_btn.place(x=240, y=51)
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
                        mode_combobox.place(x=20, y=50)
                        info_btn.place(x=240, y=51)
                        start_button.configure(text="Продолжить")
                    else:
                        self.pause_event.set()
                        mode_combobox.place_forget()
                        info_btn.place_forget()
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
                    send_anyway_v = send_anyway.get()

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
                        return

                    if new_v == 0 and old_v == 0:
                        messagebox.showwarning("Ошибка", "Пожалуйста,  Выберите хотя бы один режим")
                        return
                    delay = int(delay_v)
                    chats = int(chats_v)
                    accounts = int(accounts_v)

                    mode_combobox.place_forget()
                    info_btn.place_forget()

                    self.total_steps = 0
                    self.current_step = 0

                    self.delaylabel = ctk.CTkLabel(frame, text="", font=ctk.CTkFont(family="Helvetica", size=12, weight="bold"))
                    self.delaylabel.place(x=445,y=350)
                    self.cycle_label = ctk.CTkLabel(frame, text="", font=ctk.CTkFont(family="Helvetica", size=11, weight="bold"))
                    if hasattr(self, "progress_label") and self.progress_label.winfo_exists():
                        self.progress_label.configure(text="Начинаем работу...")
                        self.progress_label.place(x=33, y=350)
                    else:
                        self.progress_label = ctk.CTkLabel(frame, text="Начинаем работу...", font=ctk.CTkFont(family="Helvetica", size=12, weight="bold"))
                        self.progress_label.place(x=33, y=350)
                    self.cycle_label.place(x=30, y=330)
                    self.progress_bar = ctk.CTkProgressBar(frame, width=518, height=18)
                    self.progress_bar.set(0)
                    self.progress_bar.place(x=30, y=380)


                    def startthread_answer_chats():
                        from func import answer_chats
                        work = answer_chats(chats, new, old, custom, send_anyway_v, accounts, delay, self, self.pause_event3)
                        if not work:
                            self.progress_label.configure(text="Завершение работы...")
                            mode_combobox.place(x=20, y=50)
                            info_btn.place(x=240, y=51)
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
                        mode_combobox.place(x=20, y=50)
                        info_btn.place(x=240, y=51)
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
                        mode_combobox.place(x=20, y=50)
                        info_btn.place(x=240, y=51)
                        start_button.configure(text="Продолжить")
                    else:
                        self.pause_event3.set()
                        mode_combobox.place_forget()
                        info_btn.place_forget()
                        start_button.configure(text="Пауза")

            # Proqrev
            self.pause_event4 = getattr(self, 'pause_event', Event())
            self.pause_event.set()
            self.thread_running4 = getattr(self, 'thread_running', False)
            def start_proqrev(event=None):
                if not self.thread_running4:
                    delay_v = delay_entry.get().strip()
                    cycle_delay_v = cycle_delay_entry.get().strip()
                    cycle_v = cycle_entry.get().strip()
                    accounts_v = accounts_entry.get().strip()
                    action_v = action_entry.get().strip()

                    if not delay_v or not cycle_v or not cycle_delay_v or not accounts_v or not action_v:
                        messagebox.showwarning("Ошибка", "Пожалуйста, заполните все поля")
                        return

                    delay = int(delay_v)
                    cycle = int(cycle_v)
                    cycle_delay = int(cycle_delay_v)
                    accounts = int(accounts_v)
                    action = int(action_v)

                    send_photos = send_photos_checkbox.get()
                    send_voice = send_voice_checkbox.get()
                    send_emoji = send_emoji_checkbox.get()
                    send_unknown = unknown_swithc.get()
                    send_random = random_contacts_switch.get()

                    mode_combobox.place_forget()
                    info_btn.place_forget()

                    self.total_steps = 0
                    self.current_step = 0
                    self.cycle_label = ctk.CTkLabel(frame, text="", font=ctk.CTkFont(family="Helvetica", size=11, weight="bold"))
                    self.cycle_label.place(x=477, y=350)
                    if hasattr(self, "progress_label") and self.progress_label.winfo_exists():
                        self.progress_label.configure(text="Начинаем работу...")
                        self.progress_label.place(x=33, y=350)
                    else:
                        self.progress_label = ctk.CTkLabel(frame, text="Начинаем работу...", font=ctk.CTkFont(family="Helvetica", size=12, weight="bold"))
                        self.progress_label.place(x=33, y=350)
                    self.progress_bar = ctk.CTkProgressBar(frame, width=518, height=18)
                    self.progress_bar.set(0)
                    self.progress_bar.place(x=30, y=380)
                    def startthread_proqrev():
                        from func import proqrev
                        work = proqrev(action, accounts,delay,cycle,cycle_delay,send_random,send_unknown,send_photos,send_voice,send_emoji,self,self.pause_event4)
                        if not work:
                            mode_combobox.place(x=20, y=50)
                            info_btn.place(x=240, y=51)
                            start_button.configure(text="Запуск")
                            self.thread_running4 = False
                            self.progress_bar.place_forget()
                            self.progress_label.place_forget()
                            self.cycle_label.place_forget()
                            from func import driversession
                            if driversession:
                                for d in driversession:
                                    try:
                                        d.quit()
                                    except:
                                        pass
                            return
                        mode_combobox.place(x=20, y=50)
                        info_btn.place(x=240, y=51)
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
                        mode_combobox.place(x=20, y=50)
                        info_btn.place(x=240, y=51)
                        start_button.configure(text="Продолжить")
                    else:
                        self.pause_event4.set()
                        mode_combobox.place_forget()
                        info_btn.place_forget()
                        start_button.configure(text="Пауза")


            if choose == "Рассылка сообщений":
                self.app.bind("<Return>", start_sendmessages)
                vcmd = self.app.register(validate_integer)

                info_btn = ctk.CTkButton(frame, text="?", font=font6, command=info_sendsms, width=25, height=25)
                info_btn.place(x=240, y=51)
                mindelay_label = ctk.CTkLabel(frame, text="Минимальная задержка", font=font6, height=20)
                mindelay_entry = ctk.CTkEntry(frame, validate="key", validatecommand=(vcmd, "%P"), width=80, placeholder_text="60")
                mindelay_entry.place(x=20, y=117)
                mindelay_label.place(x=20,y=92)
                maxdelay_label = ctk.CTkLabel(frame, text="Максимальная задержка", font=font6, height=20)
                maxdelay_entry = ctk.CTkEntry(frame, validate="key", validatecommand=(vcmd, "%P"), width=80, placeholder_text="120")
                maxdelay_entry.place(x=20, y=185)
                maxdelay_label.place(x=20, y=160)
                wpdelay_entry = ctk.CTkEntry(frame, validate="key", validatecommand=(vcmd, "%P"), width=80, placeholder_text="15")
                wpdelay_label = ctk.CTkLabel(frame, text="Задержка запуска WhatsApp Web", font=font6, height=20)
                wpdelay_entry.place(x=270, y=117)
                wpdelay_label.place(x=270,y=92)
                start_button = ctk.CTkButton(frame, text="Запуск", font=ctk.CTkFont(family="Segoe UI", size=18), command=start_sendmessages)
                start_button.place(x=360, y=185)

            if choose == "Рассылка сообщений PRO":
                if status == "Trial":
                    messagebox.showerror("Подписки отсутствует", "Необходима подписка Pro для данной функции. Можете связаться для покупки t.me/emil_mmd")
                    mode_combobox.set("Выберите режим")
                if status == "Admin" or status == "Pro":
                    self.app.bind("<Return>", start_sendmessages_numbers)
                    vcmd = self.app.register(validate_integer)
                    info_btn = ctk.CTkButton(frame, text="?", font=font6, command=info_sendsms_pro, width=25, height=25)
                    info_btn.place(x=240, y=51)
                    mindelay_label = ctk.CTkLabel(frame, text="Минимальная задержка", font=font6, height=20)
                    mindelay_entry = ctk.CTkEntry(frame, validate="key", validatecommand=(vcmd, "%P"), width=80, placeholder_text="60")
                    mindelay_entry.place(x=20, y=117)
                    mindelay_label.place(x=20,y=92)
                    maxdelay_label = ctk.CTkLabel(frame, text="Максимальная задержка", font=font6, height=20)
                    maxdelay_entry = ctk.CTkEntry(frame, validate="key", validatecommand=(vcmd, "%P"), width=80, placeholder_text="120")
                    maxdelay_entry.place(x=20, y=185)
                    maxdelay_label.place(x=20, y=160)
                    
                    cycle_switch = ctk.CTkSwitch(frame, text="Использовать циклы", font=font6, command=cycle_switch_command)
                    cycle_entry = ctk.CTkEntry(frame, width=100, placeholder_text="Кол-во циклов")
                    cycle_switch.place(x=260, y=92)

                    randomdelay_switch = ctk.CTkSwitch(frame, text="Cлучайные задержки", font=font6, command=randomdelay_switch_command)
                    randomdelay_entry = ctk.CTkEntry(frame, placeholder_text="Задержка в минутах", width=140)
                    randomdelaychance_entry = ctk.CTkEntry(frame, placeholder_text="Шанс задержки", width=130)
                    randomdelay_switch.place(x=260, y=160)

                    accounts_number_enter = ctk.CTkEntry(frame, validate="key", validatecommand=(vcmd, "%P"), width=35, placeholder_text="1")
                    accounts_number_label = ctk.CTkLabel(frame, text="Количество аккаунтов", font=font6, height=20)
                    accounts_number_enter.place(x=20, y=252)
                    accounts_number_label.place(x=20, y=227)

                    start_button = ctk.CTkButton(frame, text="Запуск", font=ctk.CTkFont(family="Segoe UI", size=18), command=start_sendmessages_numbers)
                    start_button.place(x=360, y=272)

            if choose == "Ответчик на чаты PRO":
                if status == "Trial":
                    messagebox.showerror("Подписки отсутствует", "Необходима подписка Pro для данной функции. Можете связаться для покупки t.me/emil_mmd")
                    mode_combobox.set("Выберите режим")
                if status == "Pro" or status == "Admin":
                    self.app.bind("<Return>", answer_chats)
                    vcmd = self.app.register(validate_integer)

                    info_btn = ctk.CTkButton(frame, text="?", font=font6, command=info_answers, width=25, height=25)
                    info_btn.place(x=240, y=51)

                    delay_label = ctk.CTkLabel(frame, text="Задержка", font=font6, height=20)
                    delay_entry = ctk.CTkEntry(frame, validate="key", validatecommand=(vcmd, "%P"), width=80, placeholder_text="60")
                    delay_entry.place(x=20, y=117)
                    delay_label.place(x=20,y=92)

                    chats_label = ctk.CTkLabel(frame, text="Количество чатов", font=font6, height=20)
                    chats_entry = ctk.CTkEntry(frame, validate="key", validatecommand=(vcmd, "%P"), width=80, placeholder_text="50")
                    chats_entry.place(x=20, y=185)
                    chats_label.place(x=20, y=160)
                    
                    custom_switch = ctk.CTkSwitch(frame, text="Пользовательские ответы [?]", font = font6, command=custom_switch_command)
                    ToolTip(custom_switch, "При включении на каждое входящее сообщение отправляется индивидуальный ответ из словаря Settings/settings.ini. \nПри выключении всем контактам отправляется одно и то же сообщение.")

                    new_switch = ctk.CTkSwitch(frame, text="Отвечать на новые сообщения", font=font6, command=new_switch_command)
                    new_switch.place(x=260, y=92)

                    old_switch = ctk.CTkSwitch(frame, text="Отвечать если нет новых", font=font6)
                    old_switch.place(x=260, y=130)

                    send_anyway = ctk.CTkSwitch(frame, text="Отправить если нет совпадений [?]", font=font6)
                    ToolTip(send_anyway, "Отправляется сообщение по умолчанию, если нет совпадений в settings.ini.")


                    accounts_number_enter = ctk.CTkEntry(frame, validate="key", validatecommand=(vcmd, "%P"), width=35, placeholder_text="1")
                    accounts_number_label = ctk.CTkLabel(frame, text="Количество аккаунтов", font=font6, height=20)
                    accounts_number_enter.place(x=20, y=253)
                    accounts_number_label.place(x=20, y=228)

                    start_button = ctk.CTkButton(frame, text="Запуск", font=ctk.CTkFont(family="Segoe UI", size=18), command=answer_chats)
                    start_button.place(x=360, y=280)

            if choose == "Прогрев аккаунта PRO":
                if status == "Trial":
                    messagebox.showerror("Подписки отсутствует", "Необходима подписка Pro для данной функции. Можете связаться для покупки t.me/emil_mmd")
                    mode_combobox.set("Выберите режим")
                if status == "Pro" or status == "Admin":
                    self.app.bind("<Return>", start_proqrev)
                    vcmd = self.app.register(validate_integer)

                    info_btn = ctk.CTkButton(frame, text="?", font=font6, command=info_proqrev, width=25, height=25)
                    info_btn.place(x=240, y=51)


                    delay_label = ctk.CTkLabel(frame, text="Задержка", font=font6, height=20)
                    delay_entry = ctk.CTkEntry(frame, validate="key", validatecommand=(vcmd, "%P"), width=80, placeholder_text="30")
                    delay_label.place(x=20, y=92)
                    delay_entry.place(x=20, y=117)

                    cycle_label = ctk.CTkLabel(frame, text="Кол-во циклов", font=font6, height=20)
                    cycle_entry = ctk.CTkEntry(frame, validate="key", validatecommand=(vcmd, "%P"), width=80, placeholder_text="200")
                    cycle_label.place(x=20, y=152)
                    cycle_entry.place(x=20, y=177)

                    cycle_delay_label = ctk.CTkLabel(frame, text="Задержка между циклами (мин)", font=font6, height=20)
                    cycle_delay_entry = ctk.CTkEntry(frame, validate="key", validatecommand=(vcmd, "%P"), width=80, placeholder_text="10")
                    cycle_delay_label.place(x=20, y=212)
                    cycle_delay_entry.place(x=20, y=237)

                    action_label = ctk.CTkLabel(frame, text="Действий на цикл", font=font6, height=20)
                    action_entry = ctk.CTkEntry(frame, validate="key", validatecommand=(vcmd, "%P"), width=70 , placeholder_text="8")
                    action_label.place(x=20, y=272)
                    action_entry.place(x=20, y=297)


                    accounts_entry = ctk.CTkEntry(frame, validate="key", validatecommand=(vcmd, "%P"), width=70 , font=font6, placeholder_text="2")
                    accounts_label = ctk.CTkLabel(frame, text="Кол-во аккаунтов", font=font6, height=20)
                    accounts_entry.place(x=155, y=117)
                    accounts_label.place(x=155, y=92)

                    send_photos_checkbox = ctk.CTkCheckBox(frame, text="Отправлять фото", font=font6)
                    send_photos_checkbox.place(x=325, y=97)

                    send_voice_checkbox = ctk.CTkCheckBox(frame, text="Отправлять голосовые", font=font6)
                    send_voice_checkbox.place(x=325, y=137)

                    send_emoji_checkbox = ctk.CTkCheckBox(frame, text="Стикеры, GIF", font=font6)
                    send_emoji_checkbox.place(x=325, y=177)

                    unknown_swithc = ctk.CTkSwitch(frame, text="Незнакомые номера [?]", font=font6)
                    ToolTip(unknown_swithc, "Случайная отправка на номер из numbers.txt, шанс указываестя в Settings/settings.ini")
                    unknown_swithc.place(x=325, y=217)

                    random_contacts_switch = ctk.CTkSwitch(frame, text="Случайные контакты [?]", font=font6)
                    ToolTip(random_contacts_switch, "Контакты из contacts.txt выбираются случайно, если отключено то отправляются по очереди.")
                    random_contacts_switch.place(x=325, y=257)

                    start_button = ctk.CTkButton(frame, text="Запуск", font=ctk.CTkFont(family="Segoe UI", size=18), command=start_proqrev)
                    start_button.place(x=360, y=297)



        self.mode_label = ctk.CTkLabel(frame, text=f"Добро пожаловать, {name}", text_color="white", font=font5)
        mode_combobox = ctk.CTkOptionMenu(frame, values=["Рассылка сообщений", "Рассылка сообщений PRO", "Прогрев аккаунта PRO", "Ответчик на чаты PRO"], command=on_choose, width=210, corner_radius=5, dropdown_font=ctk.CTkFont(family="Helvetica"), text_color="black", font=font7)
        mode_combobox.set("Выберите режим")

        mode_combobox.place(x=20, y=50)
        self.mode_label.place(x=20, y=10)

    def startingerror(self, index, version, current_version, changelog, name, status, LinkID):
        def regnewuser(q):
            from utility import CreateNewUser
            name = nickenter.get()
            if name.strip() == "":
                q.put(6)
            else:
                tg = tgenter.get()
                k = CreateNewUser(name, tg)
                q.put(k)

        def regnewuserthread(event=None):
            errorlabel.configure(text="Регистрация...", text_color="green")
            q = queue.Queue()
            thread = Thread(target=regnewuser, daemon=True, args=(q,))
            thread.start() 
            def check_result():
                if not q.empty():
                    k = q.get()
                    if k == 6:
                        errorlabel.configure(text="Пожалуйста заполните поле", text_color="red")
                    elif k == 5:
                        messagebox.showerror("Ошибка", "Не удалось получить серийный номер")
                    elif k == 4:
                        messagebox.showerror("Ошибка", "Не удалось подключиться. Возможно отсутствует подключение к интернету")
                    elif k == 2:
                        errorlabel.configure(text="Имя пользователя занято", text_color="red")
                    elif k == 3:
                        errorlabel.configure(text="Успешная регистрация!", text_color="green")
                        messagebox.showinfo("Регистрация", "Срок использование пробного периода закончился.Вам доступна Trial версия. Перезапустите программу. Покупка PRO - t.me/emil_mmd")
                        self.app.destroy()
                        sys.exit()
                    elif k == 1:
                        errorlabel.configure(text="Успешная регистрация!", text_color="green")
                        messagebox.showinfo("Регистрация", "Регистрация завершена! Перезапустите программу.")
                        self.app.destroy()
                        sys.exit()
                else:
                    self.app.after(100, check_result)

            check_result()

        if index == 2:
            self.app.bind("<Return>", regnewuserthread)
            self.label3.place_forget()
            font3 = ctk.CTkFont(family="Arial", size=18, weight="bold")
            font1 = ctk.CTkFont(family="Arial", size=13, weight="bold")
            newuserlabel1 = ctk.CTkLabel(self.app, text="Добро пожаловать!", font=font3)
            shadow = ctk.CTkFrame(self.app, width=280, height=300, fg_color="#1a1a1a", corner_radius=15)
            shadow.place(x=195, y=165)
            frame = ctk.CTkFrame(self.app, width=280, height=300, fg_color="#2e2e2e", corner_radius=15)
            frame.place(x=190, y=160)
            errorlabel = ctk.CTkLabel(frame, text="",  font=font1)
            errorlabel.place(x=20, y=136)
            newuserlabel2 = ctk.CTkLabel(frame, text="Создать аккаунт", font=("Arial", 16))
            nickenter = ctk.CTkEntry(frame, placeholder_text="Имя пользователя", width=180, height=30)
            tgenter = ctk.CTkEntry(frame, placeholder_text="Ваш TG (опционально)", width=180, height=30)
            tgenter.place(x=15, y=100)
            regbutton = ctk.CTkButton(frame, text="Регистрация", font=("Arial", 16), command=regnewuserthread, width=130, height=30)
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
            def skip():
                update_button.place_forget()
                label_update.place_forget()
                changelod_label.place_forget()
                continuebtn.place_forget()
                self.mainmenu(name, status, current_version)
            def update():
                import subprocess
                import sys
                update_path = "update.exe"
                try:
                    subprocess.Popen([update_path, current_version, LinkID])
                except Exception as e:
                    print(e)
                    messagebox.showerror("Ошибка", "update.exe не обнаружен")
                self.app.destroy()
                sys.exit()
            self.label3.place_forget()
            cleaner = " ".join(changelog.split())
            label_update = ctk.CTkLabel(self.app, text=f"Доступна новая версия v{version}", font=ctk.CTkFont(family="Arial", size=18, weight="bold"))
            label_update.place(x=15, y=75)
            changelod_label = ctk.CTkLabel(self.app, text=changelog, font=ctk.CTkFont(family="Arial", size=15), justify="left", anchor="w")
            changelod_label.place(x=23, y=110)
            continuebtn = ctk.CTkButton(self.app, text="Пропустить", font=ctk.CTkFont(family="Arial", size=16, weight="bold"), height=28, command=skip)
            continuebtn.place(x=23, y=460)
            update_button = ctk.CTkButton(self.app, text="Скачать и установить",font=ctk.CTkFont(family="Arial", size=16, weight="bold"), command=update, height=28)
            update_button.place(x=23, y=410)
        if index == 6:
            messagebox.showerror("Ошибка подключения", "Не удалось установить соединения. Возможно отсутствует подключение к интернету.")
            self.app.quit()
            sys.exit(0)