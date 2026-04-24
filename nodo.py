"""
================================================================================
MÓDULO: nodo.py
================================================================================
Este módulo define la clase Nodo, que es la UNIDAD BÁSICA de todas las 
estructuras de datos enlazadas usadas en este proyecto.

Cada elemento (nodo) contiene:
  1. UN VALOR/DATO: La información que queremos almacenar (en nuestro caso, un Estudiante)
  2. UN PUNTERO (siguiente): La referencia al siguiente nodo en la cadena

Esta forma de organizar datos permite insertar y eliminar elementos de forma eficiente sin necesidad de reorganizar toda la estructura.
================================================================================
"""

import uuid
from estudiante import Estudiante


class Nodo:
    """
    Atributos:
    - id_estudiante: Identificador único generado automáticamente (UUID)
    - estudiante: Objeto Estudiante que contiene los datos del estudiante
    - prioridad: Nivel de prioridad (1-5), usado solo en colas de prioridad
    - motivo_prioridad: Razón por la cual el estudiante tiene prioridad
    - siguiente: Referencia al siguiente nodo en la cadena (None si es el último)
    - valor: Atributo genérico para uso en la pila de historial
    """
    
    def __init__(self, estudiante: Estudiante = None, prioridad: int = None, motivo_prioridad: str = None):
        # Genera un ID único para cada nodo 
        self.id_estudiante = str(uuid.uuid4())
        
        # El dato principal que almacena el nodo
        self.estudiante = estudiante
        
        # Campos específicos para estudiantes con prioridad
        self.prioridad = prioridad          # 1=bajo, 5=crítico
        self.motivo_prioridad = motivo_prioridad  # Razón de la prioridad
        
        # PUNTERO al siguiente nodo (inicialmente None, se enlaza después)
        self.siguiente = None
        
        # Atributo genérico para uso en la pila de historial (Stack)
        self.valor = None
