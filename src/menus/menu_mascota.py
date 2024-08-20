from config.mascota import Mascota
from os import system
from sys import stdout
from time import sleep
system("cls")

def main():
    try:
        while True:
            print("-------------------- Menu Mascota ------------------")
            print("1. Regitrar nueva mascota")
            print("2. Buscar mascota")
            print("3. Actualizar mascota")
            print("4. Eliminar mascota")
            print("5. Salir")            

            while True:
                try:
                    opcion = int(input("Seleccione una opcion: "))
                    break
                except ValueError:
                    print("Opción no válida")
                    
            if opcion == 5: 
                system("cls")
                break
            
        
            elif opcion == 1:
                system("cls")
                print("1. Registrar Mascota")
                inser_mascota = Mascota()
                inser_mascota.InsertarMascota()
                system('pause')
                system('cls')
            
            elif opcion == 2:
                system("cls")
                inser_mascota = Mascota()
                id = int(input("Id de mascota a buscar: "))
                inser_mascota.BuscarMascotaID(id)
                system('pause')
                system('cls')
            
            elif opcion == 3:
                system("cls")
                inser_mascota = Mascota()
                id = int(input("Id de mascota a actualizar : "))
                inser_mascota.ActualizarMascota(id)
                system('pause')
                system('cls')
            elif opcion == 4:
                system("cls")
                inser_mascota = Mascota()
                id = int(input('Ingrese el id de la mascota que desea eliminar: '))
                inser_mascota.EliminarMascota(id)
                system('pause')
                system('cls')
            else:
                system("cls")
                print("Opcion no valida intente de nuevo")   
    except KeyboardInterrupt:
        print('El usuario ha cancelado la ejecución, por favor continue')
    except Exception as error:
        print(f'Ha ocurrido error no codificado {error}')
    finally:
        end = 'Gracias por usar nuestro programa'
        for i in end:
            print(i,end="")
            stdout.flush()
            sleep(0.1)
