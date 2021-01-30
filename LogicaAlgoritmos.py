from PyQt5 import QtWidgets,QtCore,QtGui,uic
from PyQt5.QtCore import Qt
import sys
import resources
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

try:
    # Include in try/except block if you're also targeting Mac/Linux
    from PyQt5.QtWinExtras import QtWin
    myappid = 'com.RotcehOdraude.Github.Algoritmos'
    QtWin.setCurrentProcessExplicitAppUserModelID(myappid)    
except ImportError:
    pass

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class DataTable:
    def __init__(self,indices,datos):
        self.indices = indices
        self.datos = datos


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data.datos[index.row()][index.column()]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data.datos)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data.datos[0])
    
    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.indices[0][section])

            if orientation == Qt.Vertical:
                return str(self._data.indices[1][section])
    


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        #self.setWindowTitle("Hello World")
        # Carga de la UI
        fileh = QtCore.QFile(':/ui/mainwindow.ui')
        fileh.open(QtCore.QFile.ReadOnly)
        uic.loadUi(fileh, self)
        fileh.close()
        self.windowTitle

        ## Variables 
        self.dda_datos_input = [(0,1),(0,1)]

        
        # Algoritmo DDA #
        self.DDA_algoritmo()


    def DDA_algoritmo(self):
        self.boton.clicked.connect(self.dda_boton_hacer_click)




    ## Definición de eventos de la interfaz gráfica
    def dda_boton_hacer_click(self):
        # Se manda a llamar cada vez que se pulsa el botón en DDA
        self.dda_datos_input = []
        self.dda_datos_input.append(tuple(self.vertice_inicial.text().split(",")))
        self.dda_datos_input.append(tuple(self.vertice_final.text().split(",")))
        xi = int(self.dda_datos_input[0][0]) # El primer elemento de la primer tupla [(x1,y1)(x2,y2)]
        yi = int(self.dda_datos_input[0][1])
        xf = int(self.dda_datos_input[1][0])# El primer elemento de la segunda tupla [(x1,y1)(x2,y2)]
        yf = int(self.dda_datos_input[1][1])
        x0 = round(xi)
        y0 = round(yi)
        dx = xf - xi
        dy = yf - yi
        m =  dy / dx
        abs_m = abs(m)

        for plot in self.groupBox.findChildren(MplCanvas):
            plot.deleteLater()

        if abs_m <= 1:
            print("Pendiente menor o igual que 1: mayormente horizontal")
            ##  Algoritmo DDA y sus variables
            k = abs(dx)
            x = [0 for x in range(k+1)]
            y = [0 for x in range(k+1)]
            x[0] = x0
            y[0] = y0
            y_ = [x for x in range(k+1)]
            for i in range(k):
                x[i+1] = x[i] + 1
                y[i+1] = y[i] + m
            for i in range(len(y)):
                y_[i] = round(y[i])

            ##  Se genera el Plot
            # Se crea el plot de Matplotlib como un Widget de PyQt
            self.sc = MplCanvas(self, width=5, height=4, dpi=100)
            self.sc.axes.plot(x, y_,"o",label="Algoritmo DDA")
            self.sc.axes.legend()
            self.sc.axes.plot(x,y,label="Linea original")
            self.sc.axes.legend()
            # Se definen los incrementos del eje x, y
            self.sc.axes.set_xticks(range(x[0],x[-1]+1,1))
            self.sc.axes.set_yticks(range(y_[0],y_[-1]+1,1))
            # Se dibuja el grid
            self.sc.axes.grid(True)
            self.GraficaMatplot.addWidget(self.sc)

            ##  Se genera la tabla con los datos
            matrix = []
            for i in range(k+1):
                matrix.append([i,x[i],y[i],y_[i]])

            contenidoTabla = DataTable([['k','xk','yk real','yk'],["it "+str(x) for x in range(k+1)]],matrix)
            model = TableModel(contenidoTabla)
            self.tablaDatos.setModel(model)
            self.tablaDatos.resizeColumnsToContents()


        elif abs_m > 1:
            print("Pendiente mayor que 1: mayormente vertical")
            ##  Algoritmo DDA y sus variables
            k = abs(dy)
            x = [0 for x in range(k+1)]
            y = [0 for x in range(k+1)]
            x[0] = x0
            y[0] = y0
            x_ = [x for x in range(k+1)]
            for i in range(k):
                x[i+1] = x[i] + (1/m)
                y[i+1] = y[i] + 1
            for i in range(len(y)):
                x_[i] = round(x[i])

            ##  Se genera el Plot
            # Se crea el plot de Matplotlib como un Widget de PyQt
            self.sc = MplCanvas(self, width=5, height=4, dpi=100)
            self.sc.axes.plot(x_, y,"o",label="Algoritmo DDA")
            self.sc.axes.legend()
            self.sc.axes.plot(x,y,label="Linea original")
            self.sc.axes.legend()
            # Se definen los incrementos del eje x, y
            self.sc.axes.set_xticks(range(x_[0],x_[-1]+1,1))
            self.sc.axes.set_yticks(range(y[0],y[-1]+1,1))
            # Se dibuja el grid
            self.sc.axes.grid(True)
            self.GraficaMatplot.addWidget(self.sc)

            ##  Se genera la tabla con los datos
            matrix = []
            for i in range(k+1):
                matrix.append([i,x_[i],x[i],y[i]])
                
            contenidoTabla = DataTable([['k','xk','xk real','yk'],["it "+str(x) for x in range(k+1)]],matrix)
            model = TableModel(contenidoTabla)
            self.tablaDatos.setModel(model)
            self.tablaDatos.resizeColumnsToContents()


        self.m.setText(str(m))
        self.abs_m.setText(str(abs_m))
        self.dx.setText(str(dx))
        self.dy.setText(str(dy))
        self.x0.setText(str(x0))
        self.y0.setText(str(y0))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(':/icons/icono.ico'))
    main = MainWindow()
    main.setWindowTitle("Dibujo de primitivas en 2D")
    main.show()
    sys.exit(app.exec_())

    




    