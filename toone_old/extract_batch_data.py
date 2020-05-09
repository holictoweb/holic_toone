#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import logging
from logging.handlers import TimedRotatingFileHandler
from PyQt5.QAxContainer import QAxWidget
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QApplication



class SysTrader(QObject):
    def __init__():
        """자동투자시스템 메인 클래스 start
        """
        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.kiwoom.OnEventConnect.connect(self.kiwoom_OnEventConnect)  # 로그인 결과를 받을 콜백함수 연결
