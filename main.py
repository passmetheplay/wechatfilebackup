import sys
from PyQt5.QtWidgets import QApplication
from main_window_ui import MainWindowUI
from event_handlers import EventHandlers
from utilities import Utilities

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window_ui = MainWindowUI()
    event_handlers = EventHandlers(main_window_ui)
    utilities = Utilities()  # 如果需要的话
    main_window_ui.show()  # 显示窗口


    sys.exit(app.exec_())
