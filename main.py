from cola_simple import ColaSimple
from cola_prioridad import ColaPrioridad
from cola_circular import ColaCircular
from estudiante import Estudiante
from lista_enlazada import ListaEnlazada
from stack import Stack, Accion


# Pila de historial para deshacer acciones
historial_acciones = Stack()


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
                print("\n=== Deshacer última acción 📊")
                print(deshacer_accion(cola_simple, cola_prioridad, cola_circular, lista_inscritos))
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
    
    # Registrar acción en el historial
    accion = Accion(
        tipo="configurar_curso",
        datos={"nombre_curso": nombre_curso, "cupos": cupos},
        descripcion=f"Configurar curso '{nombre_curso}' con {cupos} cupos"
    )
    historial_acciones.push(accion)
    
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
    
    # Registrar acción en el historial
    accion = Accion(
        tipo="enqueue_normal",
        datos={"nombre": nuevo_estudiante.nombre, "ci": nuevo_estudiante.ci_estudiante},
        descripcion=f"Registro de estudiante normal: {nuevo_estudiante.nombre}"
    )
    historial_acciones.push(accion)
    
    return f"↳ ENQUEUE estudiante normal: {nuevo_estudiante.nombre} 🔈"


def registrar_estudiante_prioridad(
    nuevo_estudiante: Estudiante, cola_prioridad: ColaPrioridad, cola_circular: ColaCircular, lista_inscritos: ListaEnlazada
) -> str:
    prioridad = validar_rango_prioridad("Ingrese la prioridad del estudiante (1-5): ")
    motivo_prioridad = validar_input("Ingrese el motivo de prioridad: ")
    cola_prioridad.enqueue(nuevo_estudiante, prioridad, motivo_prioridad)
    
    # Registrar acción en el historial
    accion = Accion(
        tipo="enqueue_prioridad",
        datos={"nombre": nuevo_estudiante.nombre, "ci": nuevo_estudiante.ci_estudiante, "prioridad": prioridad, "motivo": motivo_prioridad},
        descripcion=f"Registro de estudiante prioritario: {nuevo_estudiante.nombre} (P{prioridad})"
    )
    historial_acciones.push(accion)
    
    return f"↳ ENQUEUE estudiante con prioridad: {nuevo_estudiante.nombre} (P{prioridad}) - Motivo: {motivo_prioridad} 🚨"

def liberar_cupo(lista_inscritos: ListaEnlazada, cola_prioridad: ColaPrioridad, cola_circular: ColaCircular) -> str:
    if lista_inscritos.is_empty():
        return "No hay estudiantes inscritos para retirar. ⛔"
    
    print("\n=== Lista de inscritos ===")
    for id_estudiante, estudiante in lista_inscritos:
        print(f"ID {id_estudiante}: {estudiante.nombre} (CI: {estudiante.ci_estudiante})")
    
    ci_estudiante_retirar = validar_input("Ingrese la cédula del estudiante a retirar: ")
    estudiante_retirado = None
    id_estudiante_retirado = None
    for id_estudiante, estudiante in lista_inscritos:
        if estudiante.ci_estudiante == ci_estudiante_retirar:
            estudiante_retirado = estudiante
            id_estudiante_retirado = id_estudiante
            break
    
    if estudiante_retirado is None:
        return f"No se encontró un estudiante con cédula {ci_estudiante_retirar}. ⛔"
    
    lista_inscritos.eliminar(id_estudiante_retirado)
    print(f"✅ Estudiante retirado: {estudiante_retirado.nombre}. Se ha liberado un cupo.")

    # Registrar acción en el historial
    accion = Accion(
        tipo="liberar_cupo",
        datos={"nombre": estudiante_retirado.nombre, "ci": estudiante_retirado.ci_estudiante, "id_estudiante": id_estudiante_retirado},
        descripcion=f"Retiro de inscripción: {estudiante_retirado.nombre}"
    )
    historial_acciones.push(accion)

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
            # Registrar cada estudiante atendido individualmente en el historial
            accion = Accion(
                tipo="atender",
                datos={
                    "nombre": estudiante.nombre,
                    "ci": estudiante.ci_estudiante,
                    "tipo": "prioridad",
                    "prioridad": prioridad,
                    "motivo": motivo_prioridad
                },
                descripcion=f"Atender estudiante prioritario: {estudiante.nombre} (P{prioridad})"
            )
            historial_acciones.push(accion)
            print(f"Atendiendo estudiante prioritario: {estudiante.nombre} (P{prioridad}) - Motivo: {motivo_prioridad} 🚨")
            procesado = True
        
        # Si hay espacio y cola simple tiene elementos
        elif not cola_simple.is_empty():
            estudiante = cola_simple.dequeue()
            lista_inscritos.insertar_final(estudiante)
            # Registrar cada estudiante atendido individualmente en el historial
            accion = Accion(
                tipo="atender",
                datos={
                    "nombre": estudiante.nombre,
                    "ci": estudiante.ci_estudiante,
                    "tipo": "normal"
                },
                descripcion=f"Atender estudiante normal: {estudiante.nombre}"
            )
            historial_acciones.push(accion)
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
            # Registrar cada estudiante atendido individualmente en el historial
            accion = Accion(
                tipo="atender_prioritario",
                datos={
                    "nombre": estudiante.nombre,
                    "ci": estudiante.ci_estudiante,
                    "tipo": "prioridad",
                    "prioridad": prioridad,
                    "motivo": motivo_prioridad
                },
                descripcion=f"Atender caso prioritario: {estudiante.nombre} (P{prioridad})"
            )
            historial_acciones.push(accion)
            print(f"Atendiendo estudiante prioritario: {estudiante.nombre} (P{prioridad}) - Motivo: {motivo_prioridad} 🚨")
            procesado = True
        
        # Si hay espacio y cola circular tiene elementos
        elif not cola_circular.is_empty():
            estudiante = cola_circular.dequeue()
            lista_inscritos.insertar_final(estudiante)
            # Registrar cada estudiante atendido individualmente en el historial
            accion = Accion(
                tipo="atender_prioritario",
                datos={
                    "nombre": estudiante.nombre,
                    "ci": estudiante.ci_estudiante,
                    "tipo": "circular"
                },
                descripcion=f"Atender estudiante en espera: {estudiante.nombre}"
            )
            historial_acciones.push(accion)
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


