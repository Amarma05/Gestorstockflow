import sqlite3
import os
#importamos rich para la parte grafica
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint

console = Console()

#conectamos a la base de datos
def conectar_db():
    try:
        conn= sqlite3.connect('inventario.db')
        return conn
    except:
         print("Error al conectar la base de datos Productos")

#print("-------Bienvenidos a stockflow-------")
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
            
        rprint(f"[bold green]Producto {nombre} agregado correctamente![/bold green]")
    except sqlite3.IntegrityError:
            conn.rollback()
            rprint("[bold red]Error al ingresar producto.[/bold red]")

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
        rprint(f"[bold green]Producto {producto_id}: {nombre} actualizado correctamente![/bold green]")

    except sqlite3.IntegrityError:
           conn.rollback()
           rprint("[bold yellow]Producto no encontrado en la base de datos.[/bold yellow]")

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
# Módulo para visualizar producto
def visualizar_p(conn):
     try:
        cursor = conn.cursor()
        cursor.execute('SELECT id, nombre, descripcion, cantidad, precio, categoria FROM productos')
        productos = cursor.fetchall()
        
        if productos:
             # Crear objeto Table
             
             table = Table()
             
             # Añadir las columnas con estilo
             table.add_column("ID", style="cyan", justify="center")
             table.add_column("Nombre", style="white", min_width=25)
             table.add_column("Descripción", style="white", min_width=25)
             table.add_column("Cantidad", style="white", justify="center")
             table.add_column("Precio", style="white", justify="right")
             table.add_column("Categoría", style="white")

             for p in productos:
                  # NOTA: Usando los índices corregidos: p[3]=cantidad, p[4]=precio, p[5]=categoria
                  table.add_row(
                      str(p[0]),                   #id
                      p[1],                      #nombre
                      str(p[2]),                #descripcion                             
                      str(p[3]),                   # Cantidad
                      f"{p[4]}",               # Precio con formato de 2 decimales
                      p[5]                         # Categoría
                  )
             
             console.print(# Imprimir la tabla con rich
                Panel(
                    table,
                    title="[bold yellow]LISTADO COMPLETO DE PRODUCTOS[/bold yellow]",
                    border_style="purple",
                    padding=(1, 2)
                    )
                  )

        else:
             rprint("[yellow]⚠️ La base de datos de productos está vacía.[/yellow]")

     except sqlite3.Error as e:
          conn.rollback()
          rprint(f"[bold red]Error al visualizar los datos: {e}[/bold red]")

#modulo buscar producto
def buscar_producto(conn, id_busqueda):
     try:
        cursor = conn.cursor()
        productos = []
        if id_busqueda.isdigit():
           cursor.execute('SELECT * FROM productos WHERE id = ?', (int(id_busqueda),))
           productos = cursor.fetchall()
        
        if productos:
            table = Table()
             
             # Añadir las columnas con estilo
            table.add_column("ID", style="cyan", justify="center")
            table.add_column("Nombre", style="white", min_width=25)
            table.add_column("Descripción", style="white", min_width=25)
            table.add_column("Cantidad", style="white", justify="center")
            table.add_column("Precio", style="white", justify="right")
            table.add_column("Categoría", style="white")
            
            for p in productos:

              table.add_row(
                      str(p[0]),                   #id
                      p[1],                      #nombre
                      str(p[2]),                #descripcion                             
                      str(p[3]),                   # Cantidad
                      f"{p[4]}",               # Precio con formato de 2 decimales
                      p[5]                         # Categoría
                  )
              console.print(Panel(
                    table,
                    title=f"[bold yellow]🔎 RESULTADOS DE BÚSQUEDA para ID: {id_busqueda}[/bold yellow]",
                    border_style="purple",
                    padding=(1, 2)
                    )
                  )
        else:
             # 5. Usar rprint para el mensaje de no encontrado
            rprint(f"\n[yellow]⚠️ No se encontraron productos para el ID: '{id_busqueda}'[/yellow]")       
     except sqlite3.Error as e:
        print(f"\nError al buscar el producto: {e}")

#función para ppedir los datos de nuevos productos y llenar la tabla
def obtener_datos_producto():

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
        menu_text = (
            "[bold cyan]1.[/bold cyan] Ingresar producto\n"
            "[bold yellow]2.[/bold yellow] Actualizar productos\n"
            "[bold red]3.[/bold red] Eliminar productos\n"
            "[bold green]4.[/bold green] Visualizar productos \n"
            "[bold magenta]5.[/bold magenta] Buscar productos\n"
            "[bold blue]6.[/bold blue] Reporte stock de productos\n"
            "[bold white]7.[/bold white] 🚪 Salir"
        )
        #opcion = input("Seleccione una opción (1-7): ").strip()
        console.print(
            Panel(
                menu_text,
                title="[bold yellow]📦 SISTEMA STOCKFLOW[/bold yellow]",
                border_style="purple",
                padding=(1, 2)
            )
        )

        opcion = input("Seleccione una opción (1-7): ").strip()

        if opcion == "1":
            console.print(
                Panel(
                    # 2. El contenido (puede ser texto o vacío, si solo quieres el título)
                    "Complete los campos para el nuevo producto.", 
                    # Título: El texto es amarillo (yellow) y en negrita (bold)
                    title="[bold yellow]➕ INGRESAR PRODUCTO NUEVO[/bold yellow]", 
                    # Borde: El color es púrpura (purple)
                    border_style="purple", 
                    padding=(1, 2)
                )
            )
            
            #print("-----Ingresar producto nuevo-----")
            nombre, descripcion, cantidad, precio, categoria = obtener_datos_producto()
            ingresar_p_nuevo(conn, nombre, descripcion, cantidad, precio, categoria)
        
        elif opcion == "2":
            console.print(
                Panel(
                    "[bold yellow]Antes de eliminar algún producto verifique que sean los datos correctos![/bold yellow]",
                    title="[bold yellow]Elimine productos[/bold yellow]",
                    border_style="purple", 
                    padding=(1, 2),
                    #producto_id = input("Ingrese el ID del producto a eliminar")
                )
            )
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
            console.print(
                Panel(
                    "[bold yellow] En esta sección encuentre sus productos po ID![/bold yellow]",
                    title="[bold yellow]BUSCADOR...[/bold yellow]",
                    border_style="purple", 
                    padding=(1, 2),
                    #producto_id = input("Ingrese el ID del producto a eliminar")
                )
            )
            termino = input("Ingrese ID del producto a buscar: ").strip()
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

     


          


       