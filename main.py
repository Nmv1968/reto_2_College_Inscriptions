"""
================================================================================
MÓDULO: main.py
================================================================================
Módulo PRINCIPAL del sistema de gestión de inscripciones.

¿QUÉS HACE ESTE MÓDULO?
- Controla el flujo principal del programa (menú de opciones)
- Coordina todas las estructuras de datos (colas, lista de inscritos)
- Implementa la lógica de negocio del sistema universitario
- Gestiona el historial de acciones para la función "Deshacer"

ESTRUCTURAS DE DATOS USADAS:
- ColaSimple: Estudiantes regulares en espera (FIFO)
- ColaPrioridad: Estudiantes con prioridad (Beca, Ultimo semestre, etc)
- ColaCircular: Cola de espera cuando el curso está lleno
- ListaEnlazada: Estudiantes ya inscritos en el curso
- Stack: Historial de acciones para deshacer operaciones

FLUJO GENERAL:
1. Configurar curso (nombre + cupos)
2. Registrar llegada de estudiantes (normal o prioritario)
3. Procesar siguientes turnos en cola (Prioridad -> Regular)
4. Procesar turnos prioritarios (inscribir según prioridad y si estan en cola de espera)
5. Gestionar retiros y reasignaciones
6. Deshacer acciones si es necesario
================================================================================
"""

from cola_simple import ColaSimple
from cola_prioridad import ColaPrioridad
from cola_circular import ColaCircular
from estudiante import Estudiante
from lista_enlazada import ListaEnlazada
from stack import Stack, Accion


def main_menu():
    """
    Función principal que muestra el menú y procesa las opciones del usuario.
    
    Estructuras de datos inicializadas:
    - cola_simple: Cola FIFO para estudiantes regulares
    - cola_prioridad: Cola de prioridad para casos urgentes
    - cola_circular: Cola de espera cuando el curso está lleno
    - lista_inscritos: Lista de estudiantes matriculados
    - historial_acciones: Pila para el sistema de deshacer
    """
    # Inicializar todas las estructuras de datos
    cola_simple = ColaSimple()
    cola_prioridad = ColaPrioridad()
    cola_circular = ColaCircular()
    lista_inscritos = ListaEnlazada()
    historial_acciones = Stack()

    # Ciclo principal del programa
    while True:
        header = f"=== 🏫 Centro de Inscripciones: {lista_inscritos.list_name} 🏫 ===" if lista_inscritos.is_course_configurated else "=== 🏫 Centro de Inscripciones Universitarias 🏫 ==="
        print(f"\n{header}")
        print("1. Configurar curso 🔈")
        print("2. Llegada estudiante 🚨")
        print("3. Procesar siguientes turnos en cola 🏁")
        print("4. Mostrar inscritos/estado de colas 📊")
        print("5. Registrar retiro de inscripción 🗑️")
        print("6. Atender casos prioritarios ⚡")
        print("7. Deshacer última acción ↩️")
        print("8. Ver historial de acciones 📜")
        print("9. Salir 🚪")
        print("\n" + "=" * len(header))
        opcion = validar_input("Seleccione una opción: ")

        # Bloque de opciones del menú
        match opcion:
            case "1":
                print("\n=== Configuración de curso ===")
                if lista_inscritos.is_course_configurated:
                    print("⚠️ El curso ya ha sido configurado. No se puede modificar. ⛔")
                else:
                    print(configurar_curso(lista_inscritos, historial_acciones))
            
            case "2":
                if verificar_configuracion(lista_inscritos):
                    print(f"\n=== Registro de llegada: {lista_inscritos.list_name} ===")
                    print(registrar_llegada_estudiante(cola_simple, cola_prioridad, historial_acciones))
            
            case "3":
                if verificar_configuracion(lista_inscritos):
                    print(f"\n=== Procesando turnos para: {lista_inscritos.list_name} ===")
                    atender_turnos(cola_simple, cola_prioridad, cola_circular, lista_inscritos, historial_acciones)
            
            case "4":
                mostrar_estado_colas(cola_simple, cola_prioridad, cola_circular, lista_inscritos)
            
            case "5":
                if verificar_configuracion(lista_inscritos):
                    if lista_inscritos.is_empty():
                        print(f"⚠️ No hay estudiantes inscritos en '{lista_inscritos.list_name}' para retirar. ⛔")
                    else:
                        print(f"\n=== Retiro de inscripción: {lista_inscritos.list_name} ===")
                        print(liberar_cupo(lista_inscritos, cola_prioridad, cola_circular, historial_acciones))
            
            case "6":
                if verificar_configuracion(lista_inscritos):
                    print(f"\n=== Casos prioritarios para: {lista_inscritos.list_name} ===")
                    atender_casos_prioritarios(cola_prioridad, cola_circular, lista_inscritos, historial_acciones)
            
            case "7":
                print("\n=== Deshacer última acción ↩️")
                print(deshacer_accion(cola_simple, cola_prioridad, cola_circular, lista_inscritos, historial_acciones))
            
            case "8":
                mostrar_historial(historial_acciones)
            
            case "9":
                print("Saliendo...🚪")
                break
            
            case _:
                print("Opción no válida. Intente nuevamente. ⛔")


