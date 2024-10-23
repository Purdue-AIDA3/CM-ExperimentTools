import sys
from PyQt6.QtCore import QUrl, pyqtSignal, QObject, QFile, QIODevice, pyqtSlot
from PyQt6.QtWebChannel import QWebChannel
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineScript, QWebEnginePage
from PyQt6.QtWidgets import QApplication
from PyQt6.QtNetwork import QNetworkCookie
from datetime import datetime

import time

class ClickHandler(QObject):

    elementClicked = pyqtSignal(str, float, float)

    @pyqtSlot(str, float, float)
    def handleElementClicked(self, text, x, y):
        self.elementClicked.emit(text, x, y)


class Task2WebEngineView(QWebEngineView):
    elementClicked = pyqtSignal(str, float, float)
    def __init__(self, parent=None):
        super().__init__(parent)
        load_web_channel_js = QWebEngineScript()
        load_web_channel_js.setInjectionPoint(QWebEngineScript.InjectionPoint.DocumentCreation)
        load_web_channel_js.setWorldId(QWebEngineScript.ScriptWorldId.MainWorld)
        load_web_channel_js.setName("qwebchannel.js")
        load_web_channel_js.setRunsOnSubFrames(True)
        load_web_channel_js_file = QFile(":/qtwebchannel/qwebchannel.js")
        load_web_channel_js_file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text)
        load_web_channel_js.setSourceCode(str(load_web_channel_js_file.readAll(), 'utf-8'))
        self.page().scripts().insert(load_web_channel_js)

        click_handler_js = QWebEngineScript()
        click_handler_js.setInjectionPoint(QWebEngineScript.InjectionPoint.DocumentCreation)
        click_handler_js.setWorldId(QWebEngineScript.ScriptWorldId.MainWorld)
        click_handler_js.setName("click_handler.js")
        click_handler_js.setRunsOnSubFrames(True)
        click_handler_js.setSourceCode(
            """
            var click_handler
            var webChannel = new QWebChannel(qt.webChannelTransport, function(channel) {
                click_handler = channel.objects.click_handler;
            });
            window.addEventListener("click", function(event) {
                if (event.target.tagName == "CANVAS")
                    click_handler.handleElementClicked("Map", event.clientX  , event.clientY)
                else
                    click_handler.handleElementClicked(event.target.innerText, event.clientX  , event.clientY)
            });
            """
        )
        self.page().scripts().insert(click_handler_js)
        self.channel = QWebChannel()
        self.click_handler = ClickHandler()
        self.channel.registerObject("click_handler", self.click_handler)
        self.page().setWebChannel(self.channel)
        self.click_handler.elementClicked.connect(self.handleElementClicked)
        cookie_store = self.page().profile().cookieStore()
        qcookie = QNetworkCookie()
        qcookie.setName(".DA-CC-Identity".encode())
        with open("Resources\cookie") as f:
            cookie = f.readline()
        qcookie.setValue(cookie.encode())
        qcookie.setDomain("cloud.distributed-avionics.com")
        qcookie.setPath("/")
        expiration_date = datetime.now()
        expiration_date = expiration_date.replace(year = expiration_date.year + 1)
        qcookie.setExpirationDate(expiration_date)
        qcookie.setHttpOnly(True)
        qcookie.setSecure(False)
        cookie_store.setCookie(qcookie, QUrl())


    @pyqtSlot(str, float, float)
    def handleElementClicked(self, text, x, y):
        self.elementClicked.emit(text, x, y)