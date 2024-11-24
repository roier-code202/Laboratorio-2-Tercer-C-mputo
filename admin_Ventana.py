from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QMainWindow, QTableWidget, QTableWidgetItem, QWidget
from base_datos import obtener_reservas  # Importamos la función para obtener reservas desde la base de datos.

# Clase para la ventana de inicio de sesión
class VentanaLogin(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Login Administrador")  # Título de la ventana
        self.setGeometry(100, 100, 300, 150)  # Tamaño y posición de la ventana

        # Layout principal para organizar los widgets
        self.layout = QVBoxLayout()

        # Campo de usuario
        self.label_usuario = QLabel("Usuario:") 
        self.input_usuario = QLineEdit()  # Campo de texto para ingresar el usuario
        self.layout.addWidget(self.label_usuario)  
        self.layout.addWidget(self.input_usuario)

        # Campo de contraseña
        self.label_password = QLabel("Contraseña:") 
        self.input_password = QLineEdit()  # Campo de texto para ingresar la contraseña
        self.input_password.setEchoMode(QLineEdit.Password)  # Oculta los caracteres ingresados
        self.layout.addWidget(self.label_password)  # Añade la etiqueta al layout
        self.layout.addWidget(self.input_password) 

        # Botón para iniciar sesión
        self.boton_login = QPushButton("Iniciar Sesión")  # Crea un botón con texto
        self.boton_login.clicked.connect(self.verificar_credenciales)  # Conecta el botón a la función de verificación
        self.layout.addWidget(self.boton_login)  #

        self.setLayout(self.layout)  # Establece el layout principal para la ventana

    def verificar_credenciales(self):
        usuario = self.input_usuario.text()  # Obtiene el texto ingresado en el campo de usuario
        password = self.input_password.text()  # Obtiene el texto ingresado en el campo de contraseña
        if usuario == "admin" and password == "admin123":  # Verifica las credenciales
            self.accept()  # Cierra la ventana y devuelve un estado de aceptación
        else:
            QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos")  # Muestra un mensaje de error

# Clase para la ventana principal del administrador
class VentanaAdmin(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("Gestión de Reservas")  # Título de la ventana principal
        self.setGeometry(100, 100, 600, 400)  # Tamaño y posición de la ventana

        # Layout principal para organizar los widgets
        self.layout = QVBoxLayout()
        self.tabla_reservas = QTableWidget()  # Tabla para mostrar las reservas
        self.layout.addWidget(self.tabla_reservas)  # Añade la tabla al layout

        # Botón para refrescar los datos de la tabla
        self.boton_refrescar = QPushButton("Refrescar")  # Crea un botón con texto
        self.boton_refrescar.clicked.connect(self.cargar_reservas)  # Conecta el botón a la función de carga
        self.layout.addWidget(self.boton_refrescar)  # Añade el botón al layout

        # Widget central que contiene el layout principal
        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)  # Establece el widget central de la ventana

        self.cargar_reservas()  # Llama a la función para cargar las reservas al inicializar la ventana

    def cargar_reservas(self):
        reservas = obtener_reservas()  # Llama a la función para obtener los datos de la base de datos
        self.tabla_reservas.setRowCount(len(reservas))  # Establece el número de filas según la cantidad de reservas
        self.tabla_reservas.setColumnCount(7)  # Establece el número de columnas necesarias
        self.tabla_reservas.setHorizontalHeaderLabels(
            ["ID", "Nombre", "Teléfono", "Correo", "Fecha", "Capacidad", "Mesa", "Costo"])  # Etiquetas para las columnas

        # Itera sobre las reservas y las inserta en la tabla
        for row_idx, reserva in enumerate(reservas):
            for col_idx, data in enumerate(reserva):
                # Inserta cada dato en la celda correspondiente
                self.tabla_reservas.setItem(row_idx, col_idx, QTableWidgetItem(str(data)))
