
from PySide import QtGui, QtCore

class Waitbar(QtCore.QThread):
   """ Main waitbar class.

Tried to make it as Matlabish as possible, but had to fake the threading.
Make sure you kill() the object before it goes out of scope to prevent a
forced shutdown message.

Sample usage: 
   $ waitBar = WaitBar("MyTitle")
   $ waitBar.update(0.15)
   $ waitBar.update(0.75)
   $ waitBar.kill()
"""
   referenceCount = 0

   def __init__(self, title='Progress ...', initialVal=0.0):

      if Waitbar.referenceCount != 0:
         raise RuntimeError("Cannot instantiate more than one waitbar in the same process.")
      Waitbar.referenceCount+=1

      QtCore.QThread.__init__(self)

      if QtGui.QApplication.instance() is None:
         app = QtGui.QApplication([''])

      self.pbarwin = ProgressWindow(title)
      self.pbarwin.show()
      self.update(initialVal)

   def run(self):
      self.exec_()

   def update(self, val):
      self.val = val
      self.pbarwin.updateBar(val)

   def kill(self):
      """ Call this before going out of scope to prevent thread kill message. """
      Waitbar.referenceCount -= 1
      self.quit()
      self.pbarwin.fin()

class ProgressWindow(QtGui.QWidget):
   """ Internal class for waitbar. """

   def __init__(self, title='Progress ...', parent=None):
      super(ProgressWindow, self).__init__(parent)

      self.progressbar = QtGui.QProgressBar()
      self.progressbar.setMinimum(0)
      self.progressbar.setMaximum(100)

      mainLayout = QtGui.QGridLayout()
      mainLayout.addWidget(self.progressbar, 0, 0)

      self.setLayout(mainLayout)
      self.setWindowTitle(title)

   def updateBar(self, value):
      self.progressbar.setValue(int(round(value*100)))

   def fin(self):
      self.hide()


def main():
   """ A little piece of test code. """
   import time

   wb = Waitbar("TestTitle ...")
   for ii in range(0, 101, 8):
      print(ii/100.0)
      wb.update(ii/100.0)
      time.sleep(1.0)

   wb.kill()

   wb2 = Waitbar("Second title ...")
   for ii in range(0, 101, 15):
      print(ii/100.0)
      wb2.update(ii/100.0)
      time.sleep(1.0)

   wb2.kill()

if __name__=='__main__':

   main()

      



        

        

