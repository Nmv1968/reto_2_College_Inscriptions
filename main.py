from cola_simple import ColaSimple
from cola_prioridad import ColaPrioridad
from cola_circular import ColaCircular
from estudiante import Estudiante
from lista_enlazada import ListaEnlazada


def inscriptionMenu():
    cola_simple = ColaSimple()
    cola_prioridad = ColaPrioridad()
    cola_circular = ColaCircular()
    lista_inscritos: ListaEnlazada = ListaEnlazada()

    while True:
        print("\n=== 🏫 Centro de Inscripciones Universitarias 🏫 ===")
        print("1. Configurar curso 🔈")
        print("2. Llegada estudiante 🚨")
        print("3. Procesar siguientes turnos en cola 📡")
        print("4. Mostrar inscritos/estado de colas 📊")
        print("5. Registrar retiro de inscripción 📊")
        print("6. Atender casos prioritarios 📊")
        print("7. Deshacer última acción 📊")
        print("8. Salir 🚪")
        print("\n =============================================================")
        opcion = validar_input("Seleccione una opción: ")

        match opcion:
            case "1":
                print("\n=== Configuración de curso ===")
                if (
                    lista_inscritos.get_list_name() is not None 
                    and lista_inscritos.get_list_max_size() is not None
                ):
                    print(
                        "⚠️ El curso ya ha sido configurado. No se puede modificar. ⛔"
                    )
                else:
                    print(configurar_curso(lista_inscritos))
            case "2":
                print("\n=== Registro de llegada de estudiante ===")
                if (
                    lista_inscritos.get_list_name() is None
                    and lista_inscritos.get_list_max_size() is None
                ):
                    print("⚠️ Configure el curso antes de registrar estudiantes.")
                else:
                    print(enqueue_estudiante(cola_simple, cola_prioridad, cola_circular, lista_inscritos))
            case "3":
                print("\n=== Procesar siguientes turnos en cola ===")
                if (
                    lista_inscritos.get_list_name() is None
                    and lista_inscritos.get_list_max_size() is None
                ):
                    print("⚠️ Configure el curso antes de procesar turnos.")
                else:
                    atender_turnos(cola_simple, cola_prioridad, cola_circular, lista_inscritos)
            case "4":
                mostrar_estado_colas(cola_simple, cola_prioridad, cola_circular, lista_inscritos)
            case "5":
                print("\n=== Registrar retiro de inscripción ===")
                if lista_inscritos.is_empty():
                    print("⚠️ No hay estudiantes inscritos para retirar. ⛔")
                else:
                    print(liberar_cupo(lista_inscritos, cola_prioridad, cola_circular))
            case "6":
                print("\n=== Atender casos prioritarios ===")
                atender_casos_prioritarios(cola_prioridad, cola_circular, lista_inscritos)
            case "7":
                pass
            case "8":
                print("Saliendo...🚪")
                break
            case _:
                print("Opción no válida. Intente nuevamente. ⛔")


# Valida que la entrada de texto no esté vacía
def validar_input(texto: str) -> str:
    # Bucle que solicita entrada hasta que sea válida
    while True:
        valor = input(texto)
        if valor.strip():
            return valor
        print("Entrada no válida. Por favor, ingrese un valor no vacío. ⛔")


def configurar_curso(curso: ListaEnlazada):
    nombre_curso = validar_input("Ingrese el nombre del curso: ")
    curso.set_list_name(nombre_curso)
    cupos = int(validar_input("Ingrese el número de cupos disponibles: "))
    curso.set_max_size(cupos)
    return f"Curso '{nombre_curso}' configurado exitosamente con {cupos} cupos. ✅"


def enqueue_estudiante(cola_simple: ColaSimple, cola_prioridad: ColaPrioridad, cola_circular: ColaCircular, lista_inscritos: ListaEnlazada) -> str:
    nombre = validar_input("Ingrese el nombre del estudiante: ")
    ci = validar_input("Ingrese la cédula de identidad del estudiante: ")
    has_prioridad = (
        validar_input("¿El estudiante tiene prioridad? (s/n): ").lower() == "s"
    )
    nuevo_estudiante = Estudiante(nombre, ci)
    if has_prioridad:
        return registrar_estudiante_prioridad(nuevo_estudiante, cola_prioridad, cola_circular, lista_inscritos)
    else:
        return registrar_estudiante_normal(nuevo_estudiante, cola_simple, cola_circular, lista_inscritos)


def registrar_estudiante_normal(
    nuevo_estudiante: Estudiante, cola_simple: ColaSimple, cola_circular: ColaCircular, lista_inscritos: ListaEnlazada
) -> str:
    cola_simple.enqueue(nuevo_estudiante)
    return f"↳ ENQUEUE estudiante normal: {nuevo_estudiante.nombre} 🔈"


