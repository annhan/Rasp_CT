# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Wed Jul 30 21:49:42 2014
#      by: PyQt4 UI code generator 4.11.1
#
# WARNING! All changes made in this file will be lost!

import serial,time
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4 import QtNetwork
import RPi.GPIO as GPIO
import threading
import math
import os
import array
import socket
from random import randint
mauR=""
mauG=""
mauB=""
mauRoff=""
mauGoff=""
mauBoff=""
tocdoon=10
tocdooff=10
CBD=100
CBT=150
bientruyen=0
sobat=24
sobatlonnhat=sobat+1
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)
class Server(QtCore.QThread):
    def __init__(self):
        super(Server, self).__init__()
    def run(self):
        global mauR,mauG,mauB,mauBoff,mauRoff,mauGoff,tocdoon,tocdooff
        s = socket.socket()
        host = socket.gethostname()
        print(host)
        port = 10001
        s.bind(("0.0.0.0",port))
        s.listen(5)
        while True:
            c,addr = s.accept()
            print(addr)
            try:
                dulieu=bytes.decode(c.recv(1024))
            except:
                print("co loi")
            if "CBTREN" in dulieu:
                self.emit(QtCore.SIGNAL("Server1(QString)"),"aaa")
            if "CBDUOI" in dulieu:
                self.emit(QtCore.SIGNAL("Server(QString)"),"aaa")
            try:
                if "Mau" in dulieu:
                    vitri=dulieu.find("Mau")
                    vitri=vitri+3
                    vitri1=dulieu.find(",",vitri)
                    mauR=str(dulieu[vitri:vitri1])
                    vitri2=dulieu.find(",",vitri1+1)
                    bien=dulieu[vitri1+1:vitri2]
                    mauG=str(bien)
                    vitri3=dulieu.find(",",vitri2+1)
                    mauB=str(dulieu[vitri2+1:vitri3])
                    print(mauR)
                    print(mauG)
                    print(mauB)
                    f = open('luubien.txt','w+')
                    f.write("Ron:"+str(mauR)+" Gon:" + str(mauG)+" Bon:" + str(mauB)+" end\r\n")
                    f.write("Roff:"+str(mauRoff)+" Goff:" + str(mauGoff)+" Boff:" + str(mauBoff)+" end\r\n")
                    f.write("SpeedON:"+str(tocdoon)+" SpeedOFF:" + str(tocdooff)+" end\r\n")
                    f.close()
            except:
                print("loi internet")
            c.send(b'Ket noi thanh cong ct!')
            c.close()
class docmau(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)
    def run(self):
        global mauR,mauG,mauB,mauBoff,mauRoff,mauGoff,tocdoon,tocdooff,sobat
        mau42=array.array('B',[10]).tostring()
        rs232.write(mau42)
        print(mau42)
        f = open('luubien.txt','r')
        noidung=f.read()
        try:
            if "Gon" in noidung:
                vitri=noidung.find("Gon")
                vitri=vitri+4
                vitri1=noidung.find(" ",vitri)
                mauG=str(noidung[vitri:vitri1])
                print(mauG)

        except:
            mauG=255
        try:
            if "Ron" in noidung:
                vitri=noidung.find("Ron")
                vitri=vitri+4
                vitri1=noidung.find(" ",vitri)
                mauR=str(noidung[vitri:vitri1])
                print(mauR)
        except:
            mauR=0
        try:
            if "Bon" in noidung:
                vitri=noidung.find("Bon")
                vitri=vitri+4
                vitri1=noidung.find(" end",vitri)
                bien=noidung[vitri:vitri1]
                mauB=str(bien)
                print(mauB)
        except:
            mauB=0
        try:
            if "Roff" in noidung:
                vitri=noidung.find("Roff")
                vitri=vitri+5
                vitri1=noidung.find(" ",vitri)
                mauRoff=str(noidung[vitri:vitri1])
                print(mauRoff)
        except:
            mauRoff=0
        try:
            if "Goff" in noidung:
                vitri=noidung.find("Goff")
                vitri=vitri+5
                vitri1=noidung.find(" ",vitri)
                mauGoff=str(noidung[vitri:vitri1])
                print("mau5")
                print(mauGoff)
        except:
            mauGoff=0
        try:
            if "Boff" in noidung:
                vitri=noidung.find("Boff")
                vitri=vitri+5
                vitri1=noidung.find(" end",vitri)
                mauBoff=str(noidung[vitri:vitri1])
                print("mau6")
                print(mauBoff)
        except:
            mauBoff=0
        try:
            if "SpeedON" in noidung:
                vitri=noidung.find("SpeedON")
                vitri=vitri+8
                vitri1=noidung.find(" ",vitri)
                tocdoon=int(noidung[vitri:vitri1])
                print("mau7")
                print(tocdoon)
        except:
            tocdoon=3
        try:
            if "SpeedOFF" in noidung:
                vitri=noidung.find("SpeedOFF")
                vitri=vitri+9
                vitri1=noidung.find(" end",vitri)
                tocdooff=int(noidung[vitri:vitri1])
                print(tocdooff)
        except:
            tocdooff=10
        return