# ==================== FUNCIONES DE VALIDACIÓN ====================

def validar_input(texto: str) -> str:
    """
    Valida que la entrada de texto no esté vacía.
    
    Proceso:
    1. Solicita entrada al usuario
    2. Verifica que no esté vacía o solo espacios en blanco
    3. Repite hasta obtener una entrada válida
    """
    while True:
        valor = input(texto)
        if valor.strip():
            return valor
        print("Entrada no válida. Por favor, ingrese un valor no vacío. ⛔")


def verificar_configuracion(curso: ListaEnlazada) -> bool:
    """
    Verifica si el curso está configurado antes de permitir operaciones.
    
    Retorna:
    - True: Si el curso tiene nombre y cupos definidos
    - False: Si el curso no está configurado (muestra mensaje de error)
    """
    if not curso.is_course_configurated:
        print("Configure el curso antes de realizar esta acción. ⚠️")
        return False
    return True


def validar_numero_entero(mensaje: str, min_val: int = None, max_val: int = None) -> int:
    """
    Valida que la entrada sea un número entero dentro de un rango opcional.
    
    Parámetros:
    - mensaje: Texto a mostrar al solicitar el valor
    - min_val: Valor mínimo permitido (opcional)
    - max_val: Valor máximo permitido (opcional)
    
    Retorna:
    - El número entero validado
    """
    while True:
        try:
            valor = int(validar_input(mensaje))
            if (min_val is not None and valor < min_val) or (max_val is not None and valor > max_val):
                rango = f" entre {min_val} y {max_val}" if min_val is not None and max_val is not None else (f" >= {min_val}" if min_val is not None else f" <= {max_val}")
                print(f"Valor fuera de rango⛔. Debe ser{rango}.")
                continue
            return valor
        except ValueError:
            print("Error: Debe ingresar un número entero válido. ⛔")


# ==================== FUNCIONES DE OPERACIONES ====================

def configurar_curso(curso: ListaEnlazada, historial: Stack):
    """
    Configura un nuevo curso con nombre y número de cupos.
    
    Proceso:
    1. Solicita el nombre del curso
    2. Solicita el número de cupos (mínimo 1)
    3. Guarda la configuración en la lista de inscritos
    4. Registra la acción en el historial para poder deshacer
    
    Nota: Solo puede configurarse una vez (no se puede modificar después).
    """
    nombre_curso = validar_input("Ingrese el nombre del curso: ")
    curso.list_name = nombre_curso
    cupos = validar_numero_entero("Ingrese el número de cupos disponibles: ", min_val=1)
    curso.max_size = cupos
    
    # Registrar acción en el historial para deshacer
    accion = Accion(
        tipo="configurar_curso",
        datos={"nombre_curso": nombre_curso, "cupos": cupos},
        descripcion=f"Configurar curso '{nombre_curso}' con {cupos} cupos"
    )
    historial.push(accion)
    
    return f"Curso '{nombre_curso}' configurado exitosamente con {cupos} cupos. ✅"


