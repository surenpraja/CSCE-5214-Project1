from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from StockModel import build_model

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
        
        #Date pickers setup
        self.dateBegginingLabel = QLabel()
        self.dateBegginingLabel.setText("Select Historical Data Beginning Date:");
        
        self.dateBegginingEdit = QDateEdit(calendarPopup=True);
        self.dateBegginingEdit.setDate(QtCore.QDate.currentDate().addDays(-365));
        self.dateBegginingEdit.setMaximumDate(QtCore.QDate.currentDate().addDays(-365))
        
        self.dateEndLabel = QLabel()
        self.dateEndLabel.setText("Select Prediction End Date:")
        
        self.dateEndEdit = QDateEdit(calendarPopup=True)
        self.dateEndEdit.setDate(QtCore.QDate.currentDate().addDays(7))
        self.dateEndEdit.setMinimumDate(QtCore.QDate.currentDate().addDays(7))
        self.dateEndEdit.setMaximumDate(QtCore.QDate.currentDate().addDays(365))
        
        #Button setup
        self.actionButton = QPushButton()
        self.actionButton.setText("Run Model")
        self.actionButton.clicked.connect(self.run_model)
        
        #Graph setup
        
        self.figure = plt.figure()
        self.graphWidget = FigureCanvas(self.figure)
        
        #Table setup
        self.table = QTableWidget()
        
        layout.addWidget(self.cblabel, 0, 0)
        layout.addWidget(self.cb, 0, 1)
        layout.addWidget(self.dateBegginingLabel, 0, 2)
        layout.addWidget(self.dateBegginingEdit, 0, 3)
        layout.addWidget(self.dateEndLabel, 0, 4)
        layout.addWidget(self.dateEndEdit, 0, 5)
        layout.addWidget(self.actionButton, 1, 2, 1, 2)
        layout.addWidget(self.graphWidget, 2, 0, 1, 6)
        layout.addWidget(self.table, 2, 7, 1, 1)
        self.setLayout(layout)
        self.setWindowTitle("My Stock Assistant")
        
    def run_model(self):
        train, valid, predictions, data_future, rmse = build_model(self.tickerDict[self.cb.currentText()], self.dateBegginingEdit.date().toPyDate(), self.dateEndEdit.date().toPyDate())
        
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(train, 'b');
        ax.plot(valid, 'm');
        ax.plot(predictions, 'r');
        ax.set_title(self.cb.currentText()+' stock prices\nRoot Mean Square Error: $'+str(round(rmse, 2)))
        ax.legend(['Stock Data:Training', 'Stock Data:Actual', 'Predictions'])
        ax.set_xlabel('Date')
        ax.set_ylabel('Price ($)')
        self.graphWidget.draw()
        
        self.table.data = data_future
        
        self.table.setRowCount(len(data_future['Date']))
        self.table.setColumnCount(2)
        self.table.setItem(0, 0, QTableWidgetItem("Date"));
        self.table.setItem(0, 1, QTableWidgetItem("Stock Price Prediction"));
        for i in range(0, len(data_future["Date"])):
            self.table.setItem(i+1, 0, QTableWidgetItem(data_future["Date"][i].strftime("%m-%d-%y")));
            self.table.setItem(i+1, 1, QTableWidgetItem("$"+str(round(data_future["Stock Price Prediction"][i][0], 2))));
        
        

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ex = combodemo()
    ex.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()