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
    return f"Curso '{nombre_curso}' configurado exitosamente. ✅"


def registrar_alerta(
    tipo: str, cola_simple: ColaSimple, cola_prioridad: ColaPrioridad
) -> str:
    match tipo:
        case "normal":
            return registrar_alerta_normal(cola_simple)
        case "critica":
            return registrar_alerta_critica(cola_prioridad)

    return "Tipo de alerta no reconocido. ⛔"


def registrar_alerta_normal(cola_simple: ColaSimple) -> str:
    alerta = validar_input("Ingrese la descripción de la alerta 🔈: ")
    cola_simple.enqueue(alerta)
    return "↳ ENQUEUE alerta normal: " + alerta + " 🔈"


def registrar_alerta_critica(cola_prioridad: ColaPrioridad) -> str:
    alerta = validar_input("Ingrese la descripción de la alerta 🚨: ")
    prioridad = validar_rango_prioridad("Ingrese la prioridad de la alerta (1-5): ")
    cola_prioridad.enqueue(alerta, prioridad)
    return "↳ ENQUEUE alerta crítica: " + alerta + " 🚨"


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