def registrar_llegada_estudiante(cola_simple: ColaSimple, cola_prioridad: ColaPrioridad, historial: Stack) -> str:
    """
    Registra la llegada de un nuevo estudiante al sistema.
    
    Proceso:
    1. Solicita nombre y cédula del estudiante
    2. Pregunta si tiene prioridad
    3. Dirige a la función correspondiente (normal o prioridad)
    
    Esta función actúa como distribuidor según el tipo de estudiante.
    """
    nombre = validar_input("Ingrese el nombre del estudiante: ")
    ci = validar_input("Ingrese la cédula de identidad del estudiante: ")
    has_prioridad = (
        validar_input("¿El estudiante tiene prioridad? (s/n): ").lower() == "s"
    )
    nuevo_estudiante = Estudiante(nombre, ci)
    
    if has_prioridad:
        return registrar_estudiante_prioridad(nuevo_estudiante, cola_prioridad, historial)
    else:
        return registrar_estudiante_normal(nuevo_estudiante, cola_simple, historial)


def registrar_estudiante_normal(
    nuevo_estudiante: Estudiante, cola_simple: ColaSimple, historial: Stack
) -> str:
    """
    Registra un estudiante sin prioridad en la cola simple (FIFO).
    
    El estudiante se agrega al final de la cola simple.
    Se registra la acción para poder deshacer después.
    """
    cola_simple.enqueue(nuevo_estudiante)
    
    # Registrar acción en el historial para deshacer
    accion = Accion(
        tipo="enqueue_normal",
        datos={"estudiante": nuevo_estudiante},
        descripcion=f"Registro de estudiante normal: {nuevo_estudiante.nombre} (CI: {nuevo_estudiante.ci_estudiante})"
    )
    historial.push(accion)
    
    return f"↳ ENQUEUE estudiante normal: {nuevo_estudiante.nombre} (CI: {nuevo_estudiante.ci_estudiante}) 🔈"


def registrar_estudiante_prioridad(
    nuevo_estudiante: Estudiante, cola_prioridad: ColaPrioridad, historial: Stack
) -> str:
    """
    Registra un estudiante con prioridad en la cola de prioridad.
    
    Proceso:
    1. Solicita el nivel de prioridad (1-5)
    2. Solicita el motivo de la prioridad
    3. Inserta en la posición correcta según prioridad
    4. Registra la acción para deshacer
    
    Diferencia con estudiante normal:
    - Normal: Va al final de la cola simple
    - Prioridad: Se coloca según su nivel (mayor prioridad = más cerca del frente)
    """
    prioridad = validar_rango_prioridad("Ingrese la prioridad del estudiante (1-5): ")
    motivo_prioridad = validar_input("Ingrese el motivo de prioridad: ")
    cola_prioridad.enqueue(nuevo_estudiante, prioridad, motivo_prioridad)
    
    # Registrar acción en el historial para deshacer
    accion = Accion(
        tipo="enqueue_prioridad",
        datos={"estudiante": nuevo_estudiante, "prioridad": prioridad, "motivo": motivo_prioridad},
        descripcion=f"Registro de estudiante prioritario: {nuevo_estudiante.nombre} (P{prioridad}) - Motivo: {motivo_prioridad}"
    )
    historial.push(accion)
    
    return f"↳ ENQUEUE estudiante con prioridad: {nuevo_estudiante.nombre} (P{prioridad}) - Motivo: {motivo_prioridad} 🚨"

