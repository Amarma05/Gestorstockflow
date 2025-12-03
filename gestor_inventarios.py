import sqlite3
import os
#conectamos a la base de datos
def conectar_db():
    try:
        conn= sqlite3.connect('inventario.db')
        return conn
    except:
         print("Error al conectar la base de datos Productos")

print("-------Bienvenidos a stockflow-------")
#creamos la base de datos
def tabla_productos(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS productos (
                       id INTEGER PRIMARY KEY,
                       nombre TEXT NOT NULL,
                       descripcion TEXT NOT NULL, 
                       cantidad INTEGER, 
                       precio INTEGER NOT NULL, 
                       categoria TEXT NOT NULL)
               ''' )
        conn.commit()
    except sqlite3.Error as e:
        print(f"\nError tabla {e}")

#modulo para ingresar productos nuevos
def ingresar_p_nuevo(conn, nombre, descripcion, precio, cantidad, categoria):
    
    try:
        cursor= conn.cursor()
        cursor.execute('''
        INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria)
        VALUES (?, ?, ?, ?, ?)
    ''',(nombre, descripcion, cantidad, precio, categoria))
        conn.commit()
            
        print(f"Producto {nombre} agregado correctamente!")
    except sqlite3.IntegrityError:
            conn.rollback()
            print("Error al ingresar producto.")

#modulo para actualizar producto
def actualizar_p(conn, producto_id, nombre,descripcion, cantidad, precio, categoria):          
    try:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE productos
            SET nombre = ?, descripcion = ?, cantidad = ?, precio = ?, categoria = ?
            WHERE id = ?
        ''', (producto_id, nombre, descripcion, cantidad, precio, categoria))
        conn.commit()
        print(f"Producto {producto_id}: {nombre} actualizado correctamente!")

    except sqlite3.IntegrityError:
           conn.rollback()
           print("Producto no encontrado en la base de datos.")

#modulo para eliminar producto
def eliminar_producto(conn, producto_id):
     try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM productos WHERE id = ?', (producto_id,))
        conn.commit()
        if cursor.rowcount > 0:
               print(f"\nProducto con ID {producto_id} eliminado con éxito.")
        else:
               print(f"\nNo se encontró el producto con ID {producto_id}.")
     except sqlite3.Error as e:
        conn.rollback()
        print(f"\nError al eliminar el producto: {e}")

#modulo para visualizar producto
def visualizar_p(conn):
     try:
        cursor = conn.cursor()
        cursor.execute('SELECT id, nombre, descripcion, cantidad, precio, categoria FROM productos')
        productos = cursor.fetchall()
        
        if productos:
             print("----Lista de productos----")
             print("{:<5} {:<25} {:<25} {:<10} {:<10} {:<15}".format("ID", "Nombre", "descripcion",
             "Cantidad", "Precio", "Categoría"))
             print("-" * 90)
             for p in productos:
                  print("{:<5} {:<25} {:<25} {:<10} {:<10} {:<15}".format(p[0],p[1],p[2],p[3],p[4],p[5]))
             print("-" * 90)
        else:
         print("\nLa base de datos de productos está vacía.")

     except sqlite3.Error as e:
          conn.rollback()
          print("Error al visualizar los datos.")

#modulo buscar producto
def buscar_producto(conn, id_busqueda):
     try:
        cursor = conn.cursor()
        productos = []
        if id_busqueda.isdigit():
           cursor.execute('SELECT * FROM productos WHERE id = ?', (int(id_busqueda),))
           productos = cursor.fetchall()
        
        if productos:
            print(f"\n--- RESULTADOS DE BÚSQUEDA para '{id_busqueda}' ---")
            print("{:<5} {:<25} {:<30} {:<10} {:<10} {:<15}".format("ID", "Nombre", "Descripción", "Cantidad", "Precio", "Categoría"))
            print("-" * 105)
            for p in productos:
                
                print("{:<5} {:<25} {:<30} {:<10} {:<10} {:<15}".format(p[0], p[1], p[2], p[3], p[4],p[5]))
            print("-" * 105)
        else:
            print(f"\nNo se encontraron productos para el término: '{id_busqueda}'")
            
     except sqlite3.Error as e:
        print(f"\nError al buscar el producto: {e}")

