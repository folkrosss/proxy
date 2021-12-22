# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox, QAction, qApp, QMenu, QApplication, QDialog, QSystemTrayIcon, QStyle
from processor import Processor
import win10toast
import threading
import geoip2.database
import init
import sys  
import widget
import os

class Scanner(QtWidgets.QMainWindow, widget.Ui_MainWindow):    

    def __init__(self):    
        super().__init__()
        
        self.setupUi(self)        
        self.index = 0      
        self.works = 0
        self.toaster = win10toast.ToastNotifier()
        self.toaster.show_toast("Загрузите список прокси для проверки...", duration = 5, threaded = True)
        self.pushButton.clicked.connect(self.opentxt)
 

        self.tray = QSystemTrayIcon(self)

        f = open('http_output.txt', 'w+')
        f.seek(0)
        f.close()
        f = open('https_output.txt', 'w+')
        f.seek(0)
        f.close()
        f = open('socks_output.txt', 'w+')
        f.seek(0)
        f.close()



        
        header = self.tableWidget.horizontalHeader()    
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        
        
        xloadAction = QAction("Загрузить список", self)
        xloadAction.setShortcut("Ctrl+F")
        xloadAction.setStatusTip("Загрузить список...")
        xloadAction.triggered.connect(self.select)
        
        xstartAction = QAction("Запустить", self)
        xstartAction.setShortcut("F5")
        xstartAction.setStatusTip("Запустить проверку...")
        xstartAction.triggered.connect(self.start)    

        xstopAction = QAction("Остановить", self)
        xstopAction.setShortcut("Esc")
        xstopAction.setStatusTip("Остановить проверку...")
        xstopAction.triggered.connect(self.stop)

        
      


        fileMenu = self.menuBar.addMenu("File")
        fileMenu.addAction(xloadAction)
        fileMenu.addAction(xstartAction)
        fileMenu.addAction(xstopAction)
        
        fileMenu.addSeparator()
        

    def opentxt(self):
        os.system("notepad http_output.txt")
        os.system("notepad https_output.txt")
        os.system("notepad socks_output.txt")
                
    def append(self, background, ipaddress, enaddress, types, sessions, response):   
    
        try: 
            locat = geoip2.database.Reader("./country/country.mmdb")
            c = locat.country(ipaddress)
            country = c.country.name
            
        except geoip2.errors.AddressNotFoundError:
            c = locat.country("162.162.162.162")
            country = c.country.name
            
        except ValueError:
            c = locat.country("162.162.162.162")
            country = c.country.name
       
        index = 0
        self.index = self.index + 1

        index = self.index - 1
           # Progress bar metod...

    

        check = QtWidgets.QCheckBox()
        self.tableWidget.setCellWidget(index, 0, check)        
      
        item = QtWidgets.QTableWidgetItem(ipaddress)
        self.tableWidget.setItem(index, 1, item) 
        
        item = QtWidgets.QTableWidgetItem(enaddress)
        item.setBackground(QtGui.QColor(237, 237, 237))
        self.tableWidget.setItem(index, 2, item)               

        item = QtWidgets.QTableWidgetItem(country)
        item.setForeground(QtGui.QColor(177, 177, 177))
        self.tableWidget.setItem(index, 3, item)               

        titem = QtWidgets.QTableWidgetItem(types)
        self.tableWidget.setItem(index, 4, titem)               

        sitem = QtWidgets.QTableWidgetItem(sessions)
        self.tableWidget.setItem(index, 5, sitem)               

        item = QtWidgets.QTableWidgetItem(response)
        self.tableWidget.setItem(index, 6, item)               
        

        if background != 0:
            
            
            check.setStyleSheet("QCheckBox::indicator {background-image: url(img/accept.png); background-repeat: no-repeat; background-position: center; width: 14px; height: 14px;}" "QCheckBox {margin: 8px;}")
            titem.setForeground(QtGui.QColor(77, 187, 85))
      
            sitem.setBackground(QtGui.QColor(126, 224, 120))
            sitem.setForeground(QtGui.QColor(255, 255, 255))
           
            self.writer(ipaddress, enaddress, types)

        else:

            check.setStyleSheet("QCheckBox::indicator {background-image: url(img/delete.png); background-repeat: no-repeat; background-position: center; width: 14px; height: 14px;}" "QCheckBox {margin: 8px;}")
            
        self.tableWidget.repaint()
        self.tableWidget.scrollToItem(item)

        

    def writer(self, ipaddress, enaddress, types):
        with open(types.lower() + "_output.txt", "a") as files:
            files.write(ipaddress + ":" + enaddress + "\n")
            

    def start(self):    
        
        value = self.spinBox.value() 
        files = self.lineEdit.text()
        delay = self.spinBox_2.text()
        timeout = self.spinBox_3.text()
        
        delay = int(delay)
        delay = delay / 10

        self.th = Processor(files, value, timeout, delay)
        self.th.length.connect(self.append)
        threading.Thread(target = self.th.running).start()
        
     



    
    def clear(self):    
        self.tableWidget.setRowCount(0)
        self.tableWidget.setRowCount(12)
        self.label_05.setText("0")
        self.label_07.setText("0")
        self.label_09.setText("0")
        self.label_11.setText("0")       
        self.statusBar().showMessage("Reset data...")
        
    
    def stop(self):    
        self.th.stop()
        
       
        
   
    def select(self):    
    
        self.file = QtWidgets.QFileDialog.getOpenFileName(self, "Select file", "C:",  "(*.txt)")[0]
        if self.file != "":
            self.lineEdit.setText(self.file)
            self.count = open(self.file, encoding = "iso-8859-1").readlines()
            self.count = len(self.count)
            self.count = int(self.count)
            
            self.tableWidget.setRowCount(self.count)
            self.statusBar().showMessage("List add...")
        else:
            pass
            

       

def main():
    app = QtWidgets.QApplication(sys.argv)    
    window = Scanner()
    window.show()
    app.exec_()

if __name__ == '__main__':

    main()