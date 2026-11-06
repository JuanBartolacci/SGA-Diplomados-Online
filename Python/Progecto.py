import os
from collections import deque

class Persona:   # Super clase, de esta se va a derivar estudiantes y profesores
    def __init__(self, cedula, nombre, correo):
        self.cedula = cedula
        self.nombre = nombre
        self.correo = correo

def evaluar(self, notas): # Jerarquia o tipos de programas academicos
    raise NotImplementedError  # para que ProgramaAcademico sea una clase abstracta y quitar el dolor de cabeza de tener que implementar el metodo evaluar en cada subclase

class Curso(ProgramaAcademico): # clase hija de ProgramaAcademico
    def evaluar(self, notas):
        if not notas: # Para evitar que divida entre 0
            return False
        promedio = sum(notas) / len(notas)
        return promedio >= 10 # Curso necesita promedio de 10 o mayor

    class Diplomado(ProgramaAcademico): # clase hija de ProgramaAcademico
        def evaluar(self,notas):
            if not notas:
                return False
            promedio = sum(notas) / len(notas)
            return promedio >= 14 # Diplomado necesita promedio de 14 o mas

        class BootCamp(ProgramaAcademico): # clase hija de ProgramaAcademico
            def evaluar(self, notas):
                if not notas:
                    return False
                return all(n >= 14 for n in notas) # Revisar todas las notas, tienen que ser mayor o =a 14

       class Alumno(Persona): # calse hija de Persona
        def__init__(self, cedula, nombre, correo, tipo_programa, notas=None, estatus="En Curso"):
            super().__init__(cedula, nombre, correo) # Herencia de Persona
            self.tipo_programa = tipo_programa # curso, diplomado o bootcamp
            self.notas notas if notas is not None else []
            self.estatus = estatus
            self._estrategia_programa = self._obtener_estrategia_programa() 

def _obtener_estrategia_programa(self): # obtener forma de evaluar segun el tipo de programa academicof
            if self.tipo_programa == "Diplomado":
                 return Diplomado()
            elif self.tipo_programa =="BootCamp":
                 return BootCamp()
            else:
                 return Curso() # default, si noes ninguno de los de arriba


