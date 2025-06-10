currentversion = "0.91"
LinkID = "1djfC1Uyz8hhDJBTC4_NA6oPCxEXG0PEr"

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
            index, version, name, ID, status, changelog = CheckSub(serial, currentversion)
            result_queue.put((index, version, name, ID, status, changelog))

            def startmainmenu():
                idx, ver, n, ID, s, changelog = result_queue.get()
                ui.startingerror(idx, ver, ID, currentversion, LinkID, changelog)
                if idx == 1:
                    ui.mainmenu(n, s, currentversion)

            after_id = ui.app.after(0, startmainmenu)

        threading.Thread(target=startcheck).start()

        ui.run()

    main()


except Exception as e:
    error_message = traceback.format_exc()
    logging.error("[!] Произошла ошибка! %s", error_message)