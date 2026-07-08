# -------------------------------------------------------------------
# 1. Datos iniciales del sistema (Variables globales)
# -------------------------------------------------------------------
planes = {
    'F001': ['Plan Básico', 'mensual', 1, False, False, 'libre'],
    'F002': ['Plan Full', 'mensual', 1, True, True, 'libre'],
    'F003': ['Plan Estudiante', 'trimestral', 3, False, True, 'tarde'],
    'F004': ['Plan Senior', 'trimestral', 3, True, False, 'mañana'],
    'F005': ['Plan Anual Pro', 'anual', 12, True, True, 'libre'],
    'F006': ['Plan Nocturno', 'mensual', 1, False, True, 'noche']
}

inscripciones = {
    'F001': [14990, 30],
    'F002': [22990, 10],
    'F003': [39990, 0],
    'F004': [35990, 6],
    'F005': [159990, 2],
    'F006': [18990, 15]
}


# -------------------------------------------------------------------
# Funciones de la Opción 1 y Opción 2
# -------------------------------------------------------------------
def cupos_tipo(tipo):
    tipo_buscado = tipo.lower()
    total_cupos = 0
    for codigo, info in planes.items():
        if info[1].lower() == tipo_buscado:
            if codigo in inscripciones:
                total_cupos += inscripciones[codigo][1]
    print(f"El total de cupos disponibles es: {total_cupos}")


def busqueda_precio(p_min, p_max):
    resultados = []
    for codigo, datos in inscripciones.items():
        precio = datos[0]
        cupos = datos[1]
        if p_min <= precio <= p_max and cupos > 0:
            if codigo in planes:
                nombre_plan = planes[codigo][0]
                resultados.append(f"{nombre_plan}--{codigo}")
    
    if resultados:
        # Ordenar alfabéticamente por el nombre del plan
        resultados.sort()
        print(f"Los planes encontrados son: {resultados}")
    else:
        print("No hay planes en ese rango de precios.")


# -------------------------------------------------------------------
# Funciones de la Opción 3
# -------------------------------------------------------------------
def actualizar_precio(codigo, nuevo_precio):
    # Se estandariza a mayúsculas para la búsqueda en los diccionarios
    cod_upper = codigo.upper()
    if cod_upper not in inscripciones:
        return False
    
    inscripciones[cod_upper][0] = nuevo_precio
    return True


# -------------------------------------------------------------------
# Funciones de validación independiente (Opción 4)
# -------------------------------------------------------------------
def validar_codigo(codigo):
    if not codigo or codigo.strip() == "":
        return False
    if codigo.upper() in planes:
        return False
    return True

def validar_nombre(nombre):
    return bool(nombre and nombre.strip() != "")

def validar_tipo(tipo):
    return tipo in ['mensual', 'trimestral', 'anual']

def validar_duracion(duracion):
    try:
        val = int(duracion)
        return val > 0
    except ValueError:
        return False

def validar_acceso_piscina(opcion):
    return opcion.lower() in ['s', 'n']

def validar_incluye_clases(opcion):
    return opcion.lower() in ['s', 'n']

def validar_horario(horario):
    return bool(horario and horario.strip() != "")

def validar_precio(precio):
    try:
        val = int(precio)
        return val > 0
    except ValueError:
        return False

def validar_cupos(cupos):
    try:
        val = int(cupos)
        return val >= 0
    except ValueError:
        return False


# -------------------------------------------------------------------
# Función para agregar el plan (Opción 4)
# -------------------------------------------------------------------
def agregar_plan(codigo, nombre, tipo, duracion, acceso_piscina, incluye_clases, horario, precio, cupos):
    cod_upper = codigo.upper()
    if cod_upper in planes:
        return False
    
    # Transformaciones requeridas
    piscina_bool = True if acceso_piscina.lower() == 's' else False
    clases_bool = True if incluye_clases.lower() == 's' else False
    
    planes[cod_upper] = [nombre, tipo, int(duracion), piscina_bool, clases_bool, horario]
    inscripciones[cod_upper] = [int(precio), int(cupos)]
    return True


# -------------------------------------------------------------------
# Función de la Opción 5
# -------------------------------------------------------------------
def eliminar_plan(codigo):
    cod_upper = codigo.upper()
    if cod_upper not in planes or cod_upper not in inscripciones:
        return False
    
    del planes[cod_upper]
    del inscripciones[cod_upper]
    return True


