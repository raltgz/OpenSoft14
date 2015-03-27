'''
Created on Mar 13, 2014

@author: sourya
TO DO:
Provide GUI for drag and drop of image files, and adding files manually through file browser

Implemented drag and drop for removing selected images
'''


from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtGui, QtCore
import os
import sys
import time
import re
import winsound
from PyQt4.Qt import QLabel, QTableWidget

#Lots of local images used, be sure check them out before running

THUMBNAIL_SIZE = 128
SPACING        = 5
IMAGES_PER_ROW = 5
file_formats=['bmp','gif','ico','jpeg','jpg','mng','pbm','pgm','png','ppm','svg','svgz','tga','tif','tiff','xbm','xpm']
exp='((bmp)|(gif)|(ico)|(jpeg)|(jpg)|(mng)|(pbm)|(pgm)|(png)|(ppm)|(svg)|(svgz)|(tga)|(tif)|(tiff)|(xbm)|(xpm))$'
import glob

selected_index=[]

''' 
links contains the absoulte paths of all the image files uploaded at
all points of time 
'''
links=[]


'''
Class which provide the transparent layer saying
   DRAG FILES HERE
'''
class Overlay(QWidget):
    def __init__(self, parent = None):
 
        QWidget.__init__(self, parent)
        self.drag=True
        #False for drop
        palette = QPalette(self.palette())
        palette.setColor(palette.Background, QtGui.QColor(255,0,0))
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setPalette(palette)

    def paintEvent(self, event):
        width=self.parent().size().width()
        height=self.parent().size().height()
        self.setGeometry(0,0,width,height)
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(QColor(255, 0, 0)))
        painter.setBrush(QtGui.QColor(25, 0, 90, 200))
        painter.setOpacity(0.60)
        if self.drag:
            p=QPixmap(r'drive_drag.png')
        else:
            p=QPixmap(r'drive_drop.png')

        p=p.scaled(width,height)
        painter.drawPixmap(0, 0, p)
        painter.end()



class TableWidget(QTableWidget):
    
    def __init__(self, parent=None, **kwargs):
        QTableWidget.__init__(self, parent, **kwargs)

        self.setAcceptDrops(True)
        self.setMouseTracking(True)
        self.cur_col=0
        self.cur_row=0
        self.last_time=time.time()
        self.setIconSize(QSize(THUMBNAIL_SIZE,THUMBNAIL_SIZE))
        self.setColumnCount(IMAGES_PER_ROW)
        self.setGridStyle(Qt.NoPen)
        self.cellClicked.connect(self.clicked)
        self.cellPressed.connect(self.pressed)
        self.setDragEnabled(True)
        self.verticalHeader().setDefaultSectionSize(THUMBNAIL_SIZE+SPACING)
        self.verticalHeader().hide()
        self.horizontalHeader().setDefaultSectionSize(THUMBNAIL_SIZE+SPACING)
        self.horizontalHeader().hide()
        self.setMaximumWidth((THUMBNAIL_SIZE+SPACING)*IMAGES_PER_ROW+(SPACING*2))
        self.setMaximumHeight(400)
        self.overlay=Overlay(self)
        self.doubleClicked.connect(self.foobar)
    
    def clicked(self,row,column):
        self.emit(QtCore.SIGNAL('preview'),row,column)

    def foobar(self,index):
        print(index.row(),index.column(),'double')
        os.startfile(links[index.row()*IMAGES_PER_ROW+index.column()])
        

    def pressed(self,row,col):
        global selected_index
        selected_index=self.selectedIndexes()
      
    def focusOutEvent(self,event):
        global selected_index
        selected_index=[]
    def dragLeaveEvent(self,event):
        self.overlay.drag=True
        self.overlay.repaint()

    def dragEnterEvent(self, event):
        if  selected_index:
            event.ignore
            return
        if event.mimeData().hasUrls:
            self.overlay.drag=False
            self.overlay.repaint()
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        print('drag moved')
        print(self.indexAt(event.pos()).row(),self.indexAt(event.pos()).column())
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()
    
    def append_files_recursively(self,path):
        if os.path.isfile(path):
            pattern=re.compile(exp,re.IGNORECASE)
            if pattern.search(path):
                if path in links:
                    return
                links.append(path)
                self.emit(QtCore.SIGNAL("dropped"))
                return
       
           
            
        if os.path.isdir(path):
            for f in glob.glob(os.path.join(path,'*')):
                self.append_files_recursively(f)
            return
    def dropEvent(self, event):
        self.overlay.drag=True
        self.overlay.repaint()
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            for url in event.mimeData().urls():
                x=str(url.toLocalFile())
                winsound.PlaySound('beep.wav' , winsound.SND_FILENAME)

                x=x.replace('/', '\\')
                #x=x.decode()
                print(x)
                self.append_files_recursively(x)
        else:
            event.ignore()
 
    def addPicture(self, row, col, picturePath):
        item=QTableWidgetItem()
        item.setFlags(QtCore.Qt.NoItemFlags | QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsDragEnabled )
    
 
        # Scale the image by either height or width and then 'crop' it to the
        # desired size, this prevents distortion of the image.
        p=QPixmap(picturePath)
        if p.height()>p.width(): p=p.scaledToWidth(THUMBNAIL_SIZE)
        else: p=p.scaledToHeight(THUMBNAIL_SIZE)
        p=p.copy(0,0,THUMBNAIL_SIZE,THUMBNAIL_SIZE)
        item.setIcon(QIcon(p))
        self.setItem(row,col,item)
        
        for p in range(col+1,IMAGES_PER_ROW):
            i=QTableWidgetItem()
            i.setFlags(QtCore.Qt.NoItemFlags)
            self.setItem(row,p,i)