def liberar_cupo(lista_inscritos: ListaEnlazada, cola_prioridad: ColaPrioridad, cola_circular: ColaCircular, historial: Stack) -> str:
    """
    Registra el retiro de un estudiante y reasigna el cupo automáticamente.
    
    Proceso:
    1. Muestra la lista de estudiantes inscritos
    2. Solicita la cédula del estudiante a retirar
    3. Elimina al estudiante de la lista de inscritos
    4. Si hay estudiantes en espera, reasigna el cupo automáticamente:
       - Prioridad: Primero verifica cola_prioridad
       - Si no hay, verifica cola_circular
    5. Registra la acción completa para deshacer
    
    Nota: La reasignación automática prioriza estudiantes con prioridad.
    """
    if lista_inscritos.is_empty():
        return "No hay estudiantes inscritos para retirar. ⛔"
    
    print("\n=== Seleccione el estudiante a retirar ===")
    for id_estudiante, estudiante in lista_inscritos:
        print(f"  • ID {id_estudiante}: {estudiante.nombre} (CI: {estudiante.ci_estudiante})")
    
    ci_estudiante_retirar = validar_input("\nIngrese la cédula del estudiante a retirar: ")
    estudiante_retirado = None
    id_estudiante_retirado = None
    # Busca el estudiante por cedula
    for id_estudiante, estudiante in lista_inscritos:
        if estudiante.ci_estudiante == ci_estudiante_retirar:
            estudiante_retirado = estudiante
            id_estudiante_retirado = id_estudiante
            break
    # Si no encuentra el estudiante
    if estudiante_retirado is None:
        return f"No se encontró un estudiante con cédula {ci_estudiante_retirar}. ⛔"
    # Remueve el estudiante y muestra mensaje
    lista_inscritos.remove(id_estudiante_retirado)
    print(f"✅ Estudiante retirado: {estudiante_retirado.nombre} (CI: {estudiante_retirado.ci_estudiante}). Se ha liberado un cupo.")

    # Datos para la acción (se actualizarán si hay reasignación)
    datos_accion = {
        "estudiante": estudiante_retirado, 
        "id_estudiante": id_estudiante_retirado,
        "reasignado": None
    }

    resultado_reasignacion = ""
    # Reasigna cupo automáticamente si hay alguien esperando
    if not cola_prioridad.is_empty():
        est, prio, mot = cola_prioridad.dequeue()
        lista_inscritos.append(est)
        datos_accion["reasignado"] = {
            "estudiante": est,
            "tipo": "prioridad",
            "prioridad": prio,
            "motivo": mot
        }
        resultado_reasignacion = f"\nCupo reasignado a estudiante prioritario: {est.nombre} (P{prio}) - Motivo: {mot} 🚨"
    elif not cola_circular.is_empty():
        est = cola_circular.dequeue()
        lista_inscritos.append(est)
        datos_accion["reasignado"] = {
            "estudiante": est,
            "tipo": "circular"
        }
        resultado_reasignacion = f"\nCupo reasignado a estudiante en espera: {est.nombre} (CI: {est.ci_estudiante}) 🔈"
    else:
        resultado_reasignacion = "\nCupo liberado exitosamente. No hay estudiantes prioritarios ni en espera para reasignar el cupo. ✅"

    # Registrar la acción completa en el historial
    accion = Accion(
        tipo="liberar_cupo",
        datos=datos_accion,
        descripcion=f"Retiro de inscripción: {estudiante_retirado.nombre} (CI: {estudiante_retirado.ci_estudiante})"
    )
    historial.push(accion)

    return resultado_reasignacion


