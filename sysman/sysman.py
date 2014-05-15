import sys, os, time, threading
from PyQt4 import QtCore, QtGui

from sysmanui import Ui_Form

exists = True

class MyForm(QtGui.QMainWindow):
    def __init__(self, parent=None):	
        
        # preload
        
        QtGui.QWidget.__init__(self, parent)
        
        cpuinfo = getCPUInfo(self)
        meminfo = getMemoryInfo(self)
        cpuActivity = getCPUActivity(self)
        
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        updateStatus(self, cpuinfo, meminfo, cpuActivity)
        
        # update via thread
        
        StatusUpdaterThread = threading.Thread(target=StatusUpdater, name="sysman-status", args=(self,))
        StatusUpdaterThread.daemon = True
        StatusUpdaterThread.start()             
        
        
def getCPUInfo(self):
        cpuinfo_raw = os.popen("cat /proc/cpuinfo").read()
				
		# cpu infos
        cpuinfo_raw = cpuinfo_raw.replace("\t", "")

        cpuinfo = list()
        cpuinfo_raw = cpuinfo_raw.split("\n")

        
        for cpu in cpuinfo_raw:
         temp = cpu.split(":")
         try:
          cpuinfo.append(temp[1][1:])
         except IndexError:
          pass
        
        return cpuinfo
        
        
def getMemoryInfo(self):
        meminfo1_raw = os.popen("free | grep Mem:").read()
        meminfo2_raw = os.popen("cat /proc/meminfo").read()
        
        meminfo = list()
        meminfo2 = list()
        
        temp = meminfo1_raw.split(" ")    

        
        # total
        meminfo.append(temp[7])
        # used
        meminfo.append(temp[12])
        # free
        meminfo.append(temp[16])
        
        meminfo2_raw = meminfo2_raw.replace("\t", "")

        temp = list()
        meminfo2_raw = meminfo2_raw.split("\n")
        
        for mem in meminfo2_raw:
         temp = mem.split(":")
         try:
          meminfo2.append(temp[1][1:])
         except IndexError:
          pass       
        #swap total
        meminfo.append(meminfo2[13].replace(" ", ""))  
        
        #swap free
        meminfo.append(meminfo2[14].replace(" ", ""))
        
        #swap used (?)
        meminfo.append(meminfo2[4].replace(" ", ""))
                 
        return meminfo
   

def getCPUActivity(self):
        cpuActivity = os.popen('top -d 1 -b -n2 | grep "Cpu(s)"|tail -n 1 | awk \'{print $2 + $4}\'').read()
        return cpuActivity


def updateStatus(self, cpuinfo, meminfo, cpuActivity):
		
			# model info
			self.ui.cpumodel.setText(cpuinfo[4])
			
			# cpu frequency
			self.ui.cpufreq.setText(cpuinfo[6]+ " MHz")
			
			# cpu cores
			self.ui.cpucores.setText(cpuinfo[11])       

			# cpu cache
			self.ui.cpucache.setText(cpuinfo[7])  
			
			# cpu instructions (flags)
			self.ui.flags.setText(cpuinfo[18])  
			
			
			# -------------------
			
			# memory total
			self.ui.memtotal.setText(meminfo[0]+"kB")  
			
			# memory free
			self.ui.memfree.setText(meminfo[2]+"kB")  

			# memory used
			self.ui.memused.setText(meminfo[1]+"kB")  
			
			# swap total
			self.ui.swaptotal.setText(meminfo[3])  
			
			# swap free
			self.ui.swapfree.setText(meminfo[4])  
			
			# swap used
			self.ui.swapused.setText(meminfo[5])
			
			# aktywnosc procesora (wykres)
			self.ui.progressBar.setProperty("value", int(getCPUActivity(self)))
			
			# dostepna pamiec RAM (wykres)
			self.ui.progressBar_2.setProperty("value", int((float(meminfo[1])/float(meminfo[0]))*100))

def StatusUpdater(self):
	global exists
	while(exists):
		updateStatus(self, getCPUInfo(self), getMemoryInfo(self), getCPUActivity(self))
		time.sleep(1)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MyForm()
    myapp.show()
    sys.exit(app.exec_())