def deshacer_accion(cola_simple: ColaSimple, cola_prioridad: ColaPrioridad, cola_circular: ColaCircular, lista_inscritos: ListaEnlazada) -> str:
    """Deshace la última acción registrada en el historial."""
    
    if historial_acciones.is_empty():
        return "No hay acciones para deshacer. ⛔"
    
    # Confirmar deshacer
    print(f"Última acción: {historial_acciones.peek()}")
    confirm = validar_input("¿Está seguro que desea deshacer la última acción? (s/n): ").lower()
    
    if confirm != "s":
        return "Operación de deshacer cancelada. ⛔"
    
    # Extraer la acción del historial
    accion = historial_acciones.pop()
    
    # Procesar según el tipo de acción
    match accion.tipo:
        case "configurar_curso":
            # Reiniciar la configuración del curso
            lista_inscritos.set_list_name(None)
            lista_inscritos.set_max_size(0)
            return f"Acción deshecha: Se ha eliminado la configuración del curso '{accion.datos['nombre_curso']}'. ✅"
        
        case "enqueue_normal":
            # Eliminar al estudiante de la cola simple
            nombre = accion.datos["nombre"]
            ci = accion.datos["ci"]
            # Buscar y eliminar el estudiante de la cola simple
            for id_estudiante, estudiante in cola_simple:
                if estudiante.ci_estudiante == ci:
                    cola_simple.eliminar_por_ci(ci)
                    return f"Acción deshecha: Estudiante normal '{nombre}' eliminado de la cola. ✅"
            return f"No se pudo deshacer: Estudiante '{nombre}' no encontrado en la cola. ⛔"
        
        case "enqueue_prioridad":
            # Eliminar al estudiante de la cola de prioridad
            nombre = accion.datos["nombre"]
            ci = accion.datos["ci"]
            prioridad = accion.datos["prioridad"]
            # Buscar y eliminar el estudiante de la cola de prioridad
            for id_estudiante, estudiante, prioridad, motivo_prioridad in cola_prioridad:
                if estudiante.ci_estudiante == ci:
                    cola_prioridad.eliminar_por_ci(ci)
                    return f"Acción deshecha: Estudiante prioritario '{nombre}' (P{prioridad}) eliminado de la cola. ✅"
            return f"No se pudo deshacer: Estudiante '{nombre}' no encontrado en la cola de prioridad. ⛔"
        
        case "atender" | "atender_prioritario":
            # Eliminar al estudiante de la lista de inscritos
            ci = accion.datos["ci"]
            tipo = accion.datos["tipo"]
            nombre = accion.datos["nombre"]
            
            # Buscar y eliminar el estudiante de la lista de inscritos
            for id_est, est in lista_inscritos:
                if est.ci_estudiante == ci:
                    lista_inscritos.eliminar(id_est)
                    # Regresar el estudiante a su cola correspondiente
                    if tipo == "prioridad":
                        prioridad = accion.datos.get("prioridad", 1)
                        motivo = accion.datos.get("motivo", "")
                        est = Estudiante(nombre, ci)
                        cola_prioridad.enqueue(est, prioridad, motivo)
                        return f"Acción deshecha: Estudiante prioritario '{nombre}' removido de inscritos y regresado a cola de prioridad. ✅"
                    elif tipo == "normal":
                        est = Estudiante(nombre, ci)
                        cola_simple.enqueue(est)
                        return f"Acción deshecha: Estudiante normal '{nombre}' removido de inscritos y regresado a cola simple. ✅"
                    elif tipo == "circular":
                        est = Estudiante(nombre, ci)
                        cola_circular.enqueue(est)
                        return f"Acción deshecha: Estudiante '{nombre}' removido de inscritos y regresado a cola circular. ✅"
            return f"No se pudo deshacer: Estudiante '{nombre}' no encontrado en la lista de inscritos. ⛔"
        
        case "liberar_cupo":
            # Reintegrar al estudiante a la lista de inscritos
            nombre = accion.datos["nombre"]
            ci = accion.datos["ci"]
            est = Estudiante(nombre, ci)
            lista_inscritos.insertar_final(est)
            return f"Acción deshecha: Estudiante '{nombre}' reintegrado a la lista de inscritos. ✅"
        
        case _:
            return f"Tipo de acción desconocido: {accion.tipo}. No se puede deshacer. ⛔"


# Función principal que inicia el menú de operaciones
def main():
    inscriptionMenu()


# Punto de entrada del programa
if __name__ == "__main__":
    main()