def mostrar_estado_colas(cola_simple: ColaSimple, cola_prioridad: ColaPrioridad, cola_circular: ColaCircular, lista_inscritos: ListaEnlazada):
    """
    Muestra el estado actual de todas las estructuras de datos.
    
    Información mostrada:
    - Cola prioritaria: Estudiantes esperando con prioridad
    - Cola simple: Estudiantes regulares en espera
    - Cola circular: Estudiantes en espera cuando el curso está lleno
    - Lista de inscritos: Estudiantes matriculados en el curso
    """
    print("\n" + "="*50)
    print(f" 📊 ESTADO ACTUAL: {lista_inscritos.list_name} 📊")
    print("="*50)
    
    # 1. Cola Prioritaria
    print(f"\nCola prioritaria 🚨 ({cola_prioridad.size()}):")
    if cola_prioridad.is_empty():
        print("  (Vacía)")
    else:
        for id_est, est, prioridad, motivo in cola_prioridad:
            print(f"  • ID {id_est}: {est.nombre} (P{prioridad}) - Motivo: {motivo}")

    # 2. Cola Simple
    print(f"\nCola simple 🔈 ({cola_simple.size()}):")
    if cola_simple.is_empty():
        print("  (Vacía)")
    else:
        for id_est, est in cola_simple:
            print(f"  • ID {id_est}: {est.nombre} (CI: {est.ci_estudiante})")

    # 3. Cola Circular (Espera)
    print(f"\nCola circular de espera 🔄 ({cola_circular.size()}):")
    if cola_circular.is_empty():
        print("  (Vacía)")
    else:
        for id_est, est in cola_circular:
            print(f"  • ID {id_est}: {est.nombre} (CI: {est.ci_estudiante})")

    # 4. Lista de Inscritos
    print(f"\nLista de inscritos ✅ ({lista_inscritos.size()}/{lista_inscritos.max_size}):")
    if lista_inscritos.is_empty():
        print("  (No hay estudiantes inscritos aún)")
    else:
        for id_est, est in lista_inscritos:
            print(f"  • ID {id_est}: {est.nombre} (CI: {est.ci_estudiante})")
    
    print("\n" + "="*45)


def mostrar_historial(historial: Stack):
    """
    Muestra el historial de acciones realizadas en el sistema.
    
    El historial se muestra desde la acción más reciente hasta la más antigua.
    Cada acción incluye: hora, tipo y descripción.
    """
    print("\n" + "="*45)
    print(" 📜 HISTORIAL DE ACCIONES 📜")
    print("="*45)
    if historial.is_empty():
        print("  (El historial está vacío)")
    else:
        for accion in historial:
            print(f"  • {accion}")
    print("\n" + "="*45)


def transferir_a_cola_circular(cola_origen, cola_circular: ColaCircular):
    """
    Transfiere todos los estudiantes de una cola a la cola circular.
    
    Se usa cuando el curso está lleno: los estudiantes en espera
    se mueven a la cola circular para esperar cupos disponibles.
    
    Maneja dos tipos de retorno:
    - Tuple: Viene de cola_prioridad (estudiante, prioridad, motivo)
    - Simple: Viene de cola_simple (estudiante)
    """
    while not cola_origen.is_empty():
        # Manejo de retorno según el tipo de cola
        resultado = cola_origen.dequeue()
        if isinstance(resultado, tuple):
            estudiante = resultado[0]
            print(f"Transferido: {estudiante.nombre} (Prioridad: P{resultado[1]}) -> Cola Circular 🔄")
        else:
            estudiante = resultado
            print(f"Transferido: {estudiante.nombre} (CI: {estudiante.ci_estudiante}) -> Cola Circular 🔄")
        cola_circular.enqueue(estudiante)