class senddkCBT(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)
    def run(self):
        global CBT,CBD,sobat,sobatlonnhat
        global mauR,mauG,mauB,mauBoff,mauRoff,mauGoff,tocdoon,tocdooff
        diachilonnhat=14
        max=diachilonnhat+1
        diachi=100
        diachi1=90
        diachitat=50
        bien=0
        bien1=0
        sang=3
        dem=5
        trangthaisang=0
        mau1t=0
        mau2t=0
        mau3t=0
        thoat=0
        while True:

            if CBD==1:
                if bien==1:
                    print("dang sang")
                    CBD=0
                else:
                    diachi=100
                    bien=1
                    CBD=0
                    dem=1
                    sang=0
                    if bien1==2:
                        diachi1=90
                        diachitat=50
                        bien1=3
            if CBT==1:
                if bien1==1:
                    print("dang sang 1")
                    CBT=0
                else:
                    diachi1=90
                    bien1=1
                    CBT=0
                    dem=2
                    sang=0
                    if bien==2:
                        diachi=100
                        diachitat=50
                        bien=3
            if bien==1:
                if diachi==100:
                    diachi=0
                else:
                    diachi=diachi+1
                    if diachi==sobatlonnhat:#lon hon gia tri 1 bat
                        print("lon nhat")
                        diachi=diachi+1
                        bien=2
                        sang=1
                        trangthaisang=1
                        time.sleep(5)#thoi gian nghi
            elif bien==2:#tat dan
                diachi=diachi-1
                diachitat=diachi-1
                if diachi==0:
                    trangthaisang=0
                    bien=0
                    sang=3
                    diachi=100
                    diachi1=90
            if bien1==1:
                if diachi1==90:
                    diachi1phu=sobatlonnhat #lon hon gia tri bat
                    diachi1=sobat
                else:
                    diachi1phu=diachi1phu-1
                    diachi1=diachi1phu-1
                    if diachi1phu==0:
                        print("nho nhat")
                        bien1=2
                        tat=1
                        sang=1
                        trangthaisang=1
                        time.sleep(5)#thoi gian nghi
            elif bien1==2:
                diachitat=diachi1phu
                diachi1phu=diachi1phu+1
                if diachitat==sobatlonnhat:
                    trangthaisang=0
                    print("nho nhat 1")
                    diachi1=90
                    diachi=100
                    bien1=0
                    sang=3
            if bien==1 and bien1==1:
                if diachi>diachi1:
                    if dem==1:
                        print("da  gap ")
                        bien1=3
                        diachi1=90
                    elif dem==2:
                        print("da  gap 1")
                        bien=3
                        diachi=100
            if sang==0:
                print("sang")
                print(diachi)
                mau1t=0
                mau2t=0
                mau3t=0
                thoat=0
                if trangthaisang==0:
                    while thoat==0:
                        if CBT==1 or CBD==1:
                            thoat=1
                        if mau1t>=(int(mauG)-15):
                            mau1t=int(mauG)
                        else:
                            mau1t=mau1t+15
                        if mau2t>=(int(mauR)-15):
                            mau2t=int(mauR)
                        else:
                            mau2t=mau2t+15
                        if mau3t>=(int(mauB)-15):
                            mau3t=int(mauB)
                        else:
                            mau3t=mau3t+15
                        print(mau1t)
                        print(mau2t)
                        print(mau3t)
                        dulieu(diachi,str(mau1t),str(mau2t),str(mau3t),"0")
                        dulieu(diachi1,str(mau1t),str(mau2t),str(mau3t),"0")
                        rs232.write(b'\xfe')
                        rs232.write(b'\xff')
                        rs232.write(b'\x01')
                        rs232.write(b'\x00')
                        rs232.write(b'\x01')
                        rs232.write(b'\x00')
                        rs232.write(b'\x01')
                        if mau1t==int(mauG) and mau2t==int(mauR) and mau3t==int(mauB):
                            thoat=1
                        time.sleep(0.01)
                elif trangthaisang==1:
                    dulieu(diachi,mauG,mauR,mauB,"0")
                    dulieu(diachi1,mauG,mauR,mauB,"0")
                    rs232.write(b'\xfe')
                    rs232.write(b'\xff')
                    rs232.write(b'\x01')
                    rs232.write(b'\x00')
                    rs232.write(b'\x01')
                    rs232.write(b'\x00')
                    rs232.write(b'\x01')
                    time.sleep(0.3)
                time.sleep(0.15)
            elif sang==1:
                thoat=0
                mau1t=int(mauG)
                mau2t=int(mauR)
                mau3t=int(mauB)
                while thoat==0:
                    if CBT==1 or CBD==1:
                        thoat=1
                    if mau1t<=10:
                        mau1t=0
                    else:
                        mau1t=mau1t-10
                    if mau2t<=10:
                        mau2t=0
                    else:
                        mau2t=mau2t-10
                    if mau3t<=10:
                        mau3t=0
                    else:
                        mau3t=mau3t-10
                    print(mau1t)
                    print(mau2t)
                    print(mau3t)
                    dulieu(diachitat,str(mau1t),str(mau2t),str(mau3t),"0")
                    rs232.write(b'\xfe')
                    rs232.write(b'\xff')
                    rs232.write(b'\x01')
                    rs232.write(b'\x00')
                    rs232.write(b'\x01')
                    rs232.write(b'\x00')
                    rs232.write(b'\x01')
                    if mau1t==0 and mau2t==0 and mau3t==0:
                        thoat=1
                    time.sleep(0.01)
                tocdo=0
                tocdooff1=int(tocdooff)
                while tocdo<tocdooff1:
                    tocdo=tocdo+1
                    time.sleep(0.01)
            elif sang==3:
		sang=4
                dulieu("255","0","0","0","0")
                rs232.write(b'\xfe')
                rs232.write(b'\xff')
                rs232.write(b'\x01')
                rs232.write(b'\x00')
                rs232.write(b'\x01')
                rs232.write(b'\x00')
                rs232.write(b'\x01')
                time.sleep(0.02)
	    else:
		time.sleep(0.02)
