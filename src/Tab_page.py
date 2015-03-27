import sys, random
from PyQt4 import QtCore, QtGui
#from msilib.schema import Shortcut

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
import Match
import re
#import winsound
#from Match import *
from PyQt4.Qt import QLabel, QTableWidget, QWidget, QIcon

#Lots of local images used, be sure check them out before running
''' Don't ever change these in code. '''
THUMBNAIL_SIZE = 128
SPACING        = 5
IMAGES_PER_ROW = 5


file_formats=['bmp','gif','ico','jpeg','jpg','mng','pbm','pgm','png','ppm','svg','svgz','tga','tif','tiff','xbm','xpm']
exp='((bmp)|(gif)|(ico)|(jpeg)|(jpg)|(mng)|(pbm)|(pgm)|(png)|(ppm)|(svg)|(svgz)|(tga)|(tif)|(tiff)|(xbm)|(xpm))$'
import glob


''' 
links contains the absoulte paths of all the image files uploaded at
all points of time 
'''


'''
Class which provide the transparent layer saying
   DRAG FILES HERE
'''
from threading import Thread

class MyThread(QThread):
    def on_thread_finished(self, thread, data):
        pass
    def __init__(self, parent=None):
        QThread.__init__(self)
        self.parent = parent
        self.threadlinks=[]
    def run(self):
        in_links=list(self.parent.tableWidget.links)
        thresholdarray=[]
        thresholdarray.append(self.parent.thresholdpath)
        thresholdarray.extend(in_links)
        print("inpuuuuuuuuuuuuuuuuuuuuuuut",thresholdarray)
        out_links=Match.execute(thresholdarray,self.parent.cache.overlay)
        self.parent and self.parent.on_thread_finished(self, out_links)
        self.emit(QtCore.SIGNAL('finished'),list(out_links))


