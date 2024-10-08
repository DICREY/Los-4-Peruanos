import os 
import re
from datetime import datetime
from config.conexion10 import BaseDatos

os.system("cls")

class Productos():
    @classmethod
    def __init__(cls,
                 id: str = None,
                 nombre: str = None,
                 descripcion: str = None,
                 precio: float = None,
                 stock: int = None
                ):
        
        cls.__id = id
        cls.__nombre = nombre
        cls.__descripcion = descripcion
        cls.__precio = precio
        cls.__stock = stock
        
    @classmethod
    def set_id(cls):
        while True:
                try:
                    id = input('Escriba el id del producto: ')
                    if (1 <= len(id) <= 1000000000):
                        cls.__id = id
                        break
                    else:
                        print('El número debe estar entre 3 y 100000000')
                except ValueError:
                    print('El código debe ser un número.')
                except KeyboardInterrupt:
                    print('El usuario ha cancelado la entrada de datos.')
                continue
            
    @classmethod
    def get_id(cls):
        return cls.__id
         
    @classmethod
    def set_nombre(cls):
        while True:
            try:
                patron = r'^[a-zA-Z ]+$'
                nombre = input("Ingrese el nombre del producto: ")
                if len(nombre) >= 3 and re.match(patron, nombre):
                    cls.__nombre = nombre 
                    break
                else:
                    print("El nombre debe tener almenos 3 caracteres. Intente nuevamente.")
            except KeyboardInterrupt:
                print('El usuario ha cancelado la entrada de datos.')
                continue
            
    @classmethod
    def get_nombre(cls):
        return cls.__nombre
    
    @classmethod
    def set_descripcion(cls):
        while True:
            try:
                patron = r'^[a-zA-Z ]+$'
                descripcion = input("Ingrese la descripcion del producto: ")
                if len(descripcion) > 10 and re.match(patron, descripcion):
                    cls.__descripcion = descripcion
                    break
            except KeyboardInterrupt:
                print('El usuario ha cancelado la entrada de datos.')
                continue
    
    @classmethod
    def get_descripcion(cls):
        return cls.__descripcion
    
    @classmethod
    def set_precio(cls):
        while True:
            try:
                precio = float(input("Ingrese el precio del producto: "))
                if (1 <= precio <= 1000000000):
                    cls.__precio = precio
                    break
                else:
                    print('Error inserte nuevamente')
            except KeyboardInterrupt:
                print('El usuario ha cancelado la entrada de datos.')
                continue
            
    @classmethod
    def get_precio(cls):
        return cls.__precio
    
    @classmethod
    def set_stock(cls):
        while True:
            try:
                stock = int(input("Inserte la cantidad de productos que hay: "))
                cls.__stock = stock
                break
            except KeyboardInterrupt:
                print('El usuario ha cancelado la entrada de datos.')
                continue
    
    @classmethod
    def get_stock(cls):
        return cls.__stock
    
    @classmethod
    def insertar_producto(cls):
        cls.capturar_datos()
        conexion = BaseDatos.conectar()
        
        if conexion: 
            cursor_productos = conexion.cursor()
            cursor_productos.callproc("InsertarProducto", [
                cls.get_id(),
                cls.get_nombre(),
                cls.get_descripcion(),
                cls.get_precio(),
                cls.get_stock()
            ])
            conexion.commit()
        print("Producto registrado correctamente...")
        if conexion:
            BaseDatos.desconectar()
            
    @classmethod
    def capturar_datos(cls):
        cls.set_id()
        cls.set_nombre()
        cls.set_descripcion()
        cls.set_precio()
        cls.set_stock()
    
    @classmethod
    def buscar_producto_id(cls, id = None):
        conexion = BaseDatos.conectar()
        if conexion:
            try: 
                producto_encontrado = False
                cursor_productos = conexion.cursor()
                print(f"Buscando el producto {id}...")
                cursor_productos.callproc("BuscarProductoID", [id])
                for busqueda in cursor_productos.stored_results():
                    resultado = busqueda.fetchone()
                    if resultado:
                        producto_encontrado = True
                        print('\nResultado:\n',
                        f'************************************************\n{resultado}\n',
                        '************************************************')
                        return producto_encontrado
                    else:
                        print("Producto no encontrado. intente de nuevo")
                        print(producto_encontrado)
                        return producto_encontrado
            except Exception as e:
                print(f'Error al buscar el producto: {e}')
            finally:
                if conexion:
                    cursor_productos.close()
                    BaseDatos.desconectar()        
    
    @classmethod
    def actualizar_producto(cls , id):
        conexion = BaseDatos.conectar()
        producto_encontrado = cls.buscar_producto_id(id)
        if producto_encontrado:
            try:
                print('--------------- Escriba los nuevos datos del producto ---------------')
                cls.set_id()
                cls.set_nombre()
                cls.set_descripcion()
                cls.set_precio()
                cls.set_stock()
                
                nuevo_id = cls.get_id()
                nuevo_nombre = cls.get_nombre()
                nuevo_descripcion = cls.get_descripcion()
                nuevo_precio = cls.get_precio()
                nuevo_stock = cls.get_stock()
                
                print(f"id: {nuevo_id}")
                print(f"nombre: {nuevo_nombre}")
                print(f"Nueva descripcion: {nuevo_descripcion}")
                print(f"Nuevo precio: {nuevo_precio}")
                print(f"Nuevo stock: {nuevo_stock}")
                
                cursor_producto = conexion.cursor()
                cursor_producto.callproc("ActualizarProducto", [
                    nuevo_id,
                    nuevo_nombre,
                    nuevo_descripcion,
                    nuevo_precio,
                    nuevo_stock
                ])
                conexion.commit()
                cursor_producto.close()
                print("Producto actualizado")
            except Exception as error:
                print(f"Error al actualiza el producto: {error}. Intente de nuevo")
            finally:
                BaseDatos.desconectar()
        else:
            print("Producto no encontrado. intente otra vez")        

    @classmethod
    def eliminar_producto (cls, id):
        conexion = BaseDatos.conectar()
        producto_encontrado = cls.buscar_producto_id(id)
        if producto_encontrado:
            try:
                cursor_producto = conexion.cursor()
                cursor_producto.callproc("EliminarProducto", [id])
                conexion.commit()
                cursor_producto.close()
                print("Producto eliminado")
            except Exception as error:
                print(f"Error al eliminar producto: {error}. intente de nuevo")
            finally:
                BaseDatos.desconectar()

    @classmethod
    def buscar_producto_nombre(cls, nombre = None):
        conexion = BaseDatos.conectar()
        if conexion:
            try:
                if nombre is None:
                    while True:
                        nombre = input("Escribe el nombre del producto que desea buscar: ")
                        if len(nombre) > 2:
                            break
                        else:
                            print("Escribe un nombre valido")
                producto_encontrado = False
                cursor_producto = conexion.cursor()
                print(f'Buscando producto...')
                cursor_producto.callproc('BuscarProductoNombre', [nombre])
                for busqueda in cursor_producto.stored_results():
                    resultados = busqueda.fetchall()
                    if resultados:
                        for datos in resultados:
                            print(datos)
                        return producto_encontrado
                    else:
                        print('No se encontraron registros. Intente de nuevo.')
                        print(producto_encontrado)
                        return producto_encontrado
            except Exception as e:
                print(f'Error al buscar producto: {e}')
            finally:
                if conexion:
                    cursor_producto.close()
                    BaseDatos.desconectar()
    
    