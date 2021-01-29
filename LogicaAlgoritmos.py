from PyQt5 import QtWidgets, QtGui, uic
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

qt_creator_file = "ui_Algoritmos.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qt_creator_file)

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("Dibujo de primitivas en 2D")
        self.setWindowIcon(QtGui.QIcon("icono.png"))

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
        print(self.dda_datos_input)
        xi = int(self.dda_datos_input[0][0]) # El primer elemento de la primer tupla [(x1,y1)(x2,y2)]
        yi = int(self.dda_datos_input[0][1])
        xf = int(self.dda_datos_input[1][0])# El primer elemento de la segunda tupla [(x1,y1)(x2,y2)]
        yf = int(self.dda_datos_input[1][1])
        x0 = round(xi)
        y0 = round(yi)
        dx = k = (xf - xi)
        dy = yf - yi
        x = [0 for x in range(k+1)]
        y = [0 for x in range(k+1)]
        x[0] = x0
        y[0] = y0
        m =  dy / dx
        abs_m = abs(m)

        self.m.setText(str(m))
        self.abs_m.setText(str(abs_m))
        self.dx.setText(str(dx))
        self.dy.setText(str(dy))
        self.x0.setText(str(x0))
        self.y0.setText(str(y0))

        if abs_m <= 1:
            print("Pendiente menor o igual que 1: mayormente horizontal")
            y_ = [x for x in range(k+1)]
            for i in range(k):
                x[i+1] = x[i] + 1
                y[i+1] = y[i] + m
            for i in range(len(y)):
                y_[i] = round(y[i]) 
        elif abs_m > 1:
            print("Pendiente mayor que 1: mayormente vertical")

        for plot in self.groupBox.findChildren(MplCanvas):
            plot.deleteLater()

        # Se crea el plot de Matplotlib como un Widget de PyQt
        self.sc = MplCanvas(self, width=5, height=4, dpi=100)
        self.sc.axes.plot(x, y_,"o",label="Algoritmo DDA")
        self.sc.axes.plot(x,y,label="Linea original")
        # Se definen los incrementos del eje x, y
        self.sc.axes.set_xticks(range(x[0],x[-1]+1,1))
        self.sc.axes.set_yticks(range(y_[0],y_[-1]+1,1))
        # Se dibuja el grid
        self.sc.axes.grid(True)
        self.GraficaMatplot.addWidget(self.sc)
        



        

    

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()

    