def registrar_estudiante_prioridad(
    nuevo_estudiante: Estudiante, cola_prioridad: ColaPrioridad, cola_circular: ColaCircular, lista_inscritos: ListaEnlazada
) -> str:
    prioridad = validar_rango_prioridad("Ingrese la prioridad del estudiante (1-5): ")
    motivo_prioridad = validar_input("Ingrese el motivo de prioridad: ")
    cola_prioridad.enqueue(nuevo_estudiante, prioridad, motivo_prioridad)
    return f"↳ ENQUEUE estudiante con prioridad: {nuevo_estudiante.nombre} (P{prioridad}) - Motivo: {motivo_prioridad} 🚨"

def liberar_cupo(lista_inscritos: ListaEnlazada, cola_prioridad: ColaPrioridad, cola_circular: ColaCircular) -> str:
    if lista_inscritos.is_empty():
        return "No hay estudiantes inscritos para retirar. ⛔"
    
    print("\n=== Lista de inscritos ===")
    for id_estudiante, estudiante in lista_inscritos:
        print(f"ID {id_estudiante}: {estudiante.nombre} (CI: {estudiante.ci_estudiante})")
    
    ci_estudiante_retirar = validar_input("Ingrese la cédula del estudiante a retirar: ")
    estudiante_retirado = None
    for id_estudiante, estudiante in lista_inscritos:
        if estudiante.ci_estudiante == ci_estudiante_retirar:
            estudiante_retirado = estudiante
            break
    
    if estudiante_retirado is None:
        return f"No se encontró un estudiante con cédula {ci_estudiante_retirar}. ⛔"
    
    lista_inscritos.eliminar(id_estudiante)
    print(f"✅ Estudiante retirado: {estudiante_retirado.nombre}. Se ha liberado un cupo.")

    # Reasigna cupo
    if not cola_prioridad.is_empty():
        estudiante, prioridad, motivo_prioridad = cola_prioridad.dequeue()
        lista_inscritos.insertar_final(estudiante)
        return f"Cupo reasignado a estudiante prioritario: {estudiante.nombre} (P{prioridad}) - Motivo: {motivo_prioridad} 🚨"
    # Si hay espacio y cola simple tiene elementos
    elif not cola_circular.is_empty():
        estudiante = cola_circular.dequeue()
        lista_inscritos.insertar_final(estudiante)
        return f"Cupo reasignado a estudiante en espera: {estudiante.nombre} 🔈"
    else:
        return f"Cupo liberado exitosamente. No hay estudiantes prioritarios ni en espera para reasignar el cupo. ✅"

def mostrar_estado_colas(cola_simple: ColaSimple, cola_prioridad: ColaPrioridad, cola_circular: ColaCircular, lista_inscritos: ListaEnlazada):
     print("\n=== Estado actual de inscritos y colas ===")
     print("\n=== Estado de las colas ===")
     print(
         f"Cola simple 🔈 ({cola_simple.size()}): {[f'ID {id_estudiante}: {estudiante.nombre} (CI: {estudiante.ci_estudiante})' for id_estudiante, estudiante in cola_simple]}"
     )
     print(
         f"Cola prioritaria 🚨 ({cola_prioridad.size()}): {[f'ID {id_estudiante}: {estudiante.nombre} (P{prioridad}) - Motivo: {motivo}' for id_estudiante, estudiante, prioridad, motivo in cola_prioridad]}"
     )
     
     print(f"Cola circular 🔄 ({cola_circular.size()}): {[f'ID {id_estudiante}: {estudiante.nombre} (CI: {estudiante.ci_estudiante})' for id_estudiante, estudiante in cola_circular]}")
     
     print("\n=== Lista de inscritos ===")
     if lista_inscritos.is_empty():
         print("No hay estudiantes inscritos aún. ⛔")
     else:
         print(
             f"Estudiantes inscritos: ({lista_inscritos.size()}): {[f'ID {id_estudiante}: {estudiante.nombre} (CI: {estudiante.ci_estudiante})' for id_estudiante, estudiante in lista_inscritos]}"
         )