def atender_turnos(
    cola_simple: ColaSimple, cola_prioridad: ColaPrioridad, cola_circular: ColaCircular, lista_inscritos: ListaEnlazada, historial: Stack
):
    """
    Procesa estudiantes de las colas para inscribirlos en el curso.
    
    Lógica de atención (orden de prioridad):
    1. Primero: Cola de prioridad (estudiantes urgentes)
    2. Segundo: Cola simple (estudiantes regulares)
    
    El proceso continúa hasta:
    - No hay más estudiantes en ninguna cola
    - El curso alcanza su capacidad máxima
    
    Cuando el curso está lleno, los estudiantes restantes se transfieren
    a la cola circular para esperar cupos disponibles.
    
    Cada estudiante atendido se registra individualmente en el historial
    para permitir deshacer cada inscripción por separado.
    """
    if cola_prioridad.is_empty() and cola_circular.is_empty() and cola_simple.is_empty():
        return "No hay estudiantes para atender. ⛔"
    
    while lista_inscritos.size() < lista_inscritos.max_size:
        procesado = False
        
        # Procesar cola prioritaria PRIMERO (mayor urgencia)
        if not cola_prioridad.is_empty():
            estudiante, prioridad, motivo_prioridad = cola_prioridad.dequeue()
            lista_inscritos.append(estudiante)
            # Registrar cada estudiante atendido individualmente en el historial
            accion = Accion(
                tipo="atender",
                datos={
                    "estudiante": estudiante,
                    "tipo": "prioridad",
                    "prioridad": prioridad,
                    "motivo": motivo_prioridad
                },
                descripcion=f"Atender estudiante prioritario: {estudiante.nombre} (P{prioridad})"
            )
            historial.push(accion)
            print(f"Atendiendo estudiante prioritario: {estudiante.nombre} (P{prioridad}) - Motivo: {motivo_prioridad} 🚨")
            procesado = True
        
        # Si hay espacio y cola simple tiene elementos (SEGUNDO)
        elif not cola_simple.is_empty():
            estudiante = cola_simple.dequeue()
            lista_inscritos.append(estudiante)
            # Registrar cada estudiante atendido individualmente en el historial
            accion = Accion(
                tipo="atender",
                datos={
                    "estudiante": estudiante,
                    "tipo": "normal"
                },
                descripcion=f"Atender estudiante normal: {estudiante.nombre} (CI: {estudiante.ci_estudiante})"
            )
            historial.push(accion)
            print(f"Atendiendo estudiante normal: {estudiante.nombre} (CI: {estudiante.ci_estudiante}) 🔈")
            procesado = True
        
        # Si no se procesó nada, salir del ciclo
        if not procesado:
            break
    
    # Si el curso está lleno, transferir estudiantes a cola circular
    if lista_inscritos.size() >= lista_inscritos.max_size:
        print("\nEl curso ha alcanzado su capacidad máxima. No se pueden inscribir más estudiantes. ⚠️")
        if cola_prioridad.is_empty() and cola_simple.is_empty() and cola_circular.is_empty():
            print("No hay estudiantes para transferir a la cola circular. ⛔")
            return
        print("Los siguientes estudiantes serán colocados en la cola circular para esperar su turno:")
        transferir_a_cola_circular(cola_prioridad, cola_circular)
        transferir_a_cola_circular(cola_simple, cola_circular)


