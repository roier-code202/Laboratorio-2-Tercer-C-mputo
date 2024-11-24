import sys
from PyQt5.QtWidgets import QApplication
from interfaz import InterfazReservas
from base_datos import crear_base_datos

def main():
    # Crear la base de datos y la tabla si no existen
    crear_base_datos()
    # Inicializar la aplicación Qt
    app = QApplication(sys.argv)
    # Crear la interfaz de reservas
    ventana = InterfazReservas()
    # Mostrar la ventana
    ventana.show()
    # Ejecutar la aplicación
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
