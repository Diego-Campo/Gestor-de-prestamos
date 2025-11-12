import sqlite3

def verificar_db():
    try:
        conn = sqlite3.connect('inversiones_campo.db')
        cursor = conn.cursor()
        print("Conexión exitosa a la base de datos")
    
        print("\n=== Estructura de la tabla usuarios ===")
        cursor.execute("PRAGMA table_info(usuarios)")
        columnas = cursor.fetchall()
        for col in columnas:
            print(f"Columna: {col[1]}, Tipo: {col[2]}, NotNull: {col[3]}, Default: {col[4]}")
        
        print("\n=== Usuarios en el sistema ===")
        cursor.execute("SELECT id, username, nombre, es_admin FROM usuarios")
        usuarios = cursor.fetchall()
        for usuario in usuarios:
            print(f"ID: {usuario[0]}, Usuario: {usuario[1]}, Nombre: {usuario[2]}, Es Admin: {usuario[3]}")
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"Error al acceder a la base de datos: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    verificar_db()