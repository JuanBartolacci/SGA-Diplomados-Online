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

def calcular_promedio(self):
     if not self.notas:
          return 0.0
     return sum(self.notas) / len(self.notas)

def evaluar_aprobacion(self):  # Metodo para evaluar aprobacion (polimorfismo)
     if self._estrategia_programa.evaluar(self.notas):
          self.estatus = "Aprobado"
          return True
     else:                                # else (false)
          self.estatus = "Reprobado"
          return False

def a_string_archivo(self):        #metodo para guardar en txt
     notas_str = ",".join(map(str, self.notas)) if self.notas else ""
     return
f"{self.cedula},{self.nombre},{self.correo},{self.tipo_programa},{nnotas_srr},{self.estatus}/n"  # F-string para toda la informacion de alumnos

class Profesor(Persona): # clase hija de Persona
     def __init__(self, cedula, nombre, correo , especialidad, materia):  
          super().__init__(cedula, nombre, correo)  # Herencia de persona
          self.especialidad = especialidad   
          self.materia = materia               # Nuevos atributos para la clase Profesor

    def a_string_archivo(self):  # metodo para guardar en txt
        return
f"{self.cedula},{self.nombre},{self.correo},{self.especialidad},{seldf.materia}/n"


class SistemaGestion:
     def __init__(self):
     self.alumnbos = []
     self.profesores = []
     self.pila_notas = deque()         # Stack Last in first out, para guardar acciones de notas (deshacer)
     self.archivo_alumnos = "alumnos.txt"
     self.archivo_profesores = "profesores.txt"
     self.archivo_certificados = "certificados_pendientes.txt"
     self.cargar_datos() #             

     def cargar_datos(self):  # Metodo para cargar datos de alumnos y profesores desde archivos
          if os.path.exists(self.archivo_alumnos):        # Verificar si el archivo de alumnos existe
             try:
                  with open(self.archivo_alumnos, "r", encoding="utf-8") as f:        # leer el archivo alumnos (read) linea por linea (utf-8)
                  for linea in f:
                       linea = linea.strip()
                       if not linea:
                            continue
                       partes = linea.split(",")
                       if len(partes) >= 6:
                            cedula, nomnre, correo, tipo_progama, notas_str, estatus + partes[0], partes[1], partes[2], partes[3], partes[4], partes[5]
                            notas_str, estatus = partes[0], partes[1], partes[2], partes[3], partes[4], partes[5]
                            notas = [float(n) for n in notas_str.split(",") if notas_str else []]
                            self.alumnos.append(Alumno(cedula, nombre, correo, tipo_programa, notas, estatus))
             except Exception as e:
                  print(f"Error al cargar datos de alumnos: {e}")

                  if os.path.exists(self.archivo_profesores):  # Verificar si el archivo de profesores existe
                       try:
                            with open(self.archivo_profesores, "r", encoding="utf-8") as f:  # leer el archivo profesores (read) linea por linea (utf-8)
                                 for linea in f:
                                      linea = linea.strip()
                                      if not linea:
                                           continue
                                      partes = linea.split(",")
                                      if len(partes) >= 5:
                                           cedula, nombre, correo, especialidad, materia = partes[0], partes[1], partes[2], partes[3], partes[4]
                                           self.profesores.append(Profesor(cedula, nombre, correo, especialidad, materia)) 
                                           except Exception as e:
                                                print(f"Error al cargar datos de profesores: {e}")

                                    def guardar_alumnos(self): # overload, guardar alumnos en txt
                                      try:
                                           with open(self.archivo_alumnos, "w", encoding="utf-8") as f: # Write (w) en vez de read (r) para guardar los datos de alumnos en el archivo
                                                for alumno in self.alumnos:
                                                     f.write(alumno.a_string_archivo())
                                            except Exception as e:
                                                 print(f"Error al guardar alumnos: {e}")         

      def guardar_profesores(self): # overload, guardar profesores en txt
          try:
                   with open(self.archivo_profesores, "w", encoding="utf-8") as f:  # Write (w) en vez de read (r) para guardar los datos de profesores en el archivo
                        for profesor in self.profesores:
                             f.write(profesor.a_string_archivo())
                except Exception as e:
                     print(f"Error al guardar profesores: {e}")                                   
