import sys

from PyQt5.QtWidgets import QDialog, QPushButton, QVBoxLayout, QApplication, QLineEdit
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class Window(QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.input = QLineEdit()
        self.input.setText('1, -1, 1, 1, -1, 1, 1, -1, -1, 1, -1, -1, 1, 1, 1, 1, 1, -1, -1, -1, -1, 1, -1, -1, 1, -1')
        # a figure instance to plot on
        self.figure = Figure()
        # self.numList = [1, -1, 1, 1, -1, 1, 1, -1, -1, 1, -1, -1, 1, 1, 1, 1, 1, -1, -1, -1, -1, 1, -1, -1, 1, -1]

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Just some button connected to `plot` method
        self.button = QPushButton('Plot')
        self.button.clicked.connect(self.plot)

        # set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.input)
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def plot(self):
        ''' plot stuff '''
        self.numList=[]
        for item in self.input.text().replace(',,', ',-1,').split(','):
            if item !='':

                self.numList.append(int(item))

        print(self.numList)
        # create an axis
        ax = self.figure.add_subplot(111)

        # discards the old graph
        ax.clear()

        # plot data
        num = len(self.numList)
        x = range(num)
        self.valueList = self.getValue()
        s = 150
        turnPoits, maxTurn, minTurn, supportLine, pressLine, trendLine = self.analyzeData()
        for trend in trendLine:
            trendStart, trendPass = trend
            rayX = range(trendStart[0], num)
            clinedK = (trendPass[1] - trendStart[1]) / 1.0 / (trendPass[0] - trendStart[0])
            if clinedK != 0:
                bias = trendStart[1] - clinedK * trendStart[0]
                rayY = [clinedK * float(rayXitem) + bias for rayXitem in rayX]
                if clinedK > 0:
                    color = '#FF6666FF'
                else:
                    color = '#66FF66FF'
                ax.plot(rayX, rayY, c=color)
        ax.scatter(x, self.valueList, s, c="xkcd:sky blue", marker='s')
        ax.plot(x, self.valueList, c='#FFFFFF2F')
        if len(supportLine) > 0:
            ax.axhline(y=supportLine[-1][1], c='g')
        if len(pressLine) > 0:
            ax.axhline(y=pressLine[-1][1], c='r')
        ax.axis('equal')
        # refresh canvas
        self.canvas.draw()

    def getValue(self):
        self.valueList = []
        for item in range(len(self.numList)):
            self.valueList.append(sum(self.numList[:item + 1]))
        return self.valueList

    def analyzeData(self):
        '''26
        [1, 0, 1, 2, 1, 2, 3, 2, 1, 2, 1, 0, 1, 2, ]'''
        turnPoits = []
        minTurn = []
        maxTurn = []
        supportLine = []
        pressLine = []
        trendLine = []
        trendStatus = None
        first = True
        num = len(self.valueList)
        for item in range(num):
            if len(turnPoits) == 2 and first:
                first = False
                trendStatus = turnPoits[-1][1] - turnPoits[-2][1]
            if item > 0 and item < num - 1:
                if len(turnPoits) > 1:
                    if trendStatus > 0:
                        if self.valueList[item] < self.valueList[item - 1]:
                            trendLine.append((minTurn[-1], (item, self.valueList[item])))
                            trendStatus = -1
                    else:
                        if self.valueList[item] > self.valueList[item - 1]:
                            trendLine.append((maxTurn[-1], (item, self.valueList[item])))
                            trendStatus = 1

                if self.valueList[item] > self.valueList[item - 1] and self.valueList[item] > self.valueList[item + 1]:

                    if len(turnPoits) > 2:
                        if False not in [self.valueList[item] >= otherMax[-1] for otherMax in maxTurn]:
                            pressLine.append((item, self.valueList[item]))
                    turnPoits.append((item, self.valueList[item]))
                    maxTurn.append((item, self.valueList[item]))
                elif self.valueList[item] < self.valueList[item - 1] and self.valueList[item] < self.valueList[
                            item + 1]:

                    if len(turnPoits) > 2:
                        if False not in [self.valueList[item] <= otherMin[-1] for otherMin in minTurn]:
                            supportLine.append((item, self.valueList[item]))
                    turnPoits.append((item, self.valueList[item]))
                    minTurn.append((item, self.valueList[item]))

        return turnPoits, maxTurn, minTurn, supportLine, pressLine, trendLine


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = Window()
    main.setWindowTitle('TrendLine')
    main.show()

    sys.exit(app.exec_())