'''
if __name__ == '__main__':
    t = GetTitleThread('SomeSong.mp3')
    t.start()
    t.join()
    print t.sTitle
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
class Tick(QWidget):

    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.drag=True
        self.row=-1
        self.column=-1
        self.scrollposition=0
        self.pixmap=None
        self.path='tick.jpg'
        #False for drop
        palette = QPalette(self.palette())
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setPalette(palette)
        self.hide()
        self.setHidden(True)

    def paintEvent(self, event):
        print('painting tick',self.row,self.column)
        if not (self.row==-1 or self.column==-1):
            print('inside')
            if self.scrollposition%2:
                self.setGeometry((THUMBNAIL_SIZE+SPACING)*self.column,((THUMBNAIL_SIZE+SPACING)*((self.row+1)%2)),30,23)
            else:
                self.setGeometry((THUMBNAIL_SIZE+SPACING)*self.column,((THUMBNAIL_SIZE+SPACING)*((self.row)%2)),30,23)
            painter = QPainter()
            painter.begin(self)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setPen(QPen(QColor(255, 0, 0)))
            painter.setBrush(QtGui.QColor(25, 0, 90, 200))
            p=QPixmap(self.path)
            painter.drawPixmap(0, 0, p)
            painter.end()

class Highlight(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.row=0
        self.column=0
        self.pixmap=None
        self.scrollposition=0
        #False for drop
        palette = QPalette(self.palette())
        palette.setColor(palette.Background, QtGui.QColor(255,0,0))
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setPalette(palette)
    def paintEvent(self, event):
        #self.setGeometry(self.row*(THUMBNAIL_SIZE+SPACING),self.column*(THUMBNAIL_SIZE+SPACING),0,0)

        print('___________paintiiinnnggg',self.row,self.column)
        if self.scrollposition%2:
            self.setGeometry((THUMBNAIL_SIZE+SPACING)*self.column,((THUMBNAIL_SIZE+SPACING)*((self.row+1)%2)),THUMBNAIL_SIZE,THUMBNAIL_SIZE)
        else:
            self.setGeometry((THUMBNAIL_SIZE+SPACING)*self.column,((THUMBNAIL_SIZE+SPACING)*((self.row)%2)),THUMBNAIL_SIZE,THUMBNAIL_SIZE)
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(QColor(255, 0, 0)))
        painter.setBrush(QtGui.QColor(25, 0, 90, 200))
        p=QPixmap()
        if not self.pixmap==None:
            print('paintiiinnnggg')
            p=QPixmap(self.pixmap)
            #self.setGeometry(self.row*(THUMBNAIL_SIZE+SPACING),self.column*(THUMBNAIL_SIZE+SPACING),THUMBNAIL_SIZE,THUMBNAIL_SIZE)
            p=p.scaled(THUMBNAIL_SIZE,THUMBNAIL_SIZE)
            painter.drawPixmap(0, 0, p)
        painter.end()


class TableWidget(QTableWidget):
    
    def __init__(self, parent=None, **kwargs):
        QTableWidget.__init__(self, parent, **kwargs)
        
        print(self.parent())
        self.dragging_cells=False
        self.setAcceptDrops(True)
        self.setMouseTracking(True)
        self.cur_col=0
        self.links=[]
        self.swap_index_row=0
        self.swap_index_column=0
        
        self.selected_index=[]
        self.cur_row=0
        self.last_time=time.time()
        self.setIconSize(QSize(THUMBNAIL_SIZE,THUMBNAIL_SIZE))
        self.setColumnCount(IMAGES_PER_ROW)
        self.setGridStyle(Qt.NoPen)
        self.cellClicked.connect(self.clicked)
        self.cellPressed.connect(self.pressed)

        self.cellEntered.connect(self.enter)
        self.setDragEnabled(True)
        self.verticalHeader().setDefaultSectionSize(THUMBNAIL_SIZE+SPACING)
        self.verticalHeader().hide()
        self.horizontalHeader().setDefaultSectionSize(THUMBNAIL_SIZE+SPACING)
        self.horizontalHeader().hide()
        self.setMaximumWidth((THUMBNAIL_SIZE+SPACING)*IMAGES_PER_ROW+(SPACING*2)+10)
        self.setMinimumWidth((THUMBNAIL_SIZE+SPACING)*IMAGES_PER_ROW+(SPACING*2)+10)
        self.setMaximumHeight(276)
        self.overlay=Overlay(self)
        self.doubleClicked.connect(self.foobar)
        
        self.ticks=[]
        
        
        self.highlight=Highlight(self)
        self.setVerticalStepsPerItem(0)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerItem)
        self.verticalScrollBar().valueChanged.connect(self.scrolled)

    def leaveEvent(self, event):
        
        self.emit(QtCore.SIGNAL('preview'),-1,-1)
        print('wwwwwwwwwwwwooooooooooooooooo')

        self.highlight.hide()
        
    
    def scrolled(self):
        '''
        if not (self.verticalScrollBar().sliderPosition()==0 or self.verticalScrollBar().sliderPosition()%2==1):
            self.verticalScrollBar().setSliderPosition(self.verticalScrollBar().sliderPosition()-1)
        '''
        sliderposition=self.verticalScrollBar().sliderPosition()
        print('vlakf',self.verticalStepsPerItem())
        for x in self.ticks:
            x.deleteLater()
            x.destroy()
        self.ticks=[]
        for index in self.selected_index:
            if index.row()==sliderposition or index.row()==sliderposition+1:
                tick=Tick(self)
                self.ticks.append(tick)
                tick.row=index.row()
                tick.scrollposition=self.verticalScrollBar().sliderPosition()
                tick.column=index.column()
                tick.repaint()
                tick.show()
        print('scrolled',self.verticalScrollBar().sliderPosition()) 
        
    def mouseReleaseEvent(self,event):
        print('releeaaaased')
        return super(TableWidget,self).mouseReleaseEvent(event)

    def exchange(self,row,column):    
        print('exchanging')
        drag_row=self.selected_index[0].row()
        drag_column=self.selected_index[0].column()
        for x in self.selected_index:
            print(x.row(),x.column())
        self.selected_index=[]
        print('select',drag_row,drag_column)
        print('drag',row,column)
       
        for tick in reversed(self.ticks):
            tick.deleteLater()
            tick.destroy()
            self.ticks.remove(tick)
        
        
        item=QTableWidgetItem()
        item.setFlags(QtCore.Qt.NoItemFlags | QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsDragEnabled )
        
        link1=self.links[row*IMAGES_PER_ROW+column]
        link2=self.links[drag_row*IMAGES_PER_ROW+drag_column]
        self.links[row*IMAGES_PER_ROW+column]=link2
        self.links[drag_row*IMAGES_PER_ROW+drag_column]=link1

        p=QPixmap(link1)
        if p.height()>p.width(): p=p.scaledToWidth(THUMBNAIL_SIZE)
        else: p=p.scaledToHeight(THUMBNAIL_SIZE)
        p=p.copy(0,0,THUMBNAIL_SIZE,THUMBNAIL_SIZE)
        item.setIcon(QIcon(p))
        self.setItem(drag_row,drag_column,item)

        item1=QTableWidgetItem()
        item1.setFlags(QtCore.Qt.NoItemFlags | QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsDragEnabled )
        p=QPixmap(link2)
        if p.height()>p.width(): p=p.scaledToWidth(THUMBNAIL_SIZE)
        else: p=p.scaledToHeight(THUMBNAIL_SIZE)
        p=p.copy(0,0,THUMBNAIL_SIZE,THUMBNAIL_SIZE)
        item1.setIcon(QIcon(p))
        self.setItem(row,column,item1)

        p=QPixmap(self.links[row*IMAGES_PER_ROW+column])
        if p.height()>p.width(): p=p.scaledToWidth(THUMBNAIL_SIZE)
        else: p=p.scaledToHeight(THUMBNAIL_SIZE)
        p=p.copy(0,0,THUMBNAIL_SIZE,THUMBNAIL_SIZE)
        self.highlight.pixmap=p
        self.highlight.row=row
        self.highlight.column=column
        self.highlight.scrollposition=self.verticalScrollBar().sliderPosition()
        self.highlight.repaint()
        
        print('exxxxxxxxxcccccccccc')
        for index in self.selected_index:
            print(index.row(),index.column())
        print('done')
        self.emit(QtCore.SIGNAL('show_delete'),False)
        
        

        


    def enter(self,row,column): 
        if row*IMAGES_PER_ROW+column>=len(self.links):
            self.highlight.hide()
            self.dragging_cells=False
            return
        if row==-1 or column==-1:
            self.highlight.hide()
            self.dragging_cells=False
            return
        self.highlight.row=row
        self.highlight.column=column
         
        p=QPixmap(self.links[row*IMAGES_PER_ROW+column])
        if p.height()>p.width(): p=p.scaledToWidth(THUMBNAIL_SIZE)
        else: p=p.scaledToHeight(THUMBNAIL_SIZE)
        p=p.copy(0,0,THUMBNAIL_SIZE,THUMBNAIL_SIZE)
        self.highlight.pixmap=p
        self.highlight.scrollposition=self.verticalScrollBar().sliderPosition()
        self.highlight.repaint()
        self.highlight.show()
        if self.dragging_cells:
            self.exchange(row,column)
        print('entttttttteeeeeer',row,column)
        self.emit(QtCore.SIGNAL('preview'),row,column)
        self.dragging_cells=False
    def clicked(self,row,column):
        indexes=[]
        for x in self.selected_index:
            indexes.append(x.row()*IMAGES_PER_ROW+x.column())
        for i in reversed(range(len(self.ticks))):
            if self.ticks[i].row*IMAGES_PER_ROW+self.ticks[i].column in indexes:
                continue
            self.ticks[i].deleteLater()
            self.ticks[i].destroy()
            self.ticks.pop(i)
        if self.selected_index:
            self.emit(QtCore.SIGNAL('show_delete'),True)
        else:
            self.emit(QtCore.SIGNAL('show_delete'),False)
        
        self.emit(QtCore.SIGNAL('preview'),row,column)
        if row*IMAGES_PER_ROW+column in indexes:
            tick=Tick(self)
            self.ticks.append(tick)
            tick.row=row
            tick.column=column
            tick.scrollposition=self.verticalScrollBar().sliderPosition()
            tick.repaint()
            tick.show()
        print('clickeeeeeeeeeeeed')

    def foobar(self,index):
        print(index.row(),index.column(),'double')
        os.startfile(self.links[index.row()*IMAGES_PER_ROW+index.column()])
        

    def pressed(self,row,col):
        if self.dragging_cells:
            return
        self.selected_index=self.selectedIndexes()
        
    def dragLeaveEvent(self,event):
        index=self.indexAt(self.cursor().pos())
        print('left',index.row(),index.column())
        if index.row()==-1 or index.column==-1:
            self.dragging_cells=False
        self.overlay.drag=True
        self.overlay.repaint()

    def dragEnterEvent(self, event):
        
        if event.mimeData().hasUrls():
            self.overlay.drag=False
            self.overlay.repaint()
            event.accept()
        else:
            if  len(self.selected_index)==1:
                event.accept()
                return
            event.ignore()

    def dragMoveEvent(self, event):
        print('drag moved')
        if len(self.selected_index)==1:
            self.dragging_cells=True
            event.accept()
            return
        print(self.indexAt(event.pos()).row(),self.indexAt(event.pos()).column())
        print(self.dragging_cells)
        if event.mimeData().hasUrls():
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()
    
    def append_files_recursively(self,path):
        if os.path.isfile(path):
            pattern=re.compile(exp,re.IGNORECASE)
            if pattern.search(path):
                if path in self.links:
                    return
                self.links.append(path)
                self.emit(QtCore.SIGNAL("dropped"))
                return
        if os.path.isdir(path):
            for f in glob.glob(os.path.join(path,'*')):
                self.append_files_recursively(f)
            return
    def dropEvent(self, event):
        print('drrrrrrrooooooooooooopppppppppp')
        print(self.selected_index)
        if self.selected_index:
            index=self.itemAt(event.pos())
            print('drop',index)
            if index==None:
                self.dragging_cells=False
                print('hahahahhaah')
        self.overlay.drag=True
        self.overlay.repaint()
        if event.mimeData().hasUrls():
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            for url in event.mimeData().urls():
                x=str(url.toLocalFile())
                #winsound.PlaySound('beep.wav' , winsound.SND_FILENAME)
                x=x.replace('/', '\\')
                #x=x.decode()
                print(x)
                self.append_files_recursively(x)
        else:
            if len(self.selected_index):
                index=self.itemAt(event.pos())
                if index.row()==-1 or index.column()==-1:
                    self.dragging_cells=False
                    print('hahahahhaah')
                    return

            event.ignore()

    def addPicture(self, row, col, picturePath):
        item=QTableWidgetItem()
        item.setFlags(QtCore.Qt.NoItemFlags | QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsDragEnabled )
    

        # Scale the image by either height or width and then 'crop' it to the
        # desired size, this prevents distortion of the image.
        p=QPixmap(picturePath,"1")
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
class FinalTable(QTableWidget):
    
    def __init__(self, parent=None, **kwargs):
        QTableWidget.__init__(self, parent, **kwargs)
        
        print(self.parent())
        self.dragging_cells=False
        self.setAcceptDrops(False)
        self.setMouseTracking(True)
        self.cur_col=0
        self.links=[]
        self.swap_index_row=0
        self.swap_index_column=0
        
        self.selected_index=[]
        self.cur_row=0
        self.last_time=time.time()
        self.setIconSize(QSize(THUMBNAIL_SIZE,THUMBNAIL_SIZE))
        self.setColumnCount(IMAGES_PER_ROW)
        self.setGridStyle(Qt.NoPen)
        self.cellClicked.connect(self.clicked)
        self.cellPressed.connect(self.pressed)

        self.cellEntered.connect(self.enter)
        self.setDragEnabled(True)
        self.verticalHeader().setDefaultSectionSize(THUMBNAIL_SIZE+SPACING)
        self.verticalHeader().hide()
        self.horizontalHeader().setDefaultSectionSize(THUMBNAIL_SIZE+SPACING)
        self.horizontalHeader().hide()
        self.setMaximumWidth((THUMBNAIL_SIZE+SPACING)*IMAGES_PER_ROW+(SPACING*2)+10)
        self.setMinimumWidth((THUMBNAIL_SIZE+SPACING)*IMAGES_PER_ROW+(SPACING*2)+10)
        self.setMaximumHeight(276)
        self.doubleClicked.connect(self.foobar)
        
        
        

    def contextMenuEvent(self, event):
        index=self.indexAt(event.pos())
        row=index.row()
        col=index.column()
        if row==-1 or col==-1:
            return
        self.menu = QtGui.QMenu(self)
        renameAction = QtGui.QAction('Save Image', self)
        from functools import partial
        renameAction.triggered.connect(partial(self.saveimage,row,col))
        self.menu.addAction(renameAction)
        # add other required actions
        self.menu.popup(QtGui.QCursor.pos())

    def saveimage(self,row,col):

        import shutil
        import os
        name,extension=os.path.splitext(self.links[row*IMAGES_PER_ROW+col])
        print(name,extension)
        filename = QFileDialog.getSaveFileName(self,"Save Ouptut File", "", 'PNG (*.png)')
        filename=os.path.abspath(os.path.expanduser(str(filename)))
        print('file',str(filename))
        shutil.copy(self.links[row*IMAGES_PER_ROW+col], filename+extension)

        print('fffffffffffffffff',filename)
        print "renaming slot called"
        # get the selected cell and perform renaming

    def leaveEvent(self, event):
        
        self.emit(QtCore.SIGNAL('preview'),-1,-1)

        
    
        
    def mouseReleaseEvent(self,event):
        print('releeaaaased')
        return super(FinalTable,self).mouseReleaseEvent(event)

    def exchange(self,row,column):    
        print('exchanging')
        drag_row=self.selected_index[0].row()
        drag_column=self.selected_index[0].column()
        for x in self.selected_index:
            print(x.row(),x.column())
        self.selected_index=[]
        print('select',drag_row,drag_column)
        print('drag',row,column)
       
        
        
        item=QTableWidgetItem()
        item.setFlags(QtCore.Qt.NoItemFlags | QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsDragEnabled )
        
        link1=self.links[row*IMAGES_PER_ROW+column]
        link2=self.links[drag_row*IMAGES_PER_ROW+drag_column]
        self.links[row*IMAGES_PER_ROW+column]=link2
        self.links[drag_row*IMAGES_PER_ROW+drag_column]=link1

        p=QPixmap(link1)
        if p.height()>p.width(): p=p.scaledToWidth(THUMBNAIL_SIZE)
        else: p=p.scaledToHeight(THUMBNAIL_SIZE)
        p=p.copy(0,0,THUMBNAIL_SIZE,THUMBNAIL_SIZE)
        item.setIcon(QIcon(p))
        self.setItem(drag_row,drag_column,item)

        item1=QTableWidgetItem()
        item1.setFlags(QtCore.Qt.NoItemFlags | QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsDragEnabled )
        p=QPixmap(link2)
        if p.height()>p.width(): p=p.scaledToWidth(THUMBNAIL_SIZE)
        else: p=p.scaledToHeight(THUMBNAIL_SIZE)
        p=p.copy(0,0,THUMBNAIL_SIZE,THUMBNAIL_SIZE)
        item1.setIcon(QIcon(p))
        self.setItem(row,column,item1)

        p=QPixmap(self.links[row*IMAGES_PER_ROW+column])
        if p.height()>p.width(): p=p.scaledToWidth(THUMBNAIL_SIZE)
        else: p=p.scaledToHeight(THUMBNAIL_SIZE)
        p=p.copy(0,0,THUMBNAIL_SIZE,THUMBNAIL_SIZE)
        
        print('exxxxxxxxxcccccccccc')
        for index in self.selected_index:
            print(index.row(),index.column())
        print('done')
        self.emit(QtCore.SIGNAL('show_delete'),False)
        
        

        


    def enter(self,row,column): 
        print('finaaaaaaaaal',row,column)
        if row*IMAGES_PER_ROW+column>=len(self.links):
            print(row*IMAGES_PER_ROW+column,self.links)
            print('infor')
            self.dragging_cells=False
            return
        if row==-1 or column==-1:
            self.dragging_cells=False
            return
         
        print('enteeeeeeeeeeeeeeer finaaaaaaaaaaaaaaaaaaaaaaaaaaaaal')
        if self.dragging_cells:
            self.exchange(row,column)
        print('entttttttteeeeeer',row,column)
        self.emit(QtCore.SIGNAL('final_preview'),row,column)
        self.dragging_cells=False
    def clicked(self,row,column):
        indexes=[]
        self.selected_index=self.selectedIndexes()
        for x in self.selected_index:
            indexes.append(x.row()*IMAGES_PER_ROW+x.column())
        print('indeeeeeeexeeeeeeees',indexes)
        if self.selected_index:
            self.emit(QtCore.SIGNAL('show_delete'),True)
        else:
            self.emit(QtCore.SIGNAL('show_delete'),False)
        
        self.emit(QtCore.SIGNAL('preview'),row,column)
        print('clickeeeeeeeeeeeed')

    def foobar(self,index):
        print(index.row(),index.column(),'double')
        os.startfile(self.links[index.row()*IMAGES_PER_ROW+index.column()])
        

    def pressed(self,row,col):
        if self.dragging_cells:
            return
        self.selected_index=self.selectedIndexes()
        


    

    def addPicture(self, row, col, picturePath):
        item=QTableWidgetItem()
        item.setFlags(QtCore.Qt.NoItemFlags | QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsDragEnabled )
    

        # Scale the image by either height or width and then 'crop' it to the
        # desired size, this prevents distortion of the image.
        p=QPixmap(picturePath,"1")
        if p.height()>p.width(): p=p.scaledToWidth(THUMBNAIL_SIZE)
        else: p=p.scaledToHeight(THUMBNAIL_SIZE)
        p=p.copy(0,0,THUMBNAIL_SIZE,THUMBNAIL_SIZE)
        item.setIcon(QIcon(p))
        self.setItem(row,col,item)
        
        for p in range(col+1,IMAGES_PER_ROW):
            i=QTableWidgetItem()
            i.setFlags(QtCore.Qt.NoItemFlags)
            self.setItem(row,p,i)
            self.setItem(row,p,i)

class Laabel(QLabel):
    def __init__(self, parent=None, **kwargs):
        QLabel.__init__(self, parent, **kwargs)
        self.setAcceptDrops(True)
        self.x=self.parent()
        print(self.parent())
        self.closed=True
        self.getupdate()
        self.sel_index=[]
    def getupdate(self):
        p=QPixmap(150,170)
        if self.closed:
            p.load(r'closed.jpg')
        else:
            p.load(r'open.jpg')
        self.setPixmap(p)
    def leaveEvent(self,event): 
        print('trraash left')
        event.accept()
    def dragEnterEvent(self, event):
        self.emit(QtCore.SIGNAL('selected_index'))
        print(self.sel_index)
        if not self.sel_index:
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
    def dragMoveEvent(self,event):
        print('draaaaaagggg mooooovvvveed traaaaash')
        print('cursooor',self.geometry().contains(self.cursor().pos()))
        event.setDropAction(QtCore.Qt.CopyAction)
        event.accept()
    def dragLeaveEvent(self,event):
        print('left amma')
        self.closed=True
        self.getupdate()
        event.accept()
    def dropEvent(self,event):

        self.emit(QtCore.SIGNAL('selected_index'))
        if not self.sel_index:
            event.ignore()
            return

        event.accept()
        self.closed=True
        self.getupdate()
        #for x in selected_index:
        #    links.pop(x.row()*IMAGES_PER_ROW+x.column())
        self.emit(QtCore.SIGNAL('bhak'))

        
class StateSwitchEvent(QtCore.QEvent):
    StateSwitchType = QtCore.QEvent.User + 256

    def __init__(self, rand=0):
        super(StateSwitchEvent, self).__init__(StateSwitchEvent.StateSwitchType)

        self.m_rand = rand

    def rand(self):
        return self.m_rand

import time
BLOCKSIZE=110
SCREENSIZE=660
NUMBER=7
class QGraphicsRectWidget(QtGui.QGraphicsWidget):
    def __init__(self,paths,parent=None):
        QtGui.QGraphicsWidget.__init__(self)
        self.paths=list(paths)
        print('paaaaaaaaaaaaaaaaaaath',self.paths)
        self.ran=1
        print(self.ran)
    def paint(self, painter, option, widget):
        if int(time.time())%6==0:
            rand=random.randint(1,len(self.paths)-1)
            self.ran=rand
        path=self.paths[self.ran]
        pixmap=QPixmap(path,"1")
        pixmap=pixmap.scaled(BLOCKSIZE, BLOCKSIZE)
        painter.drawPixmap(self.rect(), pixmap, self.rect())
        
        #painter.fillRect(self.rect(), QtCore.Qt.blue)




class StateSwitchTransition(QtCore.QAbstractTransition):
    def __init__(self, rand):
        super(StateSwitchTransition, self).__init__()

        self.m_rand = rand

    def eventTest(self, event):
        return (event.type() == StateSwitchEvent.StateSwitchType and
                event.rand() == self.m_rand)

    def onTransition(self, event):
        pass


class StateSwitcher(QtCore.QState):
    def __init__(self, machine):
        super(StateSwitcher, self).__init__(machine)

        self.m_stateCount = 0
        self.m_lastIndex = 0

    def onEntry(self, event):
        n = QtCore.qrand() % self.m_stateCount + 1
        while n == self.m_lastIndex:
            n = QtCore.qrand() % self.m_stateCount + 1

        self.m_lastIndex = n
        self.machine().postEvent(StateSwitchEvent(n))

    def onExit(self, event):
        pass

    def addState(self, state, animation):
        self.m_stateCount += 1
        trans = StateSwitchTransition(self.m_stateCount)
        trans.setTargetState(state)
        self.addTransition(trans)
        trans.addAnimation(animation)


def createGeometryState(w1, rect1, w2, rect2, w3, rect3, w4, rect4, parent):
    result = QtCore.QState(parent)

    result.assignProperty(w1, 'geometry', rect1)
    result.assignProperty(w2, 'geometry', rect2)
    result.assignProperty(w3, 'geometry', rect3)
    result.assignProperty(w4, 'geometry', rect4)

    return result        
class MainWindow(QWidget):
    def __init__(self, parent=None, **kwargs):
        QWidget.__init__(self, parent, **kwargs)
        #centralWidget=QWidget(self)
        self.l=QGridLayout()
        self.l.setAlignment(QtCore.Qt.AlignTop)
        self.grouped_1=QWidget()
        self.grouped_1.setMinimumSize(700, 700)
        self.grouped_1.setMaximumSize(700, 700)
        palette=QPalette(self.grouped_1.palette())
        palette.setColor(palette.Background, Qt.transparent)
        self.grouped_1.setPalette(palette)
        y1=QGridLayout()
        self.animationrunning=False
        self.threads=[]
        
        self.grouped_2=QWidget()
        self.grouped_2.setMinimumSize(540, 600)
        self.grouped_2.setMaximumSize(540, 800)
        y2=QGridLayout()
        self.thr_=QPushButton('Upload Blank Image for Thresholding')

        self.tableWidget=TableWidget(parent=self)
        y1.addWidget(self.thr_,0,0)
        y1.addWidget(self.tableWidget,1,0)
        self.tableWidget.setMaximumHeight(268)
        
        self.finaltable=FinalTable(parent=self)
        self.finaltable.setAcceptDrops(False)
        
        
        
        
        self.thr_.clicked.connect(self.openfile_1)
        self.thr_.setCursor(QtCore.Qt.PointingHandCursor)
        self.preview=QLabel(parent=self)
        self.preview.setMinimumHeight(227)
        
        
        self.preview.setAlignment(Qt.AlignCenter)
        self.preview.setMaximumHeight(227)
        y1.addWidget(self.preview,2,0)
        self.curr_path=''
        '''
        self.image=QLabel(self)
        pixmap=QPixmap('very_perfect.png')
        self.image.setPixmap(pixmap)
        self.image.setGeometry(0,0,200,200)
        self.image.move(0,0)
        '''

        #self.setCentralWidget(centralWidget)
        self.grouped=QWidget()
        self.grouped.setMaximumSize(690, 120)
        
        x=QGridLayout()
        x.setAlignment(QtCore.Qt.AlignTop)
        y2.setAlignment(QtCore.Qt.AlignBottom)
        
        self.trash=Laabel(self)
        #self.trash.setMaximumHeight(130)
        self.trash.setMaximumWidth(70)
        x.addWidget(self.trash,0,3)
        #x.setSpacing(10)
        #x.addWidget(QWidget)
        self.filebutton=QPushButton('Select Files')
        self.del_=QPushButton('Delete')
        #self.tab_=QPushButton('Tab')
        self.cache=windowOverlay(str="1")
        self.cache.setMinimumSize(400, 500)
        self.cache.setVisible(False)

        #self.l.addWidget(self.filebutton,0,1)
        #self.filebutton.setMaximumWidth(180)
        #self.filebutton.setMinimumHeight(130)
        #self.filebutton.setMinimumWidth(160)
        
        self.filebutton.clicked.connect(self.openfile)
        x.addWidget(self.filebutton,0,2)
        
        #self.del_.setMaximumWidth(160)
        self.del_.setMaximumWidth(120)
        #self.del_.setMinimumHeight(130)
        
        self.del_.setCursor(QtCore.Qt.PointingHandCursor)
        self.del_.clicked.connect(self.delete_and_drawagain)
        #x.addWidget(self.tab_,0,4)
        x.addWidget(self.del_,0,4)
        self.del_.hide()
        
        s1=QGridLayout()
        s1.setAlignment(QtCore.Qt.AlignLeft)
        self.run_=QPushButton('Run')
        #self.run_.setMaximumWidth(160)
        #self.run_.setMinimumWidth(180)
        #self.run_.setMinimumHeight(130)
        self.run_.setCursor(QtCore.Qt.PointingHandCursor)
        self.run_.clicked.connect(self.run)
        
        #self.del_.setCursor(QtCore.Qt.PointingHandCursor)
        x.addWidget(self.run_,0,0)
    
        
        
        self.settings_panel=QWidget()
        #self.settings_panel.setMaximumHeight(80)
        '''self.settings_panel.setAutoFillBackground(True)
        self.settings_panel.setMinimumHeight(130)
        self.settings_panel.setStyleSheet(""" background-color:red;""")
        self.settings_panel.setLayout(s1)
        y1.addWidget(self.settings_panel,2,0)'''
        
        y2.addWidget(self.cache,0,0)
        y2.addWidget(self.finaltable,1,0)
        self.finaltable.setMaximumHeight(133)
        
        self.final_preview=QLabel(self)
        y2.addWidget(self.final_preview,0,0)
        self.final_preview.setVisible(False)
        
        self.dirbutton=QPushButton('Select Directory')
        #self.l.addWidget(self.dirbutton,2,0)
        #self.dirbutton.setMaximumWidth(200)
        #self.dirbutton.setMinimumHeight(130)
        #self.dirbutton.setMinimumWidth(180)
        self.filebutton.setCursor(QtCore.Qt.PointingHandCursor)
        self.dirbutton.setCursor(QtCore.Qt.PointingHandCursor)
        
        
        x.addWidget(self.dirbutton,0,1)
        self.grouped.setLayout(x)
        self.preview.setStyleSheet(""" background-color:white;""")
        
        y1.addWidget(self.grouped,3,0)
        self.grouped_1.setLayout(y1)
        self.l.addWidget(self.grouped_1,0,0)
        
        self.grouped_2.setLayout(y2)
        self.l.addWidget(self.grouped_2,0,1)
        self.run_.setMaximumWidth(120)
        self.dirbutton.setMaximumWidth(180)
        self.filebutton.setMaximumWidth(150)
        self.newthread=MyThread(self)
        self.dirbutton.clicked.connect(self.opendir)
        self.connect(self.tableWidget, QtCore.SIGNAL('preview'),self.preview_shot)
        self.connect(self.finaltable, QtCore.SIGNAL('final_preview'),self.final_preview_shot)
        self.connect(self.tableWidget, QtCore.SIGNAL("dropped"), self.pictureDropped)
        self.connect(self.tableWidget,QtCore.SIGNAL('bhak'),self.delete_and_drawagain)
        self.connect(self.trash,QtCore.SIGNAL('bhak'),self.delete_and_drawagain)
        self.connect(self.trash,QtCore.SIGNAL('selected_index'),self.get_selected_index)
        self.connect(self.tableWidget, QtCore.SIGNAL('show_delete'),self.show_delete)
        from functools import partial
        self.connect(self.newthread,QtCore.SIGNAL('finished'),self.showfirst)
        self.setLayout(self.l)
        self.row=-1
        
        #QtGui.QShortcut(QtGui.QKeySequence("Ctrl+F"), self, self.openfile)
        #QtGui.QShortcut(QtGui.QKeySequence("Ctrl+D"), self, self.opendir)
        
        #QtGui.QShortcut(QtGui.QKeySequence("del"), self, self.delete_and_drawagain)
        
        
        
        palette=QPalette(self.grouped.palette())
        palette.setColor(palette.Background, Qt.transparent)
        self.grouped.setPalette(palette)
        
        
        palette=QPalette(self.grouped_2.palette())
        palette.setColor(palette.Background, Qt.transparent)
        self.grouped_2.setPalette(palette)
        self.thresholdpath=''
       # self.tab_.connect(self.newtab)
   # def newtab(self):
       # self.emit('newtab')
    def showfirst(self,finallinks):
        for x in finallinks:
            self.finaltable.links.append(x)
            self.pictureDropped_infinaltable()
        print('shoooooooooooowfiiiiiiiiiiiiiii')
        self.final_preview_shot(0, 0)
    def animation(self):
        self.animdialog=QDialog(self)
        self.button1 = QGraphicsRectWidget(self.tableWidget.links)
        self.button2 = QGraphicsRectWidget(self.tableWidget.links)
        self.button3 = QGraphicsRectWidget(self.tableWidget.links)
        self.button4 = QGraphicsRectWidget(self.tableWidget.links)
        self.button2.setZValue(1)
        self.button3.setZValue(2)
        self.button4.setZValue(3)
        
        print('startanimaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
    
        self.scene = QtGui.QGraphicsScene(0, 0, SCREENSIZE, SCREENSIZE,parent=self.animdialog)
        self.scene.setBackgroundBrush(QtCore.Qt.black)
        self.scene.addItem(self.button1)
        self.scene.addItem(self.button2)
        self.scene.addItem(self.button3)
        self.scene.addItem(self.button4)
        
         
        self.window = QtGui.QGraphicsView(self.scene,parent=self.animdialog)
        #self.window = QtGui.QGraphicsView(self.scene)
        self.window.setFrameStyle(0)
        self.window.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.window.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.window.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.machine = QtCore.QStateMachine()

        self.group = QtCore.QState()
        self.timer = QtCore.QTimer()
        self.timer.setInterval(1250)
        self.timer.setSingleShot(True)
        self.group.entered.connect(self.timer.start)

        state1 = createGeometryState(self.button1, QtCore.QRect(BLOCKSIZE*2, 0, BLOCKSIZE, BLOCKSIZE),
            self.button2, QtCore.QRect(BLOCKSIZE*3, 0, BLOCKSIZE, BLOCKSIZE),
            self.button3, QtCore.QRect(SCREENSIZE-BLOCKSIZE*2, 0, BLOCKSIZE, BLOCKSIZE),
            self.button4, QtCore.QRect(SCREENSIZE-BLOCKSIZE, 0, BLOCKSIZE, BLOCKSIZE), self.group)

        state2 = createGeometryState(self.button1, QtCore.QRect(SCREENSIZE-BLOCKSIZE,BLOCKSIZE*2, BLOCKSIZE, BLOCKSIZE),
            self.button2, QtCore.QRect(SCREENSIZE-BLOCKSIZE, BLOCKSIZE*3, BLOCKSIZE, BLOCKSIZE),
            self.button3, QtCore.QRect(SCREENSIZE-BLOCKSIZE, SCREENSIZE-BLOCKSIZE*2, BLOCKSIZE, BLOCKSIZE),
            self.button4, QtCore.QRect(SCREENSIZE-BLOCKSIZE, SCREENSIZE-BLOCKSIZE, BLOCKSIZE, BLOCKSIZE), self.group)

        state3 = createGeometryState(self.button1, QtCore.QRect(BLOCKSIZE*3, SCREENSIZE-BLOCKSIZE, BLOCKSIZE, BLOCKSIZE),
            self.button2, QtCore.QRect(BLOCKSIZE*2, SCREENSIZE-BLOCKSIZE, BLOCKSIZE, BLOCKSIZE),
            self.button3, QtCore.QRect(BLOCKSIZE, SCREENSIZE-BLOCKSIZE, BLOCKSIZE, BLOCKSIZE),
            self.button4, QtCore.QRect(0, SCREENSIZE-BLOCKSIZE, BLOCKSIZE, BLOCKSIZE), self.group)

        state4 = createGeometryState(self.button1, QtCore.QRect(0, BLOCKSIZE*3, BLOCKSIZE, BLOCKSIZE),
            self.button2, QtCore.QRect(0, BLOCKSIZE*2, BLOCKSIZE, BLOCKSIZE),
            self.button3, QtCore.QRect(0, BLOCKSIZE, BLOCKSIZE, BLOCKSIZE),
            self.button4, QtCore.QRect(0, 0, BLOCKSIZE, BLOCKSIZE), self.group)

        state5 = createGeometryState(self.button1, QtCore.QRect( BLOCKSIZE*2,BLOCKSIZE*2, BLOCKSIZE, BLOCKSIZE),
            self.button2, QtCore.QRect(BLOCKSIZE*3, BLOCKSIZE*2, BLOCKSIZE, BLOCKSIZE),
            self.button3, QtCore.QRect(BLOCKSIZE*2, BLOCKSIZE*3, BLOCKSIZE, BLOCKSIZE),
            self.button4, QtCore.QRect(BLOCKSIZE*3, BLOCKSIZE*3, BLOCKSIZE, BLOCKSIZE), self.group)

        state6 = createGeometryState(self.button1, QtCore.QRect(BLOCKSIZE, BLOCKSIZE, BLOCKSIZE, BLOCKSIZE),
            self.button2, QtCore.QRect(SCREENSIZE-2*BLOCKSIZE, BLOCKSIZE, BLOCKSIZE,BLOCKSIZE),
            self.button3, QtCore.QRect(BLOCKSIZE, SCREENSIZE-2*BLOCKSIZE, BLOCKSIZE, BLOCKSIZE),
            self.button4, QtCore.QRect(SCREENSIZE-2*BLOCKSIZE, SCREENSIZE-2*BLOCKSIZE, BLOCKSIZE, BLOCKSIZE), self.group)

        state7 = createGeometryState(self.button1, QtCore.QRect(0, 0, BLOCKSIZE, BLOCKSIZE),
            self.button2, QtCore.QRect(SCREENSIZE-BLOCKSIZE, 0, BLOCKSIZE, BLOCKSIZE),
            self.button3, QtCore.QRect(0, SCREENSIZE-BLOCKSIZE, BLOCKSIZE, BLOCKSIZE),
            self.button4, QtCore.QRect(SCREENSIZE-BLOCKSIZE, SCREENSIZE-BLOCKSIZE, BLOCKSIZE, BLOCKSIZE), self.group)

        self.group.setInitialState(state1)

        self.animationGroup = QtCore.QParallelAnimationGroup()
        self.anim = QtCore.QPropertyAnimation(self.button4, 'geometry')
        self.anim.setDuration(1000)
        self.anim.setEasingCurve(QtCore.QEasingCurve.OutElastic)
        self.animationGroup.addAnimation(self.anim)

        self.subGroup = QtCore.QSequentialAnimationGroup(self.animationGroup)
        self.subGroup.addPause(100)
        self.anim = QtCore.QPropertyAnimation(self.button3, 'geometry')
        self.anim.setDuration(1000)
        self.anim.setEasingCurve(QtCore.QEasingCurve.OutElastic)
        self.subGroup.addAnimation(self.anim)

        self.subGroup = QtCore.QSequentialAnimationGroup(self.animationGroup)
        self.subGroup.addPause(150)
        self.anim = QtCore.QPropertyAnimation(self.button2, 'geometry')
        self.anim.setDuration(1000)
        self.anim.setEasingCurve(QtCore.QEasingCurve.OutElastic)
        self.subGroup.addAnimation(self.anim)

        self.subGroup = QtCore.QSequentialAnimationGroup(self.animationGroup)
        self.subGroup.addPause(200)
        self.anim = QtCore.QPropertyAnimation(self.button1, 'geometry')
        self.anim.setDuration(1000)
        self.anim.setEasingCurve(QtCore.QEasingCurve.OutElastic)
        self.subGroup.addAnimation(self.anim)

        self.stateSwitcher = StateSwitcher(self.machine)
        self.group.addTransition(self.timer.timeout, self.stateSwitcher)
        self.stateSwitcher.addState(state1, self.animationGroup)
        self.stateSwitcher.addState(state2, self.animationGroup)
        self.stateSwitcher.addState(state3, self.animationGroup)
        self.stateSwitcher.addState(state4, self.animationGroup)
        self.stateSwitcher.addState(state5, self.animationGroup)
        self.stateSwitcher.addState(state6, self.animationGroup)
        self.stateSwitcher.addState(state7, self.animationGroup)

        self.machine.addState(self.group)
        self.machine.setInitialState(self.group)
        
        
    def startanimation(self):
        self.machine.start()
    
        self.window.resize(SCREENSIZE, SCREENSIZE)
        self.window.show()
        

        QtCore.qsrand(QtCore.QTime(0, 0, 0).secsTo(QtCore.QTime.currentTime()))
        
        '''
        while True and self.animationrunning:
            QApplication.processEvents(QEventLoop.ExcludeUserInputEvents)
        '''
        import sys
        self.animdialog.move(10,10)
        self.animdialog.setWindowFlags(Qt.FramelessWindowHint)
        self.animdialog.resize(SCREENSIZE+40,SCREENSIZE+40)

        #self.animdialog.setWindowFlags(Qt.Popup)
        self.animdialog.exec_()

    def clearfinal(self):
        for x in reversed(range(self.finaltable.rowCount())):
            print('remoooooooooving ',x)
            self.finaltable.removeRow(x)
    def on_thread_finished(self,thread,finallinks):
        '''
        pixmap=QPixmap(finallinks[0])
        self.finalimage.setPixmap(pixmap)
        self.finalimage.show()
        self.y2.addWidget(self.finalimage,2,0)
        '''
        self.grouped_1.show()
        print('finaaaaaaaal',finallinks)
        self.cache.setVisible(False)
        self.animationrunning=False
        self.window.hide()
        self.animdialog.close()

    def run(self):
        #self.grouped_1.setVisible(False)

        #self.newthread=MyThread(self)
    
        
        if self.thresholdpath=='':
            self.p=QMessageBox()
            self.p.setText('Input Threshold')
            self.p.setDetailedText('Input Threshold image for thresholding')
            self.p.show()
            return
        self.finaltable.links=[]
        self.finaltable.setRowCount(0)
        for i in reversed(range(self.finaltable.rowCount())):
            self.finaltable.removeRow(i)
        self.finaltable.clear()
        self.final_preview.hide()    
        self.newthread.start()
        self.animationrunning=True
        for i in reversed(range(self.finaltable.rowCount())):
            self.finaltable.removeRow(i)
        self.cache.overlay.str=str(len(self.tableWidget.links)-1)
        self.cache.setVisible(True)
        self.grouped_1.hide()
        #self.grouped_1.lower()
        self.l.setAlignment(Qt.AlignRight)
        self.clearfinal()
        #FROM HERE START COMMENTING
        self.animation()
        import threading
        animthread=threading.Thread(target=self.startanimation())
        animthread.start()
        #END COMMENT HERE
        print('ruuuuuuuuuuuuun')

        
    

    def show_delete(self,bo):
        if bo:
            self.del_.show() 
        else:
            self.del_.hide()
    def mouseMoveEvent(self, event):
        print('mouuuuuuuuuuuseeeeeeeeee')
        
        
    def get_selected_index(self):
        self.trash.sel_index=self.tableWidget.selected_index

    def preview_shot(self,row,column):
        if row==-1 or column==-1:
            self.preview.clear()
            return
        p=QPixmap()
        if row*IMAGES_PER_ROW+column>=len(self.tableWidget.links):
            return
        self.curr_path=self.tableWidget.links[row*IMAGES_PER_ROW+column]
        p.load(self.tableWidget.links[row*IMAGES_PER_ROW+column])
        if p.height()>p.width():
            p=p.scaledToHeight(300)
        else:
            p=p.scaledToWidth(300)
        self.preview.setPixmap(p)

    def final_preview_shot(self,row,column):

        if row==-1 or column==-1:
            self.preview.clear()
            return
        self.cache.setVisible(False)
        self.final_preview.setVisible(True)
        if row*IMAGES_PER_ROW+column>=len(self.finaltable.links):
            return
        self.curr_path=self.finaltable.links[row*IMAGES_PER_ROW+column]
        p=QPixmap(self.curr_path)
        if p.height()>p.width():
            p=p.scaledToHeight(500)
        else:
            p=p.scaledToWidth(500)
        self.final_preview.setPixmap(p)




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
                if path in self.tableWidget.links:
                    return
                self.tableWidget.links.append(path)
                self.pictureDropped()
                return
       
           
            
        if os.path.isdir(path):
            for f in glob.glob(os.path.join(path,'*')):
                self.append_files_recursively(f)
            return
    def openfile(self):
        x=QFileDialog(self,"Select Directory","C:\\")
        
        
        
        f=x.getOpenFileNames(filter='*.bmp *.gif *.ico *.jpeg *.jpg  *.mng  *.pbm  *.pgm  *.png  *.ppm  *.svg  *.svgz  *.tga  *.tif  *.tiff  *.xbm  *.xpm')
        for i in f:
            self.append_files_recursively(str(i))
            
    def openfile_1(self):
        x=QFileDialog(self,"Select Directory","C:\\")
        
        
        
        f=x.getOpenFileName(filter='*.bmp *.gif *.ico *.jpeg *.jpg  *.mng  *.pbm  *.pgm  *.png  *.ppm  *.svg  *.svgz  *.tga  *.tif  *.tiff  *.xbm  *.xpm')
        self.thresholdpath=str(f)  
    
    def opendir(self):
        fi = str(QFileDialog.getExistingDirectory(self, "Select Directory","C:\\"))
        self.append_files_recursively(str(fi))
        
    def pictureDropped_infinaltable(self):
            #print("afasf")
            
            print(self.finaltable.links[-1])

            rowCount=len(self.finaltable.links)//IMAGES_PER_ROW
            if len(self.finaltable.links)%IMAGES_PER_ROW: rowCount+=1
            self.finaltable.setRowCount(rowCount)
            
            col=(len(self.finaltable.links)-1)%IMAGES_PER_ROW
            if not col: self.row+=1
            #print(self.row,col)           
            self.row=rowCount-1
            self.finaltable.addPicture(self.row,col,self.finaltable.links[-1])     

        
        
           
    def pictureDropped(self):
            #print("afasf")
            
            print(self.tableWidget.links[-1])

            rowCount=len(self.tableWidget.links)//IMAGES_PER_ROW
            if len(self.tableWidget.links)%IMAGES_PER_ROW: rowCount+=1
            self.tableWidget.setRowCount(rowCount)
            
            col=(len(self.tableWidget.links)-1)%IMAGES_PER_ROW
            if not col: self.row+=1
            #print(self.row,col)           
            self.row=rowCount-1
            self.tableWidget.addPicture(self.row,col,self.tableWidget.links[-1])
            
    def delete_and_drawagain(self):
        #winsound.PlaySound('papercrumble.wav' , winsound.SND_FILENAME) 
        #winsound.PlaySound('beep.wav' , winsound.SND_FILENAME)
        self.tableWidget.dragging_cells=False
        lowest=100000000
        lowest_row=0
        print((self.tableWidget.links))
        print "aaaaa"
        indexes=[]
        for tick in reversed(self.tableWidget.ticks):
            print('removing tick',tick.row,tick.column)
            tick.deleteLater()
            tick.destroy()
            self.tableWidget.ticks.remove(tick)
        for x in self.tableWidget.selected_index:
            index=x.row()*IMAGES_PER_ROW+x.column()
            indexes.append(index)
            #print(index)
            if index < lowest:
                lowest=index
                lowest_row=x.row()
        indexes.sort()
        print(indexes)
        self.tableWidget.selected_index=[]
        self.show_delete(False)
        for i in reversed(range(len(indexes))):
            if self.tableWidget.links.pop(indexes[i])==self.curr_path:
                self.preview.clear()
        for i in reversed(range(lowest_row,self.tableWidget.rowCount())):
            self.tableWidget.removeRow(i)
        print(range(self.tableWidget.rowCount()*IMAGES_PER_ROW,len(self.tableWidget.links)))
        for i in range(self.tableWidget.rowCount()*IMAGES_PER_ROW,len(self.tableWidget.links)):
            rowCount=(i+1)//IMAGES_PER_ROW
            if (i+1)%IMAGES_PER_ROW: rowCount+=1
            self.tableWidget.setRowCount(rowCount)
            col=(i)%IMAGES_PER_ROW
            self.row=rowCount-1
            print(self.row,col,self.tableWidget.rowCount())
            self.tableWidget.addPicture(self.row, col, self.tableWidget.links[i])
        
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






class TabContainer(QtGui.QWidget):
  def __init__(self):
    super(TabContainer, self).__init__()
    self.initUI()
    QtGui.QShortcut(QtGui.QKeySequence("Ctrl+Q"), self, self.close)
    QtGui.QShortcut(QtGui.QKeySequence("Ctrl+T"), self, self.add_page)
    QtGui.QShortcut(QtGui.QKeySequence("Ctrl+W"), self, self.closeTab_1)
    

  def initUI(self):
    #self.setGeometry( 150, 150, 650, 350)
    self.tabwidget = QtGui.QTabWidget(self)
    self.tabwidget.setTabPosition(QtGui.QTabWidget.West)
   # self.tabwidget.setTabShape(QtGui.QTabWidget.Triangular)
    #QtCore.QObject.connect(self, QtCore.SIGNAL('tabCloseRequested(int)'), self.closeTab)
    self.connect(self.tabwidget, QtCore.SIGNAL('tabCloseRequested (int)'),self.closeTab)
    self.tabwidget.setTabsClosable(True)
    #self.tabwidget.removeTab(1)
    self.tabwidget.setAutoFillBackground(False)
    self.tabwidget.setMovable(True)
    #self.tabwidget.setTabShape(QtGui.QTabWidget.Rounded)
    vbox = QtGui.QVBoxLayout()
    self.tabwidget.setDocumentMode(True)
    vbox.addWidget(self.tabwidget)
    self.setLayout(vbox)
    self.pages = []
    self.add_page()
    self.show()
    
  def closeTab(self, index):
      
      #self.tabWidget.widget(index).close()
      if self.tabwidget.count()== 1:
          self.close()
      #self.pages.remove(self.tabwidget.currentWidget())
      self.tabwidget.removeTab(index)
      
      self.tabwidget.destroy(index)
      print len(self.pages)
        
  def closeTab_1(self):
      
      index=self.tabwidget.currentIndex()
      if self.tabwidget.count()== 1:
          self.close()
      
      self.pages.remove(self.tabwidget.currentWidget())
      self.tabwidget.destroy(index)
      self.tabwidget.removeTab(index)
      print len(self.pages)
        

  def create_page(self, *contents):
    page = QtGui.QWidget()
    vbox = QtGui.QVBoxLayout()
    
    for c in contents:
        vbox.addWidget(c)

    page.setLayout(vbox)
    return page



  '''def create_new_page_button(self):
    btn = QtGui.QPushButton('Create a new page!')
    btn.setBaseSize(50, 50)
    btn.setMinimumHeight(30)
    btn.setCursor(QtCore.Qt.PointingHandCursor)
    
    #btn.setStyleSheet('QPushButton {     border: 2px solid #8f8f91;     border-radius: 6px;     background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,                                       stop: 0 #f6f7fa, stop: 1 #dadbde);     min-width: 80px; }')
    btn.clicked.connect(self.add_page)
    
    return btn'''

  def add_page(self):
    #self.pages.append( self.create_page( MainWindow() ) )
    self.pages.append(MainWindow())
    self.tabwidget.addTab( self.pages[-1] , 'Page %s' % len(self.pages) )
    self.tabwidget.setCurrentIndex( len(self.pages)-1 )


class SplashScreen(QtGui.QWidget):
    def __init__(self, pixmap):
        QtGui.QWidget.__init__(self)
        self._pixmap = pixmap
        self._message = QtCore.QString()
        self._color = QtGui.QColor.black
        self._alignment = QtCore.Qt.AlignLeft
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint |
                            QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setFixedSize(self._pixmap.size())
        self.setMask(self._pixmap.mask())

    def clearMessage(self):
        self._message.clear()
        self.repaint()

    def showMessage(self, message, alignment=QtCore.Qt.AlignLeft,
                                   color=QtGui.QColor.black):
        self._message = QtCore.QString(message)
        self._alignment = alignment
        self._color = color
        self.repaint()

    def paintEvent(self, event):
        textbox = QtCore.QRect(self.rect())
        textbox.setRect(textbox.x() + 5, textbox.y() + 5,
                        textbox.width() - 10, textbox.height() - 10)
        painter = QtGui.QPainter(self)
        painter.drawPixmap(self.rect(), self._pixmap)
        painter.setPen(QtGui.QColor(self._color))
        painter.drawText(textbox, self._alignment, self._message)

    def mousePressEvent(self, event):
        self.hide()

def show_splash(path):
    image = QtGui.QPixmap(path)
    splash = SplashScreen(image)
    font = QtGui.QFont(splash.font())
    font.setPointSize(font.pointSize() + 5)
    splash.setFont(font)
    splash.show()
    QtGui.QApplication.processEvents()
    for count in range(1, 100):
        splash.showMessage(splash.tr('Processing %1...').arg(count),
                           QtCore.Qt.AlignBottom+20, QtCore.Qt.black)
        QtGui.QApplication.processEvents()
        QtCore.QThread.msleep(15)
    splash.hide()
    splash.close()

class overlay(QWidget):    
    def __init__(self, parent=None,str='0'):        
        super(overlay, self).__init__(parent)

        palette = QPalette(self.palette())
        palette.setColor(palette.Background, Qt.transparent)
        self.setPalette(palette)
        self.str=str

    def paintEvent(self, event):        
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        #painter.eraseRect(self.width()/2-60, self.height()/2-62,100,105)
        font = painter.font() 
        '''
        font.setPointSize ( 38 )
        painter.setFont(font)
        if A/10:
            painter.drawText(self.width()/2-150, self.height()/2+234,'Please Wait..')
            A=A+1
        else:
            painter.drawText(self.width()/2-150, self.height()/2+234,'Please Wait...')
            A=A+1
            import time
            print(A)
        #painter.fillRect(event.rect(), QBrush(QColor(255, 255, 255, 127)))
        '''
        font.setPointSize ( 98 )
        painter.setFont(font)
        painter.drawText(self.width()/2-50, self.height()/2+34,self.str)
    def updatenumber(self,number):
        print('upddddaaaaaaaaaaaateeeeeeeee',number)
        self.str=str(number)
    '''
    def showimage(self,path):
        painter=QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        pixmap=QPixmap(path)
        pixmap=pixmap.scaled(self.width(), self.height())
        painter.drawPixmap(self.rect(),pixmap, self.rect())
    '''
        #//font.setWeight(QFot::DemiBold);
        #painter.drawLine(self.width()/8, self.height()/8, 7*self.width()/8, 7*self.height()/8)
        #painter.drawLine(self.width()/8, 7*self.height()/8, 7*self.width()/8, self.height()/8)
        #painter.setPen(QPen(Qt.NoPen))        
class windowOverlay(QWidget):
    def __init__(self, parent=None,str='1'):
        super(windowOverlay, self).__init__(parent)
        self.str=str
        self.movie = QMovie('a1.gif', QByteArray(), self)
        #self.setWindowTitle(title)
        self.movie_screen = QLabel()
        # Make label fit the gif
        self.movie_screen.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.movie_screen.setAlignment(Qt.AlignCenter)
        # Create the layout
        '''main_layout = QVBoxLayout()
        main_layout.addWidget(self.movie_screen)
        main_layout.addWidget(self.la_)
        self.setLayout(main_layout)'''
        # Add the QMovie object to the label
        self.verticalLayout = QHBoxLayout(self)
        self.verticalLayout.addWidget(self.movie_screen)
        
        self.stoploading=True
        self.movie.setCacheMode(QMovie.CacheAll)
        self.movie.setSpeed(100)
        self.movie_screen.setMovie(self.movie)
        self.movie.start()
        self.overlay = overlay(self.movie_screen,self.str)
        #self.overlay.hide()

    def resizeEvent(self, event):    
        self.overlay.resize(event.size())
        event.accept()

if __name__=="__main__":
    from sys import argv, exit

    a=QtGui.QApplication(sys.argv)
    show_splash('splash.png')
    m=TabContainer()
    
    m.setStyleSheet("""

   
QWidget
{
background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                       stop: 0 #E0E0E0, stop: 1 #FFFFFF);
}
TableWidget{
background-color:green;


}
QTabWidget
{
    outline: 0;
}
FinalTable
{
border:0px;
}
QPushButton {
    
    background-color:#79bbff;
    border-radius:6px;
    border:1px solid #84bbf3;

    
    color:#ffffff;
    font-family:arial;
    font-size:15px;
    font-weight:bold;
    padding:6px 24px;
    text-decoration:none;
}
QPushButton:hover {
    background-color:#378de5;
}
QPushButton:active {
    position:relative;
    top:1px;
}


""")
    a.installEventFilter(m)
    m.showMaximized()
    m.raise_()
    exit(a.exec_())
