# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (QLabel, QTextBrowser, QTextEdit, QPushButton,
                             QWidget, QApplication, QDialog, QDesktopWidget,
                             QMessageBox)
from scrapy import Selector
import webbrowser
import pymysql
import chardet
import re


class Ui_Dialog(QWidget):

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        # 窗口大小
        # Dialog.resize(1050, 930)
        Dialog.setFixedSize(1150, 920)
        # 窗口名称
        Dialog.setWindowTitle("IP Scrap Tool")
        # 窗口图标
        Dialog.setWindowIcon(QtGui.QIcon('Data/Icon/icon_spider.png'))
        # 窗口居中
        self.windowCenter()
        # 字体
        font = QtGui.QFont()
        font.setFamily('Fira code')
        # 数据库连接配置
        self.DB_CONFIG = {
            'host': 'localhost',
            'port': 3306,
            'user': 'root',
            'password': 'root',
            'charset': 'utf8mb4',
            'cursorclass': pymysql.cursors.DictCursor
        }
        self.DB_NAME = 'ippool'
        self.targetUrl = 'https://www.xicidaili.com'

        # 结果显示框布局参数
        self.resBrowX = 550
        self.resBrowY = 240
        self.resBrowHeigh = 570
        self.resBrowWidth = 590

        self.statusLabY = 30
        self.statusLabHeigh = 30
        self.statusLabWidth = 120
        self.statusLabX = \
            self.resBrowX + self.resBrowWidth / 2 - self.statusLabWidth / 2

        self.staTxtBrowY = 70
        self.staTxtBrowHeigh = 110
        self.staTxtBrowWidth = 300
        self.staTxtBrowX = self.resBrowX + \
            self.resBrowWidth / 2 - self.staTxtBrowWidth / 2

        self.resLabY = 200
        self.resLabHeigh = 30
        self.resLabWidth = 122
        self.resLabX = \
            self.resBrowX + self.resBrowWidth / 2 - self.resLabWidth / 2

        # HTML文本框
        self.htmlLabel = QLabel(Dialog)
        self.htmlLabel.setGeometry(QtCore.QRect(185, 30, 150, 30))
        self.htmlLabel.setObjectName("htmlLabel")
        self.htmlLabel.setText("HTML文本框")
        self.htmlLabel.setStyleSheet('''
            QLabel#htmlLabel{
                background: #C35;
                padding: 28px;
                color: #FFF;
                font: 900 黑体;
                font-size: 14px;
                }
            ''')
        # ’浏览器‘按钮
        self.browserButton = QPushButton(Dialog)
        self.browserButton.setGeometry(QtCore.QRect(350, 30, 32, 32))
        self.browserButton.setObjectName("browserButton")
        self.browserButton.setFlat(1)
        self.browserButton.setToolTip('打开浏览器')
        self.browserButton.setIcon(QtGui.QIcon('Data/Icon/browser.png'))
        self.browserButton.setIconSize(QtCore.QSize(32, 32))
        self.browserButton.setStyleSheet('''
            QpushButton#browserButton{
                background: transparent;
                boder-radius: 16px;
            }
            ''')
        self.browserButton.clicked.connect(self.openBrowser)

        self.htmlTextEdit = QTextEdit(Dialog)
        self.htmlTextEdit.setFont(font)
        self.htmlTextEdit.setGeometry(QtCore.QRect(30, 70, 490, 760))
        self.htmlTextEdit.setMouseTracking(True)
        self.htmlTextEdit.setObjectName("htmlTextEdit")
        self.htmlTextEdit.setPlaceholderText("输入原始HTML文本")
        self.htmlTextEdit.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOn)
        self.htmlTextEdit.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOn)
        with open("Data/ScrollBar.qss", "rb") as fp:
            content = fp.read()
            encoding = chardet.detect(content) or {}
            content = content.decode(encoding.get("encoding") or "utf-8")
        # self.htmlTextEdit.setText(content)
        self.htmlTextEdit.setStyleSheet(content)

        # ‘抓取’按钮
        self.scrapButton = QPushButton(Dialog)
        self.scrapButton.setGeometry(QtCore.QRect(
            self.resBrowX, self.staTxtBrowY, 50, 42))
        self.scrapButton.setObjectName("scrapButton")
        self.scrapButton.setText("爬取")
        self.scrapButton.setIcon(
            QtGui.QIcon(QtGui.QPixmap("Data/Icon/extract.png")))
        self.scrapButton.clicked.connect(self.scrapEvent)
        self.scrapButton.setStyleSheet('''
            QPushButton#scrapButton{
                border-style: outset;
                border-width: 2px;
                border-radius: 10px;
                border-color: beige;
                font: bold 16px;
                color: #FFF;
                min-width: 5em;
                padding: 6px;
                border-radius: 20px;
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                         stop: 0 #1DB4E1,
                                         stop: 1.0 #428BBC);
            }
            QPushButton#scrapButton:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                         stop: 0 #34C,
                                         stop: 1.0 #A0ADDF);
            }
            QPushButton#scrapButton:pressed {
                background-color: #2B0DF1;
                border-style: inset;
            }
                ''')

        # ‘清空’按钮
        self.cleanButton = QPushButton(Dialog)
        self.cleanButton.setGeometry(QtCore.QRect(
            self.resBrowX, self.staTxtBrowY + self.staTxtBrowHeigh - 42,
            50, 42))
        self.cleanButton.setObjectName("cleanButton")
        self.cleanButton.setText("清空")
        self.cleanButton.setIcon(
            QtGui.QIcon(QtGui.QPixmap("Data/Icon/clean_text.png")))
        self.cleanButton.clicked.connect(self.cleanEvent)
        self.cleanButton.setStyleSheet('''
            QPushButton#cleanButton{
            border-style: outset;
            border-width: 2px;
            border-radius: 10px;
            border-color: beige;
            font: bold 16px;
            color: #FFF;
            min-width: 5em;
            padding: 6px;
            border-radius: 20px;
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                         stop: 0 #1DB4E1,
                                         stop: 1.0 #428BBC);
            }
            QPushButton#cleanButton:hover{
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                             stop: 1.0 #428BBC,
                                             stop: 0 #465EFB);
            }
            QPushButton#cleanButton:pressed {
                background-color: #00F;
                border-style: inset;
            }
        ''')

        # 状态显示框

        self.statusLabel = QLabel(Dialog)
        self.statusLabel.setGeometry(QtCore.QRect(self.statusLabX,
                                                  self.statusLabY,
                                                  self.statusLabWidth,
                                                  self.statusLabHeigh))
        self.statusLabel.setObjectName("statusLabel")
        self.statusLabel.setText("状态显示")
        self.statusLabel.setStyleSheet('''
            QLabel#statusLabel{
            background:#C35;
            padding: 28px;
            color:#FFF;
            font: 900 黑体;
            font-size: 14px;
            }
            ''')

        self.statusTextBrowser = QTextBrowser(Dialog)
        self.statusTextBrowser.setFont(font)
        self.statusTextBrowser.setGeometry(QtCore.QRect(self.staTxtBrowX,
                                                        self.staTxtBrowY,
                                                        self.staTxtBrowWidth,
                                                        self.staTxtBrowHeigh
                                                        ))
        self.statusTextBrowser.setObjectName("statusTextBrowser")
        self.statusTextBrowser.setText('')

        # 数据库查询结果文本显示框

        self.resultLabel = QLabel(Dialog)
        self.resultLabel.setGeometry(QtCore.QRect(self.resLabX,
                                                  self.resLabY,
                                                  self.resLabWidth,
                                                  self.resLabHeigh))
        # self.resultLabel.setGeometry(QtCore.QRect(724, 200, 150, 30))
        self.resultLabel.setObjectName("resultLabel")
        self.resultLabel.setText("数据显示")
        self.resultLabel.setStyleSheet('''QLabel#resultLabel{
                background:#C35;
                padding: 28px;
                color: #FFF;
                font: 900 黑体;
                font-size: 14px;}
            ''')
        self.resTextBrowser = QTextBrowser(Dialog)
        self.resTextBrowser.setFont(font)
        self.resTextBrowser.setGeometry(QtCore.QRect(self.resBrowX,
                                                     self.resBrowY,
                                                     self.resBrowHeigh,
                                                     self.resBrowWidth))
        self.resTextBrowser.setObjectName("resTextBrowser")
        self.resTextBrowser.setPlaceholderText('数据显示')
        self.resTextBrowser.setText('')
        self.resTextBrowser.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOn)
        self.resTextBrowser.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOn)
        with open("Data/ScrollBar.qss", "rb") as fp:
            content = fp.read()
            encoding = chardet.detect(content) or {}  # 检测编码
            content = content.decode(encoding.get("encoding") or "utf-8")
        # self.htmlTextEdit.setText(content)
        self.resTextBrowser.setStyleSheet(content)

        # ‘查询’按钮
        self.showAllButton = QPushButton(Dialog)
        self.showAllButton.setGeometry(QtCore.QRect(920, 200, 30, 30))
        self.showAllButton.setObjectName("showAllButton")
        self.showAllButton.setToolTip('查询所有数据')
        self.showAllButton.setFlat(1)
        self.showAllButton.setStyleSheet('''
            QpushButton#showAllButton{
            border-radius: 13px;
            }
            ''')
        self.showAllButton.setIcon(QtGui.QIcon('Data/Icon/showAll.png'))
        self.showAllButton.setIconSize(QtCore.QSize(35, 35))
        self.showAllButton.clicked.connect(self.showAllRecords)

        self.checkConnection()
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def windowCenter(self):
        """ 窗口居中 """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):  # 函数名固定不可变
        reply = QMessageBox.question(
            self, u'警告', u'确认退出?',
            QMessageBox.Yes,
            QMessageBox.No)
        # QMessageBox.question(self,u'弹窗名',u'弹窗内容',选项1,选项2)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()  # 关闭窗口
        else:
            event.ignore()  # 忽视点击X事件

    # ‘爬取’按钮点击调用
    @QtCore.pyqtSlot()
    def scrapEvent(self):
        """
        获取HTML文本框中的文本，提取IP信息，保存到数据库
        """
        try:
            pymysql.connect(**self.DB_CONFIG)
            conn = pymysql.connect(**self.DB_CONFIG)
            conn.autocommit(1)
            cursor = conn.cursor()
            # Table_NAME = 'ipinfo'
            IPAddr = ''
            serverAddr = ''
            port = 0
            text = self.htmlTextEdit.toPlainText()
            # print(text, type(text))
            if text:
                # <table id="ip_list">
                htmlCheck = re.match(r'[<table id="ip_list">]', text)
                if htmlCheck:
                    try:
                        conn.select_db(self.DB_NAME)
                        self.statusTextBrowser.setText('[INFO]: 连接数据库')
                        self.statusTextBrowser.setAlignment(
                            QtCore.Qt.AlignCenter)
                        html = Selector(text=text)
                        self.htmlTextEdit.setHtml(text)
                        # self.resTextBrowser.setText(str(html))
                        self.resTextBrowser.setText('')
                        preRecordNum = cursor.execute(
                            'SELECT DISTINCT * FROM IPINFO;')
                        for tr in html.xpath('//tr[@class]'):
                            IPAddr = tr.xpath('td[2]/text()').extract_first()
                            port = int(
                                tr.xpath('td[3]/text()').extract_first())
                            serverAddr = tr.xpath(
                                'td[4]/a/text()').extract_first()
                            cursor.execute("INSERT INTO ipinfo values(%d, %d, "
                                           "'%s'); " % (
                                               self.IPSwapLong(IPAddr),
                                               port,
                                               serverAddr))
                            self.resTextBrowser.append(
                                'IP地址: %15s, 端口: %5d, 服务器地址: %s' %
                                (IPAddr, port, serverAddr))
                        # 查询数据条目
                        recordNum = cursor.execute(
                            'SELECT DISTINCT * FROM IPINFO;')
                        self.statusTextBrowser.setText(' [INFO]: 数据获取成功')
                        self.statusTextBrowser.setAlignment(
                            QtCore.Qt.AlignCenter)
                        self.statusTextBrowser.append(
                            '新插入数据数目：%d条' % (recordNum - preRecordNum))
                        self.statusTextBrowser.setAlignment(
                            QtCore.Qt.AlignCenter)
                        self.statusTextBrowser.append(
                            '数据库数据数目：%d条' % recordNum)
                        self.statusTextBrowser.setAlignment(
                            QtCore.Qt.AlignCenter)

                    except Exception:
                        import traceback
                        traceback.print_exc()
                        conn.rollback()
                        self.statusTextBrowser.append(
                            '✘[EEEOR]: 出现错误，数据库回滚')
                        self.statusTextBrowser.setAlignment(
                            QtCore.Qt.AlignCenter)
                        self.resTextBrowser.setText('')
                    finally:
                        # 关闭游标连接
                        cursor.close()
                        self.statusTextBrowser.append(
                            ' [INFO]: 关闭游标连接')
                        # 关闭数据库连接
                        conn.close()
                        self.statusTextBrowser.append(
                            ' [INFO]: 关闭数据库连接')

                # 文本格式错误
                else:
                    self.statusTextBrowser.setText(
                        '✘[EEEOR]: 文本格式错误')
                    self.statusTextBrowser.setAlignment(QtCore.Qt.AlignCenter)

            # 无内容
            else:
                self.statusTextBrowser.setText(' [WARNING]: 无内容')
                self.statusTextBrowser.setAlignment(QtCore.Qt.AlignCenter)
        except Exception:
            self.statusTextBrowser.setText('')
            self.statusTextBrowser.append(
                '✘[EEEOR]: 由于目标计算机积极拒绝，无法连接')
            self.statusTextBrowser.setAlignment(QtCore.Qt.AlignCenter)
            self.statusTextBrowser.append(
                '[INFO]: 请检查数据库连接状态')
            self.statusTextBrowser.setAlignment(QtCore.Qt.AlignCenter)
        finally:
            pass

    # ‘清空’按钮点击调用
    @QtCore.pyqtSlot()
    def cleanEvent(self):
        """
        清空所有内容
        """
        self.htmlTextEdit.setText('')
        self.statusTextBrowser.setText('')
        self.resTextBrowser.setText('')

    # ‘查询’按钮点击调用
    @QtCore.pyqtSlot()
    def showAllRecords(self):
        """
            获取数据库所有数据
        """
        self.resTextBrowser.setText('')
        try:
            pymysql.connect(**self.DB_CONFIG)
            try:
                conn = pymysql.connect(**self.DB_CONFIG)
                self.statusTextBrowser.append('[INFO]: 连接数据库')
                self.statusTextBrowser.setAlignment(QtCore.Qt.AlignCenter)
                conn.autocommit(1)
                cursor = conn.cursor()
                conn.select_db(self.DB_NAME)
                recordNum = cursor.execute('SELECT DISTINCT * FROM IPINFO;')
                self.statusTextBrowser.append('数据库数据数目：%d条' % recordNum)
                self.statusTextBrowser.setAlignment(QtCore.Qt.AlignCenter)

                table_records = cursor.fetchall()
                for each_record in table_records:
                    res = 'IP地址: %15s, 端口: %5d, 服务器地址: %s' % (
                        self.IPSwapLong(each_record['IP地址']),
                        each_record['端口'],
                        each_record['服务器地址'])
                    self.resTextBrowser.append(res)
                self.statusTextBrowser.append('[INFO]: 查询成功')
                self.statusTextBrowser.setAlignment(QtCore.Qt.AlignCenter)
            except Exception:
                import traceback
                traceback.print_exc()
                conn.rollback()
                self.statusTextBrowser.append(
                    '✘[EEEOR]: 出现错误，数据库回滚')
                self.statusTextBrowser.setAlignment(QtCore.Qt.AlignCenter)
                self.resTextBrowser.setText('')
            finally:
                # 关闭游标连接
                cursor.close()
                self.statusTextBrowser.append(
                    ' [INFO]: 关闭游标连接')
                self.statusTextBrowser.setAlignment(QtCore.Qt.AlignCenter)
                # 关闭数据库连接
                conn.close()
                self.statusTextBrowser.append(
                    ' [INFO]: 关闭数据库连接')
                self.statusTextBrowser.setAlignment(QtCore.Qt.AlignCenter)
        except Exception:
            self.statusTextBrowser.setTextColor('#FF0000')
            self.statusTextBrowser.append(
                '✘[EEEOR]: 由于目标计算机积极拒绝，无法连接')
            self.statusTextBrowser.setAlignment(QtCore.Qt.AlignCenter)
            self.statusTextBrowser.append(
                '[INFO]: 请检查数据库连接状态')
            self.statusTextBrowser.setAlignment(QtCore.Qt.AlignCenter)
        finally:
            pass

    # ‘浏览器’按钮点击调用
    @QtCore.pyqtSlot()
    def openBrowser(self):
        """
            打开浏览器
        """
        webbrowser.open(self.targetUrl)

    def checkConnection(self):
        """
        检查数据库是否连接
        """
        try:
            pymysql.connect(**self.DB_CONFIG)
        except Exception as err:
            self.statusTextBrowser.append(
                '✘[EEEOR]: 由于目标计算机积极拒绝，无法连接')
            self.statusTextBrowser.setAlignment(QtCore.Qt.AlignCenter)
            self.statusTextBrowser.append(
                '[INFO]: 请检查数据库连接状态')
            self.statusTextBrowser.setAlignment(QtCore.Qt.AlignCenter)
        finally:
            pass

    def IPSwapLong(self, IPorLong):
        """
        IP地址和长整型数转换
        参数 IPorLong (str) ='255.255.255.255' 返回值 (int): 4294967295
        参数 IPorLong (int) = 1873914904       返回值 (str): 111.177.172.24
        """
        if isinstance(IPorLong, str):
            res = re.findall(r'[\d]+', IPorLong)
            longRes = (int(res[0]) << 24) + (int(res[1]) << 16) + \
                (int(res[2]) << 8) + int(res[3])
            return longRes
        else:
            IPRes = str(IPorLong >> 24) + '.' + str((IPorLong >> 16) & 255) + \
                '.' + str((IPorLong >> 8) & 255) + '.' + str(IPorLong & 255)
            return IPRes


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    Dialog = QDialog()
    gui = Ui_Dialog()
    gui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
