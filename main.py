currentversion = "0.91"

import logging
import traceback
import threading
import queue

from ui import *
from utility import *

logging.basicConfig(filename='Bin/Logs.log',filemode='a',level=logging.ERROR,format='%(asctime)s - %(levelname)s - %(message)s')
name,status = "",""
result_queue = queue.Queue()


try:
    def main():
        ui = MainUI()
        ui.start_ui()

        def startcheck():
            serial = GetSerial()
            index, version, name, status, changelog = CheckSub(serial, currentversion)
            result_queue.put((index, version, name, status, changelog))

            def startmainmenu():
                idx, ver, n, s, changelog = result_queue.get()
                ui.startingerror(idx, ver, currentversion, changelog, name, status)
                if idx == 1:
                    ui.mainmenu(n, s, currentversion)

            after_id = ui.app.after(0, startmainmenu)

        threading.Thread(target=startcheck).start()

        ui.run()

    main()


except Exception as e:
    error_message = traceback.format_exc()
    logging.error("[!] Произошла ошибка! %s", error_message)