def atender_casos_prioritarios(cola_prioridad: ColaPrioridad, cola_circular: ColaCircular, lista_inscritos: ListaEnlazada, historial: Stack):
    """
    Atiende SOLO casos prioritarios y estudiantes en espera (cola circular).
    
    Diferencia con atender_turnos():
    - atender_turnos(): Procesa prioridad Y luego normal
    - atender_casos_prioritarios(): Solo prioridad Y cola circular
    
    Esta opción es útil cuando se quiere dar atención prioritaria
    a los casos urgentes sin procesar estudiantes regulares.
    
    Lógica de atención:
    1. Primero: Cola de prioridad (estudiantes urgentes)
    2. Segundo: Cola circular (estudiantes en espera)
    """
    if lista_inscritos.size() >= lista_inscritos.max_size:
        print("\nEl curso ha alcanzado su capacidad máxima. No se pueden inscribir más estudiantes. ⚠️")
        return

    if cola_prioridad.is_empty() and cola_circular.is_empty():
        print("No hay estudiantes para atender. ⛔")
        return
    
    while lista_inscritos.size() < lista_inscritos.max_size:
        procesado = False
        
        # Procesar cola prioritaria PRIMERO
        if not cola_prioridad.is_empty():
            estudiante, prioridad, motivo_prioridad = cola_prioridad.dequeue()
            lista_inscritos.append(estudiante)
            # Registrar cada estudiante atendido individualmente en el historial
            accion = Accion(
                tipo="atender_prioritario",
                datos={
                    "estudiante": estudiante,
                    "tipo": "prioridad",
                    "prioridad": prioridad,
                    "motivo": motivo_prioridad
                },
                descripcion=f"Atender caso prioritario: {estudiante.nombre} (P{prioridad})"
            )
            historial.push(accion)
            print(f"Atendiendo estudiante prioritario: {estudiante.nombre} (P{prioridad}) - Motivo: {motivo_prioridad} 🚨")
            procesado = True
        
        # Si hay espacio y cola circular tiene elementos (SEGUNDO)
        elif not cola_circular.is_empty():
            estudiante = cola_circular.dequeue()
            lista_inscritos.append(estudiante)
            # Registrar cada estudiante atendido individualmente en el historial
            accion = Accion(
                tipo="atender_prioritario",
                datos={
                    "estudiante": estudiante,
                    "tipo": "circular"
                },
                descripcion=f"Atender estudiante en espera: {estudiante.nombre} (CI: {estudiante.ci_estudiante})"
            )
            historial.push(accion)
            print(f"Atendiendo estudiante en cola circular: {estudiante.nombre} (CI: {estudiante.ci_estudiante}) 🔄")
            procesado = True
        
        # Si no se procesó nada, salir del ciclo
        if not procesado:
            break

    # Si el curso está lleno, transferir estudiantes restantes a cola circular
    if lista_inscritos.size() >= lista_inscritos.max_size:
        print("\nEl curso ha alcanzado su capacidad máxima. No se pueden inscribir más estudiantes. ⚠️")
        print("Los siguientes estudiantes serán colocados en la cola circular para esperar su turno:")
        transferir_a_cola_circular(cola_prioridad, cola_circular)


def validar_rango_prioridad(prioridad: str) -> int:
    return validar_numero_entero(prioridad, min_val=1, max_val=5)


