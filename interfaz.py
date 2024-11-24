from PyQt5.QtWidgets import QMainWindow, QDialog, QWidget, QStackedWidget, QAction, QMessageBox, QVBoxLayout, QLineEdit, QLabel, QComboBox, QDateTimeEdit, QPushButton, QGroupBox, QInputDialog
from PyQt5.QtCore import QDateTime
from interfaz_pago import VentanaPago
from admin_Ventana import VentanaLogin, VentanaAdmin 
from base_datos import calcular_costo, guardar_reserva, cancelar_reserva, mesas

class InterfazReservas(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestor de Reservaciones - Restaurante") # Establece el titulo de la ventana
        self.resize(600, 400) # Define el tamaño inicial de la ventana
        self.setStyleSheet(self.obtener_estilos()) # Aplica los estilos personalizados
        self.initUI() # Inicia la interfaz de usuario

    def initUI(self):
        # Configura un widget de pila para cambiar entre paginas
        self.stacked_widget = QStackedWidget()
        self.pagina_reserva = self.crear_pagina_reserva() # Crea y agrega la pagina de reservaciones como principal
        self.stacked_widget.addWidget(self.pagina_reserva)
        # Crea un menu superior para consultar como la pagina principal
        menu_gestion = self.menuBar().addMenu("Consultar")
        ver_mesas_action = QAction("Ver Mesas Disponibles", self)
        ver_mesas_action.triggered.connect(self.mostrar_mesas_disponibles)
        menu_gestion.addAction(ver_mesas_action)
        # Opcion de acceso restringido para personal autorizado
        ver_reservas_action = QAction("Solo personal autorizado", self)
        ver_reservas_action.triggered.connect(self.abrir_ventana_admin)
        menu_gestion.addAction(ver_reservas_action)
        # Establece el widget central en la ventana principal 
        self.setCentralWidget(self.stacked_widget)

    def abrir_ventana_admin(self):
        # Abre una ventana de inicio de sesion para verificar si el usuario tiene permisos
        login_dialog = VentanaLogin()
        if login_dialog.exec_() == QDialog.Accepted:
            self.ventana_admin = VentanaAdmin()
            self.ventana_admin.show() # Muestra la ventana de administracion si se autentica correctamente

    def crear_pagina_reserva(self):
        pagina = QWidget() # Configuracion la pagina principal para realizar reservacion
        # Campos para ingresar la informacion del cliente
        self.entrada_nombre = QLineEdit()
        self.entrada_telefono = QLineEdit()
        self.entrada_correo = QLineEdit()
        # Combobox para seleccionar la capacidad de la mesa
        self.combo_capacidad = QComboBox()
        self.combo_capacidad.addItems(["2", "4", "6"])
        self.combo_capacidad.currentTextChanged.connect(self.actualizar_mesas_disponibles)
        
        self.combo_mesas = QComboBox() # Combobox para mostrar las mesas disponibles
        self.entrada_fecha = QDateTimeEdit(QDateTime.currentDateTime()) # Selector de fecha y hora para la reservacion
        self.label_costo = QLabel("Costo de la Reservación: $0")  # Etiqueta para mostrar el costo de la reservacion
        # Boton para procesar la reservacion
        boton_reservar = QPushButton("Realizar Reservación")
        boton_reservar.clicked.connect(self.procesar_reserva)
        # Para cancelar
        boton_cancelar_reserva = QPushButton("Cancelar Reservacion")
        boton_cancelar_reserva.clicked.connect(self.mostrar_cancelar_reserva)
        
        # Diseño de la pagina
        layout_principal = QVBoxLayout()
        layout_principal.addWidget(self.crear_grupo_cliente()) # Grupo para la informacion del cliente
        layout_principal.addWidget(self.crear_grupo_reserva()) # Grupo para los detalles de la reservacion
        layout_principal.addWidget(boton_reservar)
        layout_principal.addWidget(boton_cancelar_reserva)
        pagina.setLayout(layout_principal)
        
        return pagina

    def crear_grupo_cliente(self):
        # Crea un grupo para los campos de informacion del cliente
        grupo = QGroupBox("Información del Cliente")
        layout = QVBoxLayout()
        for label_text, entrada in [("Nombre:", self.entrada_nombre),
                                    ("Teléfono:", self.entrada_telefono),
                                    ("Correo:", self.entrada_correo)]:
            layout.addWidget(QLabel(label_text)) # Etiqueta descriptiva
            layout.addWidget(entrada) # Campo de entrada
        grupo.setLayout(layout)
        return grupo

    def crear_grupo_reserva(self):
        # Crea un grupo para los detalles de la reservacion
        grupo = QGroupBox("Detalles de la Reservación")
        layout = QVBoxLayout()
        for label_text, widget in [("Fecha y Hora:", self.entrada_fecha),
                                   ("Número de Personas:", self.combo_capacidad),
                                   ("Mesas Disponibles:", self.combo_mesas),
                                   ("", self.label_costo)]:
            if label_text:
                layout.addWidget(QLabel(label_text)) # Etiqueta descriptiva
            layout.addWidget(widget) # Widget relacionado
        grupo.setLayout(layout)
        return grupo

    def actualizar_mesas_disponibles(self):
        #Atualiza las mesas disponibles segun la capicidad seleccionada
        capacidad = int(self.combo_capacidad.currentText())
        mesas_disponibles = [m for m in mesas if m["capacidad"] == capacidad and m["disponible"]]
        self.combo_mesas.clear()
        self.combo_mesas.addItems([f"Mesa {m['numero']}" for m in mesas_disponibles])
        self.label_costo.setText(f"Costo de la Reservación: ${calcular_costo(capacidad)}")

    def mostrar_mesas_disponibles(self):
        # Muestra un mensaje con las mesas disponibles
        mensaje = "Mesas Disponibles:\n" + "\n".join(
            f"Mesa {m['numero']} - Capacidad: {m['capacidad']} - {'Disponible' if m['disponible'] else 'Reservada'}"
            for m in mesas)
        QMessageBox.information(self, "Mesas Disponibles", mensaje)

    def procesar_reserva(self):
        # Valida los campos e intenta realizar una reservacion
        if not all([self.entrada_nombre.text(), self.entrada_telefono.text(), self.entrada_correo.text()]):
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")
            return

        mesa_texto = self.combo_mesas.currentText()
        if not mesa_texto:
            QMessageBox.warning(self, "Error", "Seleccione una mesa disponible.")
            return

        mesa_numero = int(mesa_texto.split()[1])
        capacidad = int(self.combo_capacidad.currentText())
        costo = calcular_costo(capacidad)

        # Verifica si la mesa sigue disponible
        if not self.verificar_disponibilidad_mesa(mesa_numero):
            QMessageBox.warning(self, "Error", "La mesa seleccionada no está disponible.")
            return
        
        # Cambia a la interfaz de pago
        self.interfaz_pago = VentanaPago(self.entrada_nombre.text(), self.entrada_telefono.text(), self.entrada_correo.text(), self.entrada_fecha.dateTime().toString("yyyy-MM-dd HH:mm"), capacidad, mesa_numero, costo, parent=self, mesas=mesas)
        self.stacked_widget.addWidget(self.interfaz_pago)
        self.stacked_widget.setCurrentWidget(self.interfaz_pago)

    def verificar_disponibilidad_mesa(self, numero_mesa):
        # Verifica si una mesa especifica esta disponible
        for mesa in mesas:
            if mesa["numero"] == numero_mesa and mesa["disponible"]:
                return True
        return False

    def mostrar_cancelar_reserva(self):
        # Permite al usuario cancelar una reservacion basada en su telefono
        telefono, ok = QInputDialog.getText(self, 'Cancelar Reservacion', 'Ingrese su número de teléfono para cancelar su reservacion:')
        if ok:
            if telefono.strip() == "":
                QMessageBox.warning(self, "Error", "Por favor, ingrese un número de teléfono.")
            else:
                if cancelar_reserva(telefono):
                    QMessageBox.information(self, "Reservacion Cancelada", "La reservacion ha sido cancelada exitosamente.")
                else:
                    QMessageBox.warning(self, "Error", "No se encontró ninguna reservacion con este teléfono.")

    def limpiar_campos(self):
        # Limpia los campos 
        self.entrada_nombre.clear()
        self.entrada_telefono.clear()
        self.entrada_correo.clear()
        self.combo_capacidad.setCurrentIndex(0)
        self.combo_mesas.clear()
        self.entrada_fecha.setDateTime(QDateTime.currentDateTime())
        self.label_costo.setText("Costo de la Reservación: $0")

    def volver_a_reserva(self):
        # Vuelve a la pagina de reservaciones desde pago
        self.limpiar_campos()
        self.stacked_widget.setCurrentWidget(self.pagina_reserva)
   
    # Para este estilo nos ayudamos de cosas en linea y GPT
    def obtener_estilos(self):
        return """
            QMainWindow { background-color: #ffffff; }
            QLabel { font-family: 'Helvetica Neue', Arial, sans-serif; font-size: 15px; color: #333; margin-bottom: 5px; }
            QLineEdit, QComboBox, QDateTimeEdit {
                font-family: 'Helvetica Neue', Arial, sans-serif;
                font-size: 14px;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 8px;
                background-color: #f9f9f9;
            }
            QLineEdit:focus, QComboBox:focus, QDateTimeEdit:focus { border-color: #4CAF50; background-color: #fff; }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 12px 24px;
                border-radius: 25px;
                font-size: 14px;
                border: none;
            }
            QPushButton:hover { background-color: #45a049; }
            QGroupBox { font-family: 'Helvetica Neue', Arial, sans-serif; font-size: 16px; font-weight: bold; color: #444; border: none; margin: 20px 0; }
            QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 5px; }
            QStackedWidget { margin: 30px; }
            QMenuBar {
                background-color: #222;
                color: #fff;
                font-size: 16px;
            }
            QMenuBar::item {
                padding: 12px;
                background-color: #222;
            }
            QMenuBar::item:selected { background-color: #4CAF50; }
            QMenuBar::item:pressed { background-color: #388E3C; }
        """
