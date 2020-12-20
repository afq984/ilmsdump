from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QLineEdit, QPushButton, QLabel, QTextEdit, QTextBrowser
from PySide2.QtCore import QFile, QObject, Signal, QThread, Slot, QCoreApplication, Qt
import sys
import ilmsdump
import asyncio
import threading
from datetime import datetime

courses = []
target_path = '.'

def addTextBrowser(text_browser, text):
    text_browser.setText(text_browser.toPlainText() + text)

async def get_enrolled_courses(client, log):
    global courses
    tmp_courses = []
    try:
        await [tmp_courses.append(i) async for i in client.get_enrolled_courses()]
    except:
        pass
    courses = tmp_courses
    for i in tmp_courses:
        log(i.name + '\n')
    log('\n == finish == \n\n')

class Form(QObject):

    def __init__(self, ui_file, parent=None):
        self.loop = asyncio.get_event_loop()

        # load ui file
        super(Form, self).__init__(parent)
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

        self.client = ilmsdump.Client(target_path)
        self.window.show()

    def test_login(self):
        self.client = ilmsdump.Client(target_path)
        account = self.account.text()
        password = self.password.text()
        try:
            self.loop.run_until_complete(self.client.login_with_username_and_password(account, password))
            self.log('login success\n')
            return True
        except s:
            self.log('login fail\n')
            return False

    def show_enrolled(self):
        self.log('== showing the enrolled courses == \n')
        try:
            if not self.test_login(): return
            self.loop.run_until_complete( get_enrolled_courses(self.client, self.log) )
        except:
            pass

    def log(self, text):
        addTextBrowser(self.logBrowser, text)
        self.logBrowser.verticalScrollBar().setValue( self.logBrowser.verticalScrollBar().maximum() )

    def download(self):
        self.show_enrolled()
        self.log(f"download is starting... {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        self.logBrowser.repaint()
        d = ilmsdump.Downloader(client=self.client)
        print(courses)
        self.loop.run_until_complete( d.run(list(courses), []) )
        self.log(f"download finished. {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

if __name__ == "__main__":
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)
    form = Form("ilmsdump.ui")
    sys.exit(app.exec_())