import glob

class Laabel(QLabel):
    def __init__(self, parent=None, **kwargs):
        QLabel.__init__(self, parent, **kwargs)
        self.setAcceptDrops(True)
        self.closed=True
        self.getupdate()

    def getupdate(self):
        p=QPixmap(150,170)
        if self.closed:
            p.load(r'closed.jpg')
        else:
            p.load(r'open.jpg')
        self.setPixmap(p)
    def dragEnterEvent(self, event):
        if not selected_index:
            event.ignore()
            return
        event.accept()
        self.closed=False
        self.getupdate()
        return
        if event.mimeData().hasImage():
            event.accept()
        else:
            event.ignore()
    def drageLeaveEvent(self,event):
        #print('left amma')
        event.accept()
        self.closed=True
        self.getupdate()
    def dropEvent(self,event):
        if not selected_index:
            event.ignore()
            return

        event.accept()
        self.closed=True
        self.getupdate()
        #for x in selected_index:
        #    links.pop(x.row()*IMAGES_PER_ROW+x.column())
        self.emit(QtCore.SIGNAL('bhak'))

        
    
class MainWindow(QMainWindow):
    def __init__(self, parent=None, **kwargs):
        QMainWindow.__init__(self, parent, **kwargs)
        centralWidget=QWidget(self)
        
        self.l=QGridLayout(centralWidget)
 
        self.tableWidget=TableWidget(self)
        self.l.addWidget(self.tableWidget,0,0)
        
        self.preview=QLabel(self)
        self.l.addWidget(self.preview,0,1)
        
        self.curr_path=''
 
        self.trash=Laabel(self)
        self.l.addWidget(self.trash,3,0)

        self.setCentralWidget(centralWidget)
        
        self.filebutton=QPushButton('Select Files')
        self.l.addWidget(self.filebutton,1,0)
        self.filebutton.setMaximumWidth(80)
        self.filebutton.clicked.connect(self.openfile)
        
        self.dirbutton=QPushButton('Select Directory')
        self.l.addWidget(self.dirbutton,2,0)
        self.dirbutton.setMaximumWidth(100)
        self.dirbutton.clicked.connect(self.opendir)
        self.connect(self.tableWidget, QtCore.SIGNAL('preview'),self.preview_shot)
        self.connect(self.tableWidget, QtCore.SIGNAL("dropped"), self.pictureDropped)
        self.connect(self.tableWidget,QtCore.SIGNAL('bhak'),self.delete_and_drawagain)
        self.connect(self.trash,QtCore.SIGNAL('bhak'),self.delete_and_drawagain)
        
        self.row=-1

    def preview_shot(self,row,column):
        p=QPixmap()
        if row*IMAGES_PER_ROW+column>=len(links):
            return
        self.curr_path=links[row*IMAGES_PER_ROW+column]
        p.load(links[row*IMAGES_PER_ROW+column])
        if p.height()>p.width():
            p=p.scaledToHeight(300)
        else:
            p=p.scaledToWidth(300)
        self.preview.setPixmap(p)

    def dragMoveEvent(self, event):
        print('main drag moved')
    def foobar(self):
        print('dafuq')

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.MouseMove:
            self.tableWidget.overlay.drag=True
            self.tableWidget.overlay.repaint()
            self.trash.closed=True
            self.trash.getupdate()
            '''
            index=self.indexAt(event.pos())
            print(index.row(),index.column())
            if index.row()==-1 or index.column()==-1:
                self.overlay.drag=True
                self.overlay.repaint()
                return QTableWidget.eventFilter(self, source, event)
            '''
        return QMainWindow.eventFilter(self, source, event)
    def append_files_recursively(self,path):
        if os.path.isfile(path):
            pattern=re.compile(exp,re.IGNORECASE)
            if pattern.search(path):
                if path in links:
                    return
                links.append(path)
                self.pictureDropped()
                return
       
           
            
        if os.path.isdir(path):
            for f in glob.glob(os.path.join(path,'*')):
                self.append_files_recursively(f)
            return
    def openfile(self):
        x=QFileDialog(self)
        
        
        
        f=x.getOpenFileNames(filter='*.bmp *.gif *.ico *.jpeg *.jpg  *.mng  *.pbm  *.pgm  *.png  *.ppm  *.svg  *.svgz  *.tga  *.tif  *.tiff  *.xbm  *.xpm')
        for i in f:
            self.append_files_recursively(i)
    def opendir(self):
        fi = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.append_files_recursively(fi)
        
         

        
        
           
    def pictureDropped(self):
            #print("afasf")
            
            print(links[-1])

            rowCount=len(links)//IMAGES_PER_ROW
            if len(links)%IMAGES_PER_ROW: rowCount+=1
            self.tableWidget.setRowCount(rowCount)
            
            col=(len(links)-1)%IMAGES_PER_ROW
            if not col: self.row+=1
            #print(self.row,col)           
            self.row=rowCount-1
            self.tableWidget.addPicture(self.row,col,links[-1])
            
    def delete_and_drawagain(self):
        #winsound.PlaySound('papercrumble.wav' , winsound.SND_FILENAME) 
        winsound.PlaySound('beep.wav' , winsound.SND_FILENAME)
        global links
        lowest=100000000
        lowest_row=0
        print(len(links))
        global selected_index
        indexes=[]

        for x in selected_index:
            index=x.row()*IMAGES_PER_ROW+x.column()
            indexes.append(index)
            #print(index)
            if index < lowest:
                index=lowest
                lowest_row=x.row()
        indexes.sort()
        print(indexes)
        for i in reversed(range(len(indexes))):
            if links.pop(indexes[i])==self.curr_path:
                self.preview.clear()
        for i in reversed(range(lowest_row,self.tableWidget.rowCount())):
            self.tableWidget.removeRow(i)
        print(range(self.tableWidget.rowCount()*IMAGES_PER_ROW,len(links)))
        for i in range(self.tableWidget.rowCount()*IMAGES_PER_ROW,len(links)):
            rowCount=(i+1)//IMAGES_PER_ROW
            if (i+1)%IMAGES_PER_ROW: rowCount+=1
            self.tableWidget.setRowCount(rowCount)
            col=(i)%IMAGES_PER_ROW
            self.row=rowCount-1
            print(self.row,col,self.tableWidget.rowCount())
            self.tableWidget.addPicture(self.row, col, links[i])
        #selected_index=[]
    '''
    def drawagain(self):
        print('bhagsale')
        self.row=-1
        for i in reversed(range(self.tableWidget.rowCount())):
            self.tableWidget.removeRow(i)

        #print(links)
        for i in range(len(links)):
            rowCount=(i+1)//IMAGES_PER_ROW
            if (i+1)%IMAGES_PER_ROW: rowCount+=1
            self.tableWidget.setRowCount(rowCount)
            col=(i)%IMAGES_PER_ROW
            if not col:self.row+=1
            print(self.row,col,self.tableWidget.rowCount())
            self.tableWidget.addPicture(self.row, col, links[i])
    '''
 
if __name__=="__main__":
    from sys import argv, exit
 
    a=QApplication(argv)
    m=MainWindow()
    a.installEventFilter(m)
    m.resize(1200,700)
    m.show()
    m.raise_()
    exit(a.exec_())