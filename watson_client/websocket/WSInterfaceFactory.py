# coding=utf-8
import threading  # multi threading

try:
    from Queue import Queue # queue used for thread syncronization
except:
    from queue import Queue 
     
# WebSockets
from autobahn.twisted.websocket import WebSocketClientFactory
from watson_client.websocket.WSInterfaceProtocol import WSInterfaceProtocol
from twisted.internet import ssl, reactor


class WSInterfaceFactory(WebSocketClientFactory):
    def __init__(self, audioFd, summary, contentType, model, url=None, headers=None, debug=None):
        self.listeners = []
        WebSocketClientFactory.__init__(self, url=url, headers=headers)
        self.audioFd = audioFd
        self.summary = summary
        self.contentType = contentType
        self.model = model

        self.openHandshakeTimeout = 6
        self.closeHandshakeTimeout = 6

    def setListeners(self, listeners):
        self.listeners = listeners

    def getListeners(self):
        return self.listeners

    def prepareUtterance(self):
        return False

    def endReactor(self):
        print("about to stop the reactor!")
        reactor.stop()

    # this function gets called every time connectWS is called (once per WebSocket connection/session)
    def buildProtocol(self, addr):
        print('Build protocol')
        proto = WSInterfaceProtocol(self, self.audioFd, self.summary, self.contentType)
        proto.setListeners(self.listeners)
        proto.setUtterance()
        return proto
