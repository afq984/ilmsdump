import asyncio
import sys
from datetime import datetime

from PySide6.QtCore import QCoreApplication, QFile, QObject, Qt, QThread
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QLineEdit, QPushButton, QTextBrowser

import ilmsdump

target_path = '.'


def add_2_text_browser(text_browser, text):
    text_browser.setText(text_browser.toPlainText() + text)


def now():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


async def get_enrolled_courses(client, log):
    courses = []
    try:
        courses = [course async for course in ilmsdump.foreach_course(client, ['enrolled'])]
    except TypeError:
        pass
    for i in courses:
        log(i.name + '\n')
    log('\n == finish == \n\n')
    return courses


class DownloadThread(QThread):
    # TODO: make it run properly
    def __init__(self):
        QThread.__init__(self)
        self.log = None
        self.courses = None
        self.downloader = None

    def set(self, log, courses, downloader):
        self.log = log
        self.courses = courses
        self.downloader = downloader

    def run(self):
        self.log(f"download is starting... {now()}\n")
        self.downloader.run(self.courses, [])
        self.log(f"download finished. {now()}\n")


class Form(QObject):
    def __init__(self, ui_file, parent=None):
        # load ui file
        super().__init__(parent)
        ui_file = QFile(ui_file)
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.window = loader.load(ui_file)
        ui_file.close()

        # bind widget
        self.logBrowser = self.window.findChild(QTextBrowser, "log")
        self.account = self.window.findChild(QLineEdit, "account")
        self.password = self.window.findChild(QLineEdit, "password")
        self.test_login_btn = self.window.findChild(QPushButton, "testLoginBtn")
        self.show_enrolled_btn = self.window.findChild(QPushButton, "showEnrolledBtn")
        self.download_btn = self.window.findChild(QPushButton, "downloadBtn")

        # connect
        self.test_login_btn.clicked.connect(self.test_login)
        self.show_enrolled_btn.clicked.connect(self.show_enrolled)
        self.download_btn.clicked.connect(self.download)

        self.loop = asyncio.get_event_loop()
        self.client = ilmsdump.Client(target_path)
        self.download_thread = DownloadThread()
        self.window.show()

    def test_login(self):
        self.client = ilmsdump.Client(target_path)
        account = self.account.text()
        password = self.password.text()
        try:
            self.loop.run_until_complete(
                self.client.login_with_username_and_password(account, password)
            )
            self.log('login success\n')
            return True
        except ilmsdump.LoginFailed:
            self.log('login fail\n')
            return False

    def show_enrolled(self):
        self.log('== showing the enrolled courses == \n')
        if not self.test_login():
            return
        self.courses = self.loop.run_until_complete(get_enrolled_courses(self.client, self.log))

    def log(self, text):
        add_2_text_browser(self.logBrowser, text)
        self.logBrowser.verticalScrollBar().setValue(self.logBrowser.verticalScrollBar().maximum())

    def download(self):
        self.show_enrolled()
        self.logBrowser.repaint()
        d = ilmsdump.Downloader(client=self.client)
        self.log(f"download is starting... {now()}\n")
        self.loop.run_until_complete(d.run(self.courses, []))
        self.log(f"download finished. {now()}\n")
        # TODO: make it run without the following error:
        #   Cannot create children for a parent that is in a different thread
        # self.download_thread.set(self.log, self.courses, d)
        # self.download_thread.start()


if __name__ == "__main__":
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)
    form = Form("ilmsdump.ui")
    sys.exit(app.exec_())
