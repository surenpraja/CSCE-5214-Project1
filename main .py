from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
from dataloader import dataRetrieve

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar2QT
import numpy as np
import matplotlib.pyplot as plt

import sys

class combodemo(QWidget):
    def __init__(self, parent = None):
        super(combodemo, self).__init__(parent)
        
        layout = QGridLayout()
        
        #Combo box setup
        self.cblabel = QLabel()
        self.cblabel.setText("Select Ticker:")
        
        self.cb = QComboBox()
        self.tickerDict = {'':'', 'Apple':'AAPL', 'Microsoft':'MSFT', 'General Electric':'GE', 'IBM':'IBM', 'JP Morgan':'JPM', 'Uber':'UBER', 'Coca Cola':'KO', 'Game Stop':'GME', 'Pepsi':'PEP', 'Delta Airlines':'DAL', 'United Airlines':'UAL', 'Amazon':'AMZN', 'Walmart':'WMT', 'Alibaba':'BABA'}
        self.cb.addItems(self.tickerDict.keys())
        #self.cb.currentIndexChanged.connect(self.selectionchange)
        
        #Date pickers setup
        self.dateBegginingLabel = QLabel()
        self.dateBegginingLabel.setText("Select Historical Data Beginning Date:");
        
        self.dateBegginingEdit = QDateEdit(calendarPopup=True);
        self.dateBegginingEdit.setDate(QtCore.QDate.currentDate().addDays(-365));
        self.dateBegginingEdit.setMaximumDate(QtCore.QDate.currentDate().addDays(-365))
        
        self.dateEndLabel = QLabel()
        self.dateEndLabel.setText("Select Model End Date:")
        
        self.dateEndEdit = QDateEdit(calendarPopup=True)
        self.dateEndEdit.setDate(QtCore.QDate.currentDate())
        self.dateEndEdit.setMinimumDate(QtCore.QDate.currentDate())
        self.dateEndEdit.setMaximumDate(QtCore.QDate.currentDate().addDays(30))
        
        #Button setup
        self.actionButton = QPushButton()
        self.actionButton.setText("Run Model")
        self.actionButton.clicked.connect(self.run_model)
        
        #Graph setup
        
        #self.graphWidget = pg.PlotWidget()
        #self.graphWidget.setBackground('w')
        #self.graphWidget.showGrid(x=True, y=True)
        
        self.figure = plt.figure()
        self.graphWidget = FigureCanvas(self.figure)
        
        layout.addWidget(self.cblabel, 0, 0)
        layout.addWidget(self.cb, 0, 1)
        layout.addWidget(self.dateBegginingLabel, 0, 2)
        layout.addWidget(self.dateBegginingEdit, 0, 3)
        layout.addWidget(self.dateEndLabel, 0, 4)
        layout.addWidget(self.dateEndEdit, 0, 5)
        layout.addWidget(self.actionButton, 1, 2, 1, 2)
        layout.addWidget(self.graphWidget, 2, 0, 1, 6)
        self.setLayout(layout)
        self.setWindowTitle("My Stock Assistant")
        
    def run_model(self):
        train, valid, predictions = dataRetrieve(self.tickerDict[self.cb.currentText()], self.dateBegginingEdit.date().toPyDate(), self.dateEndEdit.date().toPyDate())
                
        #self.graphWidget.clear()
        
        #self.graphWidget.plot(train, pen=pg.mkPen(color='b', width=2))
        #self.graphWidget.plot(valid, pen=pg.mkPen(color='m', width=2))
        #self.graphWidget.plot(predictions, pen=pg.mkPen(color='r', width=2))
        #self.graphWidget.addLegend("Training Data", "Actual Values", "Predicted Values")
        
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        #ax.plot(np.arange(0, len(train)), train, 'b')
        ax.plot(train, 'b');
        #ax.plot(np.arange(len(train), len(train)+len(valid)), valid, 'm');
        ax.plot(valid, 'm');
        #ax.plot(np.arange(len(train), len(train)+len(predictions)), predictions, 'r')
        ax.plot(predictions, 'r');
        ax.set_title(self.cb.currentText()+' stock prices')
        ax.legend(['Stock Data:Training', 'Stock Data:Actual', 'Predictions'])
        ax.set_xlabel('Date')
        ax.set_ylabel('Price ($)')
        self.graphWidget.draw()

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ex = combodemo()
    ex.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()