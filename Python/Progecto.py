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

def registrar_alumno(self):     # metodo para registrar alumno por medio de inputs en consola
     print("/n--- Registrar Alumno ---")
     cedula = input("Ingrese su CI: ").strip()
     if any(a.cedula == cedula for a in self.alumnos):   # Evita duplicados por numero de Cedula
          print("Ya hay un alumno con esa Cedula registado.")
          return
     nombre = input("Nombre completo: ").strip()
     correo = input ("Correo electrónico: ").strip()
     print("Programas académicos displonibles: Curso, Diplomado, Bootcamp")
     tipo_programa = input("Tipo de Programa: ").strip().capitalize()
     if tipo_programa not in ["Curso", "Diplomado", "Bootcamp"]:   # metodo en caso de que la opcion seleccionada no este disponible
          print(" Programa Académico no reconocido. Inscribiendo en 'Curso' por defecto.")
          tipo_programa = "Curso"

nuevo_alumno = Alumno(cedula, nombre, correo, tipo_programa)
self.alumnos.append(nuevo_alumno)
self.guardar_alumnos()
print("Alumno registrado con éxito.")

def registrar_profesor(self):
     print("/n--- Registrar Profesor ---")
     cedula = input("Cédula: ").strip()
     if any(p.cedula == cedula for p in self.profesores):
          print(" Ya existe un profesor registrado con esa Cédula.") #Evitamos duplicados
          return
     nombre = input("Nombre Completo: ").strip()
     correo = input("Correo Electrónico: ").strip()
     especialidad = input("Especialidad: ").strip()
     materia = input("Materia: ").strip()

nuevo_profesor = Profesor(cedula, nombre, correo, especialidad, materia)
self.profesores.append(nuevo_profesor)
self.guardar_profesores()
print("Profesor registrado con éxito")

def registrar_nota(self):   # Metodo para registrar notas de alumno
     print("/n--- Registrar Nota ---")       
     cedula = input("Ingrese la Cédula del Alumno: ").strip()     # input en consola para la busqueda
     alumno = next((a for a in self.alumnos if a.cedula == cedula),None)  # busqueda de alumno con expresion next (verifica dentro de la lista) si no encuentra devuelve None

     if not alumno:         #En caso de no encontrart en la lista hacemos print del error1
          print(" Alumno no encontrado en el sistema.")
          return

     if len(alumno.notas) >= 3:   # Verificacion en caso de intentar registrar mas de 3 notas
          print("Límite de notas registrado (3).")
          return

     try:
          nota= float(input)f"ingrese la calificación para {alumno.nombre} (0 a 20): "))  # input para ingresar nota
          if not (0 <= nota <= 20):   # filtro para evitar numeros o caracteres invalidos
               print("La nota debe de estar entre 0 y 20.")
               returnexcept ValueError:
               print(" Por favor ingresar un valor válido.")
               return

          alumno.notas.append(nota) # agregamos notas
          self.pila_notas.append((cedula, nota)) # Pila LIFO (undo action)
          self.guardar_alumnos()
          print(f"Nota de {nota} registrada para a {alumno.nombre}.")

          def deshacer_ultimo_registro_nota(self):
               print("/n--- Deshacer último registro de nota ---")
               if not self.pila_notas:        # sin acciones guardadas, hacemos print del error
                    print("No hay registtro de notas para deshacer.")
                    return

               cedula, nota_removida = selff.pila_notas.pop()  #extraer cima de la pila (LIFO)
               alumno = next((a for in self.alumnos if a.cedula == cedula), None)
               if alumno and nota_removida in alumno.notas:
                    alumno.notas.remove(nota_removida)
                    self.guardar_alumnos()
                    print(f"Se removió la nota {nota_removida} del alumno {alumno.nombre}")
               else:                                                                                 
                    print("No se pudo localizar el registro exacto en el alumno correspondiente")      #print de error en vez de romper el programa

                    def grnerar_cola_certificados(self):
                         print("/n--- Generar Cola de Certificados---")
                         cola_certificados = deque()   # Cola first in first out
                         for alumno in self.alumnos:
                              if alumno.evaluar_aprobacion():
                                   cola_certificados.append(alumno)

                                   self.guardar_alumnos()

                                   if not cola_certificados()
                                   print("No hay alumnos que cumplan con los criterios de aprobación en este momento.")
                                   return

                                   print(f"Procesando Cola de Certificados (Total candidatos:{len(cola_certificados)})...")
                                   try:
                                        with open(self.archivo_certificados, "w", encoding="utf-8") as f:

                                              f.write("=========================================\n")
                f.write("REPORTE DE CERTIFICADOS PENDIENTES\n")
                f.write("=========================================\n")
                f.write(f"Total de graduandos en cola: {len(cola_certificados)}\n")

               contador = 1
               while cola_certificados:        # Bucle While se mantiene activo mientras se encuentren procesos en cola         
                    graduando = cola_certificados.popleft() #   FIFO
                    regla_extra = " (Cumple regla de ninguna nota < 14)"  # destacar en el archivo txt  alumnos de Bootcamp que cumplieron con ;a exigencia académica
                    if graduando.tipo_programa == "Bootcamp" else ""

f.write(f"{contador}. [{graduando.cedula}] {graduando.nombre}\n")
                    f.write(f"   - Programa: {graduando.tipo_programa}\n")
                    f.write(f"   - Promedio Final: {graduando.calcular_promedio():.1f}\n")
                    f.write(f"   - Estatus: APROBADO{regla_extra}\n")
                    
                    print(f" -> Procesado y agregado a cola: {graduando.nombre} ({graduando.tipo_programa})")
                    contador += 1      #     sumar 1 al contador (para enumnerar al siguiente estudiante en el reporte de manera correcta)

                       f.write("=========================================\n")
                f.write("- Fin del reporte - Generado por SGA-DO *\n")
            print(f"Cola procesada con éxito. Archivo generado: '{self.archivo_certificados}'.")
        except Exception as e:   # Este bloque atrapa la excepcion (cualquier tipo de error) y muestra el mensaje en el terminal
            print(f"Error al exportar certificados: {e}")








