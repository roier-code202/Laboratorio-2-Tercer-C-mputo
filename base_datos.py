import sqlite3

# Definir las mesas globalmente
mesas = [
    {"numero": 1, "capacidad": 2, "disponible": True},
    {"numero": 2, "capacidad": 4, "disponible": True},
    {"numero": 3, "capacidad": 2, "disponible": True},
    {"numero": 4, "capacidad": 6, "disponible": True},
    {"numero": 5, "capacidad": 4, "disponible": True},
    {"numero": 6, "capacidad": 2, "disponible": True},
    {"numero": 7, "capacidad": 2, "disponible": True},
    {"numero": 8, "capacidad": 4, "disponible": True},
    {"numero": 9, "capacidad": 6, "disponible": True},
    {"numero": 10, "capacidad": 6, "disponible": True},
]
# Esto es para el costo de la reservación dependiendo de la cantidad de personas.
def calcular_costo(capacidad):
    return {2:10, 4:20, 6:25}.get(capacidad, 0)  # Si la capacidad no es 2, 4 ni 6, se retorna 0 como costo por defecto

def crear_base_datos():
    # Crear la base de datos y tabla si no existen
    conexion = sqlite3.connect('restaurant.db')
    cursor = conexion.cursor()
    
    # Tabla de reservas
    cursor.execute('''CREATE TABLE IF NOT EXISTS reservas (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT,
                        telefono TEXT,
                        correo TEXT,
                        fecha TEXT,
                        capacidad INTEGER,
                        numero_mesa INTEGER,
                        costo INTEGER)''')
    conexion.commit()
    conexion.close()

def guardar_reserva(nombre, telefono, correo, fecha, capacidad, numero_mesa, costo):
    # Guardar una nueva reserva
    conexion = sqlite3.connect('restaurant.db')
    cursor = conexion.cursor()
    cursor.execute('''INSERT INTO reservas (nombre, telefono, correo, fecha, capacidad, numero_mesa, costo)
                      VALUES (?, ?, ?, ?, ?, ?, ?)''', 
                   (nombre, telefono, correo, fecha, capacidad, numero_mesa, costo))
    reserva_id = cursor.lastrowid  # Obtener el ID de la reserva recién creada
    conexion.commit()
    conexion.close()
    return reserva_id  # Devolver el ID de la reserva para asociarla al pago

def verificar_disponibilidad(fecha, capacidad):
    # Verificar si hay una mesa disponible con la capacidad adecuada
    conexion = sqlite3.connect('restaurant.db')
    cursor = conexion.cursor()
    cursor.execute("SELECT numero_mesa, capacidad FROM reservas WHERE fecha = ?", (fecha,))
    mesas_reservadas = cursor.fetchall()
    conexion.close()
    
    # Filtrar mesas disponibles con la capacidad adecuada
    todas_mesas = [mesa for mesa in mesas if mesa["capacidad"] == capacidad]
    mesas_reservadas = [(mesa[0], mesa[1]) for mesa in mesas_reservadas]  # Solo los números de mesa reservados
    mesas_disponibles = [mesa["numero"] for mesa in todas_mesas if (mesa["numero"], capacidad) not in mesas_reservadas]
    
    return mesas_disponibles[0] if mesas_disponibles else None
    
def cancelar_reserva(telefono):
    try:
        # Conectar a la base de datos
        conexion = sqlite3.connect('restaurant.db')
        cursor = conexion.cursor()

        # Buscar si hay una reserva con el teléfono proporcionado
        cursor.execute("SELECT * FROM reservas WHERE telefono = ?", (telefono,))
        reserva = cursor.fetchone()

        if reserva:
            # Si se encuentra, proceder a eliminar la reserva
            cursor.execute("DELETE FROM reservas WHERE telefono = ?", (telefono,))
            conexion.commit()  # Confirmar los cambios
            conexion.close()  # Cerrar la conexión
            return True  # Reserva cancelada con éxito
        else:
            conexion.close()  # Cerrar la conexión
            return False  # No se encontró ninguna reserva con ese teléfono
    except sqlite3.Error as e:
        # Si ocurre un error con la base de datos, mostrarlo y cerrar la conexión
        print(f"Error al interactuar con la base de datos: {e}")
        if conexion:
            conexion.close()
        return False  # Retornar False en caso de error
    
def obtener_reservas():
    conexion = sqlite3.connect('restaurant.db')
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM reservas")
    reservas = cursor.fetchall()
    conexion.close()
    return reservas
