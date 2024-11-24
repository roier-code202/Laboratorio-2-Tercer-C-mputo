from PyQt5.QtWidgets import QMainWindow, QLabel, QComboBox, QLineEdit, QFormLayout, QWidget, QPushButton, QVBoxLayout, QMessageBox
from base_datos import guardar_reserva

# Clase que representa la ventana de registro de pago
class VentanaPago(QMainWindow):
    def __init__(self, nombre, telefono, correo, fecha, capacidad, numero_mesa, costo, parent=None, mesas=None):
        super().__init__(parent)
        
        # Inicialización de atributos
        self.parent = parent  # Referencia a la ventana principal
        self.mesas = mesas  # Lista de mesas
        self.setWindowTitle("Registro de Pago") 
        self.setGeometry(100, 100, 400, 350)  # Configuración inicial del tamaño de la ventana

        # Guardar datos del cliente y reserva
        self.nombre = nombre
        self.telefono = telefono
        self.correo = correo
        self.fecha = fecha
        self.capacidad = capacidad
        self.numero_mesa = numero_mesa
        self.costo = costo

        # Layout principal
        self.layout = QVBoxLayout()

        # Mostrar datos del cliente y la reserva en una sola etiqueta para compactar
        self.label_datos = QLabel(f"Cliente: {self.nombre}\nTeléfono: {self.telefono}\nCorreo: {self.correo}\n"
                                  f"Fecha y Hora: {self.fecha}\nPersonas: {self.capacidad}\n"
                                  f"Mesa: {self.numero_mesa}\nTotal a Pagar: ${self.costo}")
        self.layout.addWidget(self.label_datos)

        # Sección para seleccionar el método de pago
        self.label_metodo_pago = QLabel("Selecciona el método de pago:")
        self.layout.addWidget(self.label_metodo_pago)

        # ComboBox para elegir el método de pago
        self.combo_metodo_pago = QComboBox()
        self.combo_metodo_pago.addItems(["Tarjeta de Debito/Credito", "Transferencia Bancaria"])
        self.combo_metodo_pago.currentIndexChanged.connect(self.cambiar_metodo_pago)
        self.layout.addWidget(self.combo_metodo_pago)

        # Layout para los campos dinámicos del formulario según el método de pago
        self.form_layout = QFormLayout()
        self.layout.addLayout(self.form_layout)

        # Inicializar los campos para tarjeta de débito/crédito
        self.input_numero_tarjeta = QLineEdit()
        self.input_nombre_tarjeta = QLineEdit()
        self.input_cv_tarjeta = QLineEdit()

        # Inicializar los campos para transferencia bancaria
        self.input_numero_cuenta = QLineEdit()
        self.input_banco = QLineEdit()

        # Botón para confirmar el pago
        self.boton_confirmar = QPushButton("Confirmar Pago")
        self.boton_confirmar.clicked.connect(self.confirmar_pago)
        self.layout.addWidget(self.boton_confirmar)

        # Botón para volver a la ventana de reserva
        self.boton_volver = QPushButton("Volver a Reserva")
        self.boton_volver.clicked.connect(self.volver_a_reserva)
        self.layout.addWidget(self.boton_volver)

        # Configurar el widget central
        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

        # Mostrar los campos iniciales según el método de pago seleccionado
        self.cambiar_metodo_pago()

    # Cambia los campos mostrados en el formulario según el método de pago seleccionado
    def cambiar_metodo_pago(self):
        self.limpiar_formulario()

        metodo = self.combo_metodo_pago.currentText()
        if metodo == "Tarjeta de Debito/Credito":
            # Mostrar campos de tarjeta de crédito/débito
            self.form_layout.addRow("Número de tarjeta:", self.input_numero_tarjeta)
            self.form_layout.addRow("Nombre en la tarjeta:", self.input_nombre_tarjeta)
            self.form_layout.addRow("CVV:", self.input_cv_tarjeta)
        elif metodo == "Transferencia Bancaria":
            # Mostrar campos de transferencia bancaria
            self.form_layout.addRow("Número de cuenta:", self.input_numero_cuenta)
            self.form_layout.addRow("Banco:", self.input_banco)

    # Elimina los campos actuales del formulario
    def limpiar_formulario(self):
        for i in reversed(range(self.form_layout.count())):
            self.form_layout.itemAt(i).widget().setParent(None)

    # Limpia los valores de los campos de entrada
    def limpiar_campos(self):
        self.input_numero_tarjeta.clear()
        self.input_nombre_tarjeta.clear()
        self.input_cv_tarjeta.clear()
        self.input_numero_cuenta.clear()
        self.input_banco.clear()

    # Valida y confirma el pago según el método de pago seleccionado
    def confirmar_pago(self):
        metodo = self.combo_metodo_pago.currentText()
        if metodo == "Tarjeta de Debito/Credito" and self.validar_campos_tarjeta():
            if guardar_reserva(self.nombre, self.telefono, self.correo, self.fecha, self.capacidad, self.numero_mesa, self.costo):
                self.mostrar_confirmacion("El pago ha sido confirmado exitosamente.")
                self.limpiar_campos()
                self.marcar_mesa_como_no_disponible()
                self.parent.volver_a_reserva()
            else:
                self.mostrar_error("Hubo un problema al guardar la reserva.")
        elif metodo == "Transferencia Bancaria" and self.validar_campos_transferencia():
            if guardar_reserva(self.nombre, self.telefono, self.correo, self.fecha, self.capacidad, self.numero_mesa, self.costo):
                self.mostrar_confirmacion("El pago ha sido confirmado exitosamente.")
                self.limpiar_campos()
                self.marcar_mesa_como_no_disponible()
                self.parent.volver_a_reserva()
            else:
                self.mostrar_error("Hubo un problema al guardar la reserva.")
        else:
            return

    # Valida los campos requeridos para el pago con tarjeta
    def validar_campos_tarjeta(self):
        if not self.input_numero_tarjeta.text() or not self.input_nombre_tarjeta.text() or not self.input_cv_tarjeta.text():
            self.mostrar_error("Por favor, complete todos los campos de la tarjeta.")
            return False
        return True

    # Valida los campos requeridos para la transferencia bancaria
    def validar_campos_transferencia(self):
        if not self.input_numero_cuenta.text() or not self.input_banco.text():
            self.mostrar_error("Por favor, complete todos los campos de la transferencia bancaria.")
            return False
        return True

    # Marca una mesa como no disponible en la lista de mesas
    def marcar_mesa_como_no_disponible(self):
        if self.mesas is not None:
            for mesa in self.mesas:
                if mesa["numero"] == self.numero_mesa:
                    mesa["disponible"] = False

    # Vuelve a la ventana de reserva principal
    def volver_a_reserva(self):
        self.parent.volver_a_reserva()

    # Muestra un mensaje de confirmación
    def mostrar_confirmacion(self, mensaje):
        self.mostrar_mensaje(mensaje, QMessageBox.Information)

    # Muestra un mensaje de error
    def mostrar_error(self, mensaje):
        self.mostrar_mensaje(mensaje, QMessageBox.Critical)

    # Genera una ventana emergente para mostrar mensajes
    def mostrar_mensaje(self, mensaje, tipo):
        msg_box = QMessageBox()
        msg_box.setIcon(tipo)
        msg_box.setWindowTitle("Mensaje")
        msg_box.setText(mensaje)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()