def deshacer_accion(cola_simple: ColaSimple, cola_prioridad: ColaPrioridad, cola_circular: ColaCircular, lista_inscritos: ListaEnlazada, historial: Stack) -> str:
    """Deshace la última acción registrada en el historial."""
    
    if historial.is_empty():
        return "No hay acciones para deshacer. ⛔"
    
    # Confirmar deshacer
    print(f"Última acción: {historial.peek()}")
    confirm = validar_input("¿Está seguro que desea deshacer la última acción? (s/n): ").lower()
    
    if confirm != "s":
        return "Operación de deshacer cancelada. ⛔"
    
    # Extraer la acción del historial
    accion = historial.pop()
    
    # Procesar según el tipo de acción
    match accion.tipo:
        case "configurar_curso":
            # Reiniciar la configuración del curso
            lista_inscritos.list_name = None
            lista_inscritos.max_size = 0
            return f"Acción deshecha: Se ha eliminado la configuración del curso '{accion.datos['nombre_curso']}'. ✅"
        
        case "enqueue_normal":
            # Eliminar al estudiante de la cola simple
            estudiante = accion.datos["estudiante"]
            # Buscar y eliminar el estudiante de la cola simple
            for id_est, est in cola_simple:
                if est.ci_estudiante == estudiante.ci_estudiante:
                    cola_simple.remove_by_ci(estudiante.ci_estudiante)
                    return f"Acción deshecha: Estudiante normal '{estudiante.nombre}' (CI: {estudiante.ci_estudiante}) eliminado de la cola. ✅"
            return f"No se pudo deshacer: Estudiante '{estudiante.nombre}' no encontrado en la cola. ⛔"
        
        case "enqueue_prioridad":
            # Eliminar al estudiante de la cola de prioridad
            estudiante = accion.datos["estudiante"]
            prioridad = accion.datos["prioridad"]
            # Buscar y eliminar el estudiante de la cola de prioridad
            for id_est, est, p, m in cola_prioridad:
                if est.ci_estudiante == estudiante.ci_estudiante:
                    cola_prioridad.remove_by_ci(estudiante.ci_estudiante)
                    return f"Acción deshecha: Estudiante prioritario '{estudiante.nombre}' (P{prioridad}) eliminado de la cola. ✅"
            return f"No se pudo deshacer: Estudiante '{estudiante.nombre}' no encontrado en la cola de prioridad. ⛔"
        
        case "atender" | "atender_prioritario":
            # Eliminar al estudiante de la lista de inscritos
            estudiante = accion.datos["estudiante"]
            tipo = accion.datos["tipo"]
            
            # Buscar y eliminar el estudiante de la lista de inscritos
            for id_est, est in lista_inscritos:
                if est.ci_estudiante == estudiante.ci_estudiante:
                    lista_inscritos.remove(id_est)
                    # Regresar el estudiante a su cola correspondiente
                    if tipo == "prioridad":
                        prioridad = accion.datos.get("prioridad", 1)
                        motivo = accion.datos.get("motivo", "")
                        cola_prioridad.enqueue(estudiante, prioridad, motivo)
                        return f"Acción deshecha: Estudiante prioritario '{estudiante.nombre}' removido de inscritos y regresado a cola de prioridad. ✅"
                    elif tipo == "normal":
                        cola_simple.enqueue(estudiante)
                        return f"Acción deshecha: Estudiante normal '{estudiante.nombre}' removido de inscritos y regresado a cola simple. ✅"
                    elif tipo == "circular":
                        cola_circular.enqueue(estudiante)
                        return f"Acción deshecha: Estudiante '{estudiante.nombre}' removido de inscritos y regresado a cola circular. ✅"
            return f"No se pudo deshacer: Estudiante '{estudiante.nombre}' no encontrado en la lista de inscritos. ⛔"
        
        case "liberar_cupo":
            # 1. Deshacer reasignación si existió
            reasignado = accion.datos.get("reasignado")
            msg_reasignacion = ""
            if reasignado:
                est_r = reasignado["estudiante"]
                # Buscar y eliminar al reasignado de la lista de inscritos
                for id_est, est in lista_inscritos:
                    if est.ci_estudiante == est_r.ci_estudiante:
                        lista_inscritos.remove(id_est)
                        # Devolverlo a su cola original
                        if reasignado["tipo"] == "prioridad":
                            cola_prioridad.enqueue(est_r, reasignado["prioridad"], reasignado["motivo"])
                            msg_reasignacion = f"Estudiante reasignado '{est_r.nombre}' regresado a cola prioritaria."
                        else:
                            cola_circular.enqueue(est_r)
                            msg_reasignacion = f"Estudiante reasignado '{est_r.nombre}' regresado a cola circular."
                        break
            
            # 2. Reintegrar al estudiante originalmente retirado
            estudiante_original = accion.datos["estudiante"]
            lista_inscritos.append(estudiante_original)
            
            final_msg = f"Acción deshecha: Estudiante '{estudiante_original.nombre}' reintegrado a inscritos. ✅"
            if msg_reasignacion:
                final_msg += f"\n↳ {msg_reasignacion}"
            return final_msg
        
        case _:
            return f"Tipo de acción desconocido: {accion.tipo}. No se puede deshacer. ⛔"


# Función principal que inicia el menú de operaciones
def main():
    main_menu()

# Punto de entrada del programa
if __name__ == "__main__":
    main()