def atender_turnos(
    cola_simple: ColaSimple, cola_prioridad: ColaPrioridad, cola_circular: ColaCircular, lista_inscritos: ListaEnlazada
):
    if cola_prioridad.is_empty() and cola_circular.is_empty() and cola_simple.is_empty():
        return "No hay estudiantes para atender. ⛔"
    
    while lista_inscritos.size() < lista_inscritos.get_list_max_size():
        procesado = False
        
        # Procesar cola prioritaria
        if not cola_prioridad.is_empty():
            estudiante, prioridad, motivo_prioridad = cola_prioridad.dequeue()
            lista_inscritos.insertar_final(estudiante)
            print(f"Atendiendo estudiante prioritario: {estudiante.nombre} (P{prioridad}) - Motivo: {motivo_prioridad} 🚨")
            procesado = True
        
        # Si hay espacio y cola simple tiene elementos
        elif not cola_simple.is_empty():
            estudiante = cola_simple.dequeue()
            lista_inscritos.insertar_final(estudiante)
            print(f"Atendiendo estudiante normal: {estudiante.nombre} 🔈")
            procesado = True

                    
        # Si hay espacio y cola circular tiene elementos
        """ elif not cola_circular.is_empty():
            estudiante = cola_circular.dequeue()
            lista_inscritos.insertar_final(estudiante)
            print(f"Atendiendo estudiante en cola circular: {estudiante.nombre} 🔄")
            procesado = True """
        
        # Si no se procesó nada, salir del ciclo
        if not procesado:
            break
    
    if lista_inscritos.size() >= lista_inscritos.get_list_max_size():
        print("El curso ha alcanzado su capacidad máxima. No se pueden inscribir más estudiantes. ⛔")
        print("Los siguientes estudiantes no pudieron ser inscritos y seran colocados en la cola circular para esperar su turno:")
        for id_estudiante, estudiante, prioridad, motivo in cola_prioridad:
            print(f"ID {id_estudiante}: {estudiante.nombre} (P{prioridad}) - Motivo: {motivo}")
            cola_prioridad.dequeue()  # Eliminar de la cola de prioridad
            cola_circular.enqueue(estudiante)
        for id_estudiante, estudiante in cola_simple:
            print(f"ID {id_estudiante}: {estudiante.nombre} (CI: {estudiante.ci_estudiante})")
            cola_simple.dequeue()  # Eliminar de la cola simple
            cola_circular.enqueue(estudiante)

def atender_casos_prioritarios(cola_prioridad: ColaPrioridad, cola_circular: ColaCircular, lista_inscritos: ListaEnlazada):
    if lista_inscritos.size() >= lista_inscritos.get_list_max_size():
        print("El curso ha alcanzado su capacidad máxima. No se pueden inscribir más estudiantes. ⛔")
        return

    if cola_prioridad.is_empty() and cola_circular.is_empty():
        print("No hay estudiantes para atender. ⛔")
        return
    
    while lista_inscritos.size() < lista_inscritos.get_list_max_size():
        procesado = False
        
        if not cola_prioridad.is_empty():
            estudiante, prioridad, motivo_prioridad = cola_prioridad.dequeue()
            lista_inscritos.insertar_final(estudiante)
            print(f"Atendiendo estudiante prioritario: {estudiante.nombre} (P{prioridad}) - Motivo: {motivo_prioridad} 🚨")
            procesado = True
        
        # Si hay espacio y cola circular tiene elementos
        elif not cola_circular.is_empty():
            estudiante = cola_circular.dequeue()
            lista_inscritos.insertar_final(estudiante)
            print(f"Atendiendo estudiante en cola circular: {estudiante.nombre} 🔄")
            procesado = True
        
        # Si no se procesó nada, salir del ciclo
        if not procesado:
            break

    if lista_inscritos.size() >= lista_inscritos.get_list_max_size():
        print("El curso ha alcanzado su capacidad máxima. No se pueden inscribir más estudiantes. ⛔")
        print("Los siguientes estudiantes no pudieron ser inscritos y seran colocados en la cola circular para esperar su turno:")
        for id_estudiante, estudiante, prioridad, motivo in cola_prioridad:
            print(f"ID {id_estudiante}: {estudiante.nombre} (P{prioridad}) - Motivo: {motivo}")
            cola_prioridad.dequeue()  # Eliminar de la cola de prioridad
            cola_circular.enqueue(estudiante)
        for id_estudiante, estudiante in cola_circular:
            print(f"ID {id_estudiante}: {estudiante.nombre} (CI: {estudiante.ci_estudiante})")
            cola_circular.dequeue()  # Eliminar de la cola circular
            cola_circular.enqueue(estudiante)


def validar_rango_prioridad(prioridad: str) -> int:
    while True:
        try:
            valor_prioridad = int(validar_input(prioridad))
            if 1 <= valor_prioridad <= 5:
                break
            print("Prioridad no válida ⛔. Ingrese un valor entre 1 y 5.")
        except ValueError:
            print("Error: Debe ingresar un número entero. ⛔")
    return valor_prioridad


# Función principal que inicia el menú de operaciones
def main():
    inscriptionMenu()


# Punto de entrada del programa
if __name__ == "__main__":
    main()