# -------------------------------------------------------------------
# 2. Programa Principal / Menú de Control
# -------------------------------------------------------------------
def menu_principal():
    while True:
        print("\n========== MENÚ PRINCIPAL ==========")
        print("1. Cupos por tipo de plan")
        print("2. Búsqueda de planes por rango de precio")
        print("3. Actualizar precio de plan")
        print("4. Agregar plan")
        print("5. Eliminar plan")
        print("6. Salir")
        print("=====================================")
        
        opcion = input("Ingrese opción: ").strip()
        
        if opcion == '1':
            tipo = input("Ingrese tipo de plan a consultar: ")
            cupos_tipo(tipo)
            
        elif opcion == '2':
            while True:
                try:
                    p_min = int(input("Ingrese precio mínimo: "))
                    p_max = int(input("Ingrese precio máximo: "))
                    if p_min >= 0 and p_max >= 0 and p_min <= p_max:
                        busqueda_precio(p_min, p_max)
                        break
                    else:
                        print("Los precios deben ser mayores o iguales a cero y el mínimo menor o igual al máximo.")
                except ValueError:
                    print("Debe ingresar valores enteros")
                    
        elif opcion == '3':
            while True:
                cod = input("Ingrese código del plan: ")
                nuevo_p = input("Ingrese nuevo precio: ")
                
                # Validación local del nuevo precio (debe ser entero positivo)
                try:
                    nuevo_p_int = int(nuevo_p)
                    if nuevo_p_int <= 0:
                        print("El precio debe ser un valor entero positivo.")
                        continue
                except ValueError:
                    print("El precio debe ser un número entero válido.")
                    continue
                
                # Ejecutar actualización
                if actualizar_precio(cod, nuevo_p_int):
                    print("Precio actualizado")
                else:
                    print("El código no existe")
                
                otro = input("¿Desea actualizar otro precio (s/n)?: ").strip().lower()
                if otro != 's':
                    break
                    
        elif opcion == '4':
            cod = input("Ingrese código del plan: ")
            if not validar_codigo(cod):
                print("Error: Código vacío o ya existente en los registros.")
                continue
                
            nom = input("Ingrese nombre del plan: ")
            if not validar_nombre(nom):
                print("Error: El nombre no puede estar vacío.")
                continue
                
            tip = input("Ingrese tipo (mensual/trimestral/anual): ").strip().lower()
            if not validar_tipo(tip):
                print("Error: El tipo debe ser 'mensual', 'trimestral' o 'anual'.")
                continue
                
            dur = input("Ingrese duración (meses): ")
            if not validar_duracion(dur):
                print("Error: La duración debe ser un número entero mayor que cero.")
                continue
                
            pisc = input("¿Incluye acceso a piscina? (s/n): ")
            if not validar_acceso_piscina(pisc):
                print("Error: Debe ingresar 's' o 'n'.")
                continue
                
            clas = input("¿Incluye clases grupales? (s/n): ")
            if not validar_incluye_clases(clas):
                print("Error: Debe ingresar 's' o 'n'.")
                continue
                
            hor = input("Ingrese horario: ")
            if not validar_horario(hor):
                print("Error: El horario no puede estar vacío.")
                continue
                
            prec = input("Ingrese precio: ")
            if not validar_precio(prec):
                print("Error: El precio debe ser un número entero mayor que cero.")
                continue
                
            cup = input("Ingrese cupos: ")
            if not validar_cupos(cup):
                print("Error: Los cupos deben ser un número entero mayor o igual a cero.")
                continue
            
            # Si pasó todas las validaciones previas, se registra
            if agregar_plan(cod, nom, tip, dur, pisc, clas, hor, prec, cup):
                print("Plan agregado")
            else:
                print("El código ya existe")
                
        elif opcion == '5':
            cod = input("Ingrese el código del plan a eliminar: ")
            if eliminar_plan(cod):
                print("Plan eliminado")
            else:
                print("El código no existe")
                
        elif opcion == '6':
            print("Programa finalizado.")
            break
            
        else:
            print("Debe seleccionar una opción válida")

# Ejecución del programa
if __name__ == '__main__':
    menu_principal()
    