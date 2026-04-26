# 🏫 Sistema de Gestión de Inscripciones Universitarias

Este proyecto es un simulador de gestión de inscripciones universitarias desarrollado para la materia de **Estructuras de Datos**. El sistema utiliza múltiples estructuras de datos dinámicas (implementadas desde cero mediante nodos) para gestionar de forma eficiente y justa el flujo de estudiantes hacia un curso con cupos limitados.

## 🚀 Características Principales

- **Gestión Multi-Estructura:** Uso coordinado de Colas Simples, de Prioridad, Circulares y Listas Enlazadas.
- **Priorización Inteligente:** Atención preferencial a casos especiales (becas, último semestre, etc.) mediante una jerarquía de niveles (1-5).
- **Lista de Espera Dinámica:** Los estudiantes excedentes son gestionados en una cola circular para ocupar vacantes automáticas ante retiros.
- **Sistema de Deshacer (Undo):** Capacidad de revertir acciones y restaurar el estado previo de todas las colas mediante una Pila (Stack).
- **Validación Robusta:** Control estricto de entradas de usuario para evitar errores de tipo o valores vacíos.
- **Identificadores Únicos:** Generación automática de UUIDs para cada nodo/estudiante.

## 📁 Estructura del Proyecto

- `main.py`: Punto de entrada del programa y orquestador de la lógica de negocio.
- `estudiante.py`: Definición del modelo de datos `Estudiante`.
- `nodo.py`: Clase base para la creación de nodos dinámicos.
- `cola_simple.py`: Implementación de cola FIFO para estudiantes regulares.
- `cola_prioridad.py`: Gestión de estudiantes con niveles de prioridad.
- `cola_circular.py`: Manejo de la lista de espera cíclica.
- `lista_enlazada.py`: Registro de estudiantes inscritos con control de cupos.
- `stack.py`: Pila para el almacenamiento del historial de acciones.
- `diagrama_flujo_colas.html`: Visualización gráfica y técnica del flujo del sistema.

## 🛠️ Requisitos e Instalación

1.  **Python 3.10+**: El proyecto utiliza características modernas como `match-case` y `dataclasses`.
2.  No requiere dependencias externas (solo bibliotecas estándar de Python como `uuid` y `datetime`).

### Ejecución:
Para iniciar el sistema, simplemente ejecuta el archivo principal:
```bash
python main.py
```

## 🧠 Lógica de Funcionamiento

1.  **Configuración:** Se define el curso y su capacidad máxima.
2.  **Registro:** Los estudiantes llegan y se clasifican según su prioridad.
3.  **Inscripción:** Se procesan los turnos (Prioridad > Simple). Si el curso se llena, los estudiantes restantes pasan a la cola de espera circular.
4.  **Retiros:** Al retirar a un inscrito, el sistema busca automáticamente un reemplazo prioritario o de la lista de espera.
5.  **Historial:** Todas las operaciones críticas se guardan en el historial para permitir su reversión.

---
**Desarrollado como parte del Reto 2 de Estructuras de Datos - PUCE 2026**
