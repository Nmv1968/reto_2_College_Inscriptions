from cola_simple import ColaSimple
from cola_prioridad import ColaPrioridad
from cola_circular import ColaCircular
from estudiante import Estudiante
from lista_enlazada import ListaEnlazada


def inscriptionMenu():
    cola_simple = ColaSimple()
    cola_prioridad = ColaPrioridad()
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
                print(configurar_curso(lista_inscritos))
            case "2":
                print("\n=== Registro de llegada de estudiante ===")
                if (
                    lista_inscritos.get_list_name() is None
                    and lista_inscritos.get_list_max_size() is None
                ):
                    print("⚠️ Configure el curso antes de registrar estudiantes.")
                else:
                    print(enqueue_estudiante(cola_simple, cola_prioridad))
            case "4":
                print("\n=== Estado actual de inscritos y colas ===")
                print("\n=== Estado de las colas ===")
                print(
                    f"Cola simple 🔈 ({cola_simple.size()}): {[valor for valor in cola_simple]}"
                )
                print(
                    f"Cola prioritaria 🚨 ({cola_prioridad.size()}): {[f'{estudiante.nombre} (P{prioridad})' for estudiante, prioridad, motivo in cola_prioridad]}"
                )
                print("\n=== Lista de inscritos ===")
                if lista_inscritos.is_empty():
                    print("No hay estudiantes inscritos aún. ⛔")
                else:
                    print(
                        f"Estudiantes inscritos: ({lista_inscritos.size()}): {[f'{estudiante.nombre} (CI: {estudiante.ci_estudiante})' for estudiante in lista_inscritos]}"
                    )
            case "5":
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


def enqueue_estudiante(cola_simple: ColaSimple, cola_prioridad: ColaPrioridad) -> str:
    nombre = validar_input("Ingrese el nombre del estudiante: ")
    ci = validar_input("Ingrese la cédula de identidad del estudiante: ")
    has_prioridad = (
        validar_input("¿El estudiante tiene prioridad? (s/n): ").lower() == "s"
    )
    nuevo_estudiante = Estudiante(nombre, ci)
    if has_prioridad:
        return registrar_estudiante_prioridad(nuevo_estudiante, cola_prioridad)
    else:
        return registrar_estudiante_normal(nuevo_estudiante, cola_simple)


def registrar_estudiante_normal(
    nuevo_estudiante: Estudiante, cola_simple: ColaSimple
) -> str:
    cola_simple.enqueue(nuevo_estudiante)
    return f"↳ ENQUEUE estudiante normal: {nuevo_estudiante.nombre} 🔈"


def registrar_estudiante_prioridad(
    nuevo_estudiante: Estudiante, cola_prioridad: ColaPrioridad
) -> str:
    prioridad = validar_rango_prioridad("Ingrese la prioridad del estudiante (1-5): ")
    motivo_prioridad = validar_input("Ingrese el motivo de prioridad: ")
    cola_prioridad.enqueue(nuevo_estudiante, prioridad, motivo_prioridad)
    return f"↳ ENQUEUE estudiante con prioridad: {nuevo_estudiante.nombre} (P{prioridad}) - Motivo: {motivo_prioridad} 🚨"


def atender_siguiente_alerta(
    cola_simple: ColaSimple, cola_prioridad: ColaPrioridad
) -> str:
    if not cola_prioridad.is_empty():
        valor, prioridad = cola_prioridad.dequeue()
        return f"Atendiendo alerta crítica: {valor} (P{prioridad}) 🚨"
    elif not cola_simple.is_empty():
        return f"Atendiendo alerta normal: {cola_simple.dequeue()} 🔈"
    else:
        return "No hay alertas para atender. ⛔"


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