#función para ppedir los datos de nuevos productos y llenar la tabla
def obtener_datos_producto():
    print("\n--- INGRESO DE DATOS ---")
    nombre = input("Nombre del Producto: ").strip().capitalize()
    descripcion = input("Descripción (opcional): ").strip().capitalize(

    )
    categoria = input("Categoría: ").strip().capitalize()

 #validamos la entrada de datos para la cantidad y el precio  
    while True:
        try:
            cantidad = int(input("Cantidad (Stock): "))
            if cantidad < 0:
                print("La cantidad no puede ser negativa.")
                continue
            break
        except ValueError:
            print("Entrada no válida. Por favor, ingrese un número entero para la cantidad.")

    while True:
        try:
            precio = float(input("Precio unitario: "))
            if precio < 0:
                print("El precio no puede ser negativo.")
                continue
            break
        except ValueError:
            print("Entrada no válida. Por favor, ingrese un número para el precio.")
            
    return nombre, descripcion, cantidad, precio, categoria

def reporte_bajo_s(conn,limite =3):#declaramos que si hay productos con cantidad menor a 3 se muestren
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT id, nombre, cantidad, categoria FROM productos WHERE cantidad <= ?', (limite,))
        productos_bajo_stock = cursor.fetchall()
        if productos_bajo_stock:
            print("\n¡PRODUCTOS CON BAJO STOCK!")
            print(f"(Stock menor o igual a {limite} unidades)")
            print("{:<5} {:<25} {:<10} {:<15}".format("ID", "Nombre", "cantidad", "Categoría"))
            print("-" * 55)
        else:
          print("\n¡stock al día!")
    except sqlite3.Error as e:
        print(f"\nError al generar el reporte de stock: {e}")

  
def main():
    conn = conectar_db()
    if conn is None:
        return
    tabla_productos(conn)

    while True:
        print("\n--- Menú ---")
        print("1. Ingresar producto")
        print("2. Actualizar productos")
        print("3. Eliminar productos")
        print("4. visualizar productos ")
        print("5. Buscar productos")
        print("6. Reporte stock de productos")
        print("7. Salir")

        opcion = input("Seleccione una opción (1-7): ").strip()

        if opcion == "1":
            print("-----Ingresar producto nuevo-----")
            nombre, descripcion, cantidad, precio, categoria = obtener_datos_producto()
            ingresar_p_nuevo(conn, nombre, descripcion, cantidad, precio, categoria)
        
        elif opcion == "2":
            producto_id = input("Ingrese el ID del producto a eliminar")
            if not producto_id.isdigit():
                print("ID no válido. Debe ser un número.")
            else:
                print(f"\n--- ACTUALIZAR PRODUCTO (ID: {producto_id}) ---".format(producto_id))
                nombre, descripcion, cantidad, precio, categoria = obtener_datos_producto()
                actualizar_p(conn, int(producto_id), nombre, descripcion, cantidad, precio, categoria)
                  
        elif opcion == "3":
            producto_id = input("Ingrese el ID del producto a eliminar: ").strip()
            if producto_id.isdigit():
                eliminar_producto(conn, int(producto_id))
            else:
                print("ID no válido. Debe ser un número.")
            
        elif opcion == "4":
            visualizar_p(conn)
            
        elif opcion == "5":
            termino = input("Ingrese ID o parte del Nombre del producto a buscar: ").strip()
            buscar_producto(conn,termino)

        elif opcion == "6":
            reporte_bajo_s(conn)

        elif opcion == '7':
            print("\nSaliendo del sistema. ¡Hasta pronto!")
            conn.close()
            break
        else:
            print("\nOpción no válida. Por favor, ingrese un número del 1 al 7.")
        
        input("\nPresione ENTER para continuar...")
if __name__ == "__main__":
     main()

     


          


       