def dulieu(thutu,mau1,mau2,mau3,mau4):
    try:
        thutu=str(thutu)
        mau1=str(mau1)
        mau2=str(mau2)
        mau3=str(mau3)
        mau4=str(mau4)
        thutu1=int(thutu)
        mau11=int(mau1)
        mau21=int(mau2)
        mau31=int(mau3)
        mau41=int(mau4)
        rs232.write(b'\xff')
        #time.sleep(0.01)
        matt1=array.array('B',[thutu1]).tostring()
        mau12=array.array('B',[mau11]).tostring()
        mau22=array.array('B',[mau21]).tostring()
        mau32=array.array('B',[mau31]).tostring()
        mau42=array.array('B',[mau41]).tostring()
        rs232.write(matt1)
        #time.sleep(0.01)
        rs232.write(mau12)
        #time.sleep(0.01)
        rs232.write(mau22)
        #time.sleep(0.01)
        rs232.write(mau32)
        #time.sleep(0.01)
        rs232.write(mau42)
        #time.sleep(0.01)
        macheck1=checksum(255,thutu1,mau11,mau21,mau31,mau41)
        macheck1=int(macheck1)
        checksum1=array.array('B',[macheck1]).tostring()
        rs232.write(checksum1)
    except:
        print("co loi roi oooooo")
def checksum(lenh,diachi,mau1,mau2,mau3,mau4):
    try:
        tong=lenh+diachi+mau1+mau2+mau3+mau4
        tong=tong%256
        tong=256-tong
        if tong==256:
            tong=0
        return tong
    except:
        print("loi")
class Ui_MainWindow(QtGui.QWidget):

    def setupUi(self, MainWindow):
        global mauR,mauG,mauB,bientruyen
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        self.giatriBon='255'
        self.giatriGon='255'
        self.giatriRon='255'
        self.giatriBoff='0'
        self.giatriGoff='0'
        self.giatriRoff='0'

        #self.connect(self.thrad2,QtCore.SIGNAL("FROMSIM(QString,QString,QString,QString,QString)"),self.dulieu)
        #self.connect(self.thrad3,QtCore.SIGNAL("FROMSIM1(QString,QString,QString,QString,QString)"),self.dulieu)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.layoutWidget = QtGui.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(18, 40, 351, 121))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.gridLayout_4 = QtGui.QGridLayout(self.layoutWidget)
        self.gridLayout_4.setMargin(0)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(self.layoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)
        self.Updata_coloron = QtGui.QPushButton(self.layoutWidget)
        self.Updata_coloron.setObjectName(_fromUtf8("Updata_coloron"))
        self.gridLayout.addWidget(self.Updata_coloron, 4, 1, 1, 1)
        self.Bon = QtGui.QSlider(self.layoutWidget)
        self.Bon.setOrientation(QtCore.Qt.Horizontal)
        self.Bon.setObjectName(_fromUtf8("Bon"))
        self.gridLayout.addWidget(self.Bon, 3, 1, 1, 1)
        self.label_4 = QtGui.QLabel(self.layoutWidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.Gon = QtGui.QSlider(self.layoutWidget)
        self.Gon.setOrientation(QtCore.Qt.Horizontal)
        self.Gon.setObjectName(_fromUtf8("Gon"))
        self.gridLayout.addWidget(self.Gon, 2, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.layoutWidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.layoutWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.Ron = QtGui.QSlider(self.layoutWidget)
        self.Ron.setOrientation(QtCore.Qt.Horizontal)
        self.Ron.setObjectName(_fromUtf8("Ron"))
        self.gridLayout.addWidget(self.Ron, 1, 1, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label_5 = QtGui.QLabel(self.layoutWidget)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_2.addWidget(self.label_5, 0, 1, 1, 1)
        self.label_6 = QtGui.QLabel(self.layoutWidget)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout_2.addWidget(self.label_6, 1, 0, 1, 1)
        self.Roff = QtGui.QSlider(self.layoutWidget)
        self.Roff.setOrientation(QtCore.Qt.Horizontal)
        self.Roff.setObjectName(_fromUtf8("Roff"))
        self.gridLayout_2.addWidget(self.Roff, 1, 1, 1, 1)
        self.label_7 = QtGui.QLabel(self.layoutWidget)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout_2.addWidget(self.label_7, 2, 0, 1, 1)
        self.Goff = QtGui.QSlider(self.layoutWidget)
        self.Goff.setOrientation(QtCore.Qt.Horizontal)
        self.Goff.setObjectName(_fromUtf8("Goff"))
        self.gridLayout_2.addWidget(self.Goff, 2, 1, 1, 1)
        self.label_8 = QtGui.QLabel(self.layoutWidget)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout_2.addWidget(self.label_8, 3, 0, 1, 1)
        self.Boff = QtGui.QSlider(self.layoutWidget)
        self.Boff.setOrientation(QtCore.Qt.Horizontal)
        self.Boff.setObjectName(_fromUtf8("Boff"))
        self.gridLayout_2.addWidget(self.Boff, 3, 1, 1, 1)
        self.Updata_coleroff = QtGui.QPushButton(self.layoutWidget)
        self.Updata_coleroff.setObjectName(_fromUtf8("Updata_coleroff"))
        self.gridLayout_2.addWidget(self.Updata_coleroff, 4, 1, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_2, 0, 1, 1, 1)
        self.gridLayout_3 = QtGui.QGridLayout()
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.label_10 = QtGui.QLabel(self.layoutWidget)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout_3.addWidget(self.label_10, 2, 0, 1, 1)
        self.Updata_speed = QtGui.QPushButton(self.layoutWidget)
        self.Updata_speed.setObjectName(_fromUtf8("Updata_speed"))
        self.gridLayout_3.addWidget(self.Updata_speed, 4, 1, 1, 1)
        self.Speed_down = QtGui.QSlider(self.layoutWidget)
        self.Speed_down.setOrientation(QtCore.Qt.Horizontal)
        self.Speed_down.setObjectName(_fromUtf8("Speed_down"))
        self.gridLayout_3.addWidget(self.Speed_down, 3, 1, 1, 1)
        self.label_11 = QtGui.QLabel(self.layoutWidget)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.gridLayout_3.addWidget(self.label_11, 3, 0, 1, 1)
        self.Speed_up = QtGui.QSlider(self.layoutWidget)
        self.Speed_up.setOrientation(QtCore.Qt.Horizontal)
        self.Speed_up.setObjectName(_fromUtf8("Speed_up"))
        self.gridLayout_3.addWidget(self.Speed_up, 2, 1, 1, 1)
        self.label_9 = QtGui.QLabel(self.layoutWidget)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout_3.addWidget(self.label_9, 1, 1, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_3, 0, 2, 1, 1)
        self.CBtren = QtGui.QPushButton(self.centralwidget)
        self.CBtren.setGeometry(QtCore.QRect(40, 180, 75, 23))
        self.CBtren.setObjectName(_fromUtf8("CBtren"))
        self.CBduoi = QtGui.QPushButton(self.centralwidget)
        self.CBduoi.setGeometry(QtCore.QRect(160, 180, 75, 23))
        self.CBduoi.setObjectName(_fromUtf8("CBduoi"))
        self.offall = QtGui.QPushButton(self.centralwidget)
        self.offall.setGeometry(QtCore.QRect(290, 180, 75, 23))
        self.offall.setObjectName(_fromUtf8("offall"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuSetup = QtGui.QMenu(self.menubar)
        self.menuSetup.setObjectName(_fromUtf8("menuSetup"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuSetup.menuAction())
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        #QtCore.QObject.connect(self.Ron, QtCore.SIGNAL('valueChanged(int)'), self.changeText)
        QtCore.QObject.connect(self.Updata_coloron, QtCore.SIGNAL(_fromUtf8("clicked()")),self.Updata_color_on)
        QtCore.QObject.connect(self.Updata_coleroff, QtCore.SIGNAL(_fromUtf8("clicked()")),self.Updata_color_off)
        QtCore.QObject.connect(self.Updata_speed, QtCore.SIGNAL(_fromUtf8("clicked()")),self.Up_speed)
        QtCore.QObject.connect(self.CBduoi, QtCore.SIGNAL(_fromUtf8("clicked()")),self.cambienduoi)
        QtCore.QObject.connect(self.CBtren, QtCore.SIGNAL(_fromUtf8("clicked()")),self.cambientren)
        GPIO.setmode(GPIO.BCM)     # set up BCM GPIO numbering
        GPIO.setup(23, GPIO.IN)
        GPIO.setup(24, GPIO.IN)
        GPIO.add_event_detect(23, GPIO.RISING, callback=self.my_callbacklen)
        GPIO.add_event_detect(24, GPIO.RISING, callback=self.my_callbackxuong)
        self.thrad1=docmau()
        self.thrad1.start()
        self.thrad4=Server()
        self.thrad4.start()
        self.thrad2=senddkCBT()
        self.thrad2.start()
        self.connect(self.thrad4,QtCore.SIGNAL("Server(QString)"),self.cambienduoi)
        self.connect(self.thrad4,QtCore.SIGNAL("Server1(QString)"),self.cambientren)
    def my_callbacklen(self,channel):
        if GPIO.input(23) == 0:
			global CBT
			CBT=1
        else:                  # if port 25 != 1
            print ("tat")
    def my_callbackxuong(self,channel):
        if GPIO.input(24) == 0:
			global CBD
			CBD=1
        else:                  # if port 25 != 1
            print ("tat")
    def cambientren(self):
        global CBT
        CBT=1
    def cambienduoi(self):
        global CBD
        CBD=1
    def Updata_color_on(self):
        global mauR,mauG,mauB,mauBoff,mauRoff,mauGoff,tocdooff,tocdoon
        try:
            giatri=self.Ron.value()
            self.giatriRon=(giatri*255)//99
            giatri=self.Gon.value()
            self.giatriGon=(giatri*255)//99
            giatri=self.Bon.value()
            self.giatriBon=(giatri*255)//99
            mauR=str(self.giatriRon)
            mauG=str(self.giatriGon)
            mauB=str(self.giatriBon)
            f = open('luubien.txt','w+')
            f.write("Ron:"+str(mauR)+" Gon:" + str(mauG)+" Bon:" + str(mauB)+" end\r\n")
            f.write("Roff:"+str(mauRoff)+" Goff:" + str(mauGoff)+" Boff:" + str(mauBoff)+" end\r\n")
            f.write("SpeedON:"+str(tocdoon)+" SpeedOFF:" + str(tocdooff)+" end\r\n")
            f.close()
        except:
            print("co loi")
    def Updata_color_off(self):
        try:
            global mauR,mauG,mauB,mauBoff,mauRoff,mauGoff,tocdooff,tocdoon
            giatri=self.Roff.value()
            self.giatriRoff=(giatri*255)//99
            giatri=self.Goff.value()
            self.giatriGoff=(giatri*255)//99
            giatri=self.Boff.value()
            self.giatriBoff=(giatri*255)//99
            mauRoff=str(self.giatriRoff)
            mauGoff=str(self.giatriGoff)
            mauBoff=str(self.giatriBoff)
            f = open('luubien.txt','w+')
            f.write("Ron:"+str(mauR)+" Gon:" + str(mauG)+" Bon:" + str(mauB)+" end\r\n")
            f.write("Roff:"+str(mauRoff)+" Goff:" + str(mauGoff)+" Boff:" + str(mauBoff)+" end\r\n")
            f.write("SpeedON:"+str(tocdoon)+" SpeedOFF:" + str(tocdooff)+" end\r\n")
            f.close()
        except:
            print("co loi")
    def Up_speed(self):
        try:
            global mauR,mauG,mauB,mauBoff,mauRoff,mauGoff,tocdooff,tocdoon
            tocdoon1=self.Speed_up.value()
            tocdoon=(tocdoon1*30)//99
            tocdooff1=self.Speed_down.value()
            tocdooff=(tocdooff1*50)//99
            f = open('luubien.txt','w+')
            f.write("Ron:"+str(mauR)+" Gon:" + str(mauG)+" Bon:" + str(mauB)+" end\r\n")
            f.write("Roff:"+str(mauRoff)+" Goff:" + str(mauGoff)+" Boff:" + str(mauBoff)+" end\r\n")
            f.write("SpeedON:"+str(tocdoon)+" SpeedOFF:" + str(tocdooff)+" end\r\n")
            f.close()
        except:
            print("co loi")
    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label.setText(_translate("MainWindow", "Mau sang", None))
        self.Updata_coloron.setText(_translate("MainWindow", "Update", None))
        self.label_4.setText(_translate("MainWindow", "B : ", None))
        self.label_3.setText(_translate("MainWindow", "G : ", None))
        self.label_2.setText(_translate("MainWindow", "R : ", None))
        self.label_5.setText(_translate("MainWindow", "Mau tat", None))
        self.label_6.setText(_translate("MainWindow", "R : ", None))
        self.label_7.setText(_translate("MainWindow", "G : ", None))
        self.label_8.setText(_translate("MainWindow", "B : ", None))
        self.Updata_coleroff.setText(_translate("MainWindow", "Update", None))
        self.label_10.setText(_translate("MainWindow", "Up", None))
        self.Updata_speed.setText(_translate("MainWindow", "Update", None))
        self.label_11.setText(_translate("MainWindow", "Down", None))
        self.label_9.setText(_translate("MainWindow", "Speed", None))
        self.CBtren.setText(_translate("MainWindow", "CB tren", None))
        self.CBduoi.setText(_translate("MainWindow", "CB duoi", None))
        self.offall.setText(_translate("MainWindow", "Turn Off", None))
        self.menuSetup.setTitle(_translate("MainWindow", "Setup", None))
if __name__ == "__main__":
    import sys
    rs232 = serial.Serial("/dev/ttyAMA0",baudrate=9600)
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

