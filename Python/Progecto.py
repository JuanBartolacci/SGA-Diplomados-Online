import os
from collections import deque

class Persona:
    def __init__(self, cedula, nombre, correo):
        self.cedula = cedula
        self.nombre = nombre
        self.correo = correo

# Jerarquía de Programas Académicos (Polimorfismo Real)
class ProgramaAcademico:
    def evaluar(self, notas):
        raise NotImplementedError

class Curso(ProgramaAcademico):
    def evaluar(self, notas):
        if not notas:
            return False
        promedio = sum(notas) / len(notas)
        return promedio >= 10

class Diplomado(ProgramaAcademico):
    def evaluar(self, notas):
        if not notas:
            return False
        promedio = sum(notas) / len(notas)
        return promedio >= 14

class Bootcamp(ProgramaAcademico):
    def evaluar(self, notas):
        if not notas:
            return False
        # Exige estrictamente que ninguna nota individual sea menor a 14
        return all(n >= 14 for n in notas)

class Alumno(Persona):
    def __init__(self, cedula, nombre, correo, tipo_programa, notas=None, estatus="En Curso"):
        super().__init__(cedula, nombre, correo)
        self.tipo_programa = tipo_programa # Curso, Diplomado o Bootcamp
        self.notas = notas if notas is not None else []
        self.estatus = estatus
        self._estrategia_programa = self._obtener_estrategia()

    def _obtener_estrategia(self):
        if self.tipo_programa == "Diplomado":
            return Diplomado()
        elif self.tipo_programa == "Bootcamp":
            return Bootcamp()
        else:
            return Curso()

    def calcular_promedio(self):
        if not self.notas:
            return 0.0
        return sum(self.notas) / len(self.notas)

    def evaluar_aprobacion(self):
        # Aplica polimorfismo llamando a la regla específica del programa
        if self._estrategia_programa.evaluar(self.notas):
            self.estatus = "Aprobado"
            return True
        else:
            self.estatus = "Reprobado"
            return False

    def a_string_archivo(self):
        notas_str = ",".join(map(str, self.notas)) if self.notas else ""
        return f"{self.cedula},{self.nombre},{self.correo},{self.tipo_programa},{notas_str},{self.estatus}\n"

class Profesor(Persona):
    def __init__(self, cedula, nombre, correo, especialidad, materia):
        super().__init__(cedula, nombre, correo)
        self.especialidad = especialidad
        self.materia = materia

    def a_string_archivo(self):
        return f"{self.cedula},{self.nombre},{self.correo},{self.especialidad},{self.materia}\n"

class SistemaGestion:
    def __init__(self):
        self.alumnos = []
        self.profesores = []
        self.pila_notas = deque()  # Pila (LIFO) para guardar acciones de notas: (cedula, nota)
        self.archivo_alumnos = "alumnos.txt"
        self.archivo_profesores = "profesores.txt"
        self.archivo_certificados = "certificados_pendientes.txt"
        self.cargar_datos()

    def cargar_datos(self):
        """Carga los datos iniciales desde los archivos físicos si existen."""
        if os.path.exists(self.archivo_alumnos):
            try:
                with open(self.archivo_alumnos, "r", encoding="utf-8") as f:
                    for linea in f:
                        linea = linea.strip()
                        if not linea:
                            continue
                        partes = linea.split(",")
                        if len(partes) >= 6:
                            cedula, nombre, correo, tipo_programa, notas_str, estatus = partes[0], partes[1], partes[2], partes[3], partes[4], partes[5]
                            notas = [float(n) for n in notas_str.split(",")] if notas_str else []
                            self.alumnos.append(Alumno(cedula, nombre, correo, tipo_programa, notas, estatus))
            except Exception as e:
                print(f"Error al cargar alumnos: {e}")

        if os.path.exists(self.archivo_profesores):
            try:
                with open(self.archivo_profesores, "r", encoding="utf-8") as f:
                    for linea in f:
                        linea = linea.strip()
                        if not linea:
                            continue
                        partes = linea.split(",")
                        if len(partes) >= 5:
                            cedula, nombre, correo, especialidad, materia = partes[0], partes[1], partes[2], partes[3], partes[4]
                            self.profesores.append(Profesor(cedula, nombre, correo, especialidad, materia))
            except Exception as e:
                print(f"Error al cargar profesores: {e}")

    def guardar_alumnos(self):
        """Sobrescribe el archivo alumnos.txt con el estado actual en memoria."""
        try:
            with open(self.archivo_alumnos, "w", encoding="utf-8") as f:
                for alumno in self.alumnos:
                    f.write(alumno.a_string_archivo())
        except Exception as e:
            print(f"Error al guardar alumnos: {e}")

    def guardar_profesores(self):
        """Sobrescribe el archivo profesores.txt con el estado actual en memoria."""
        try:
            with open(self.archivo_profesores, "w", encoding="utf-8") as f:
                for prof in self.profesores:
                    f.write(prof.a_string_archivo())
        except Exception as e:
            print(f"Error al guardar profesores: {e}")

    def registrar_alumno(self):
        print("\n--- REGISTRAR ALUMNO ---")
        cedula = input("Cédula: ").strip()
        if any(a.cedula == cedula for a in self.alumnos):
            print("Ya existe un alumno registrado con esa cédula.")
            return
        nombre = input("Nombre completo: ").strip()
        correo = input("Correo electrónico: ").strip()
        print("Tipos de Programa disponibles: Curso, Diplomado, Bootcamp")
        tipo_programa = input("Tipo de Programa: ").strip().capitalize()
        if tipo_programa not in ["Curso", "Diplomado", "Bootcamp"]:
            print(" Tipo no reconocido. Se guardará como 'Curso' por defecto.")
            tipo_programa = "Curso"
        
        nuevo_alumno = Alumno(cedula, nombre, correo, tipo_programa)
        self.alumnos.append(nuevo_alumno)
        self.guardar_alumnos()
        print(" Alumno registrado y guardado exitosamente en alumnos.txt.")

    def registrar_profesor(self):
        print("\n--- REGISTRAR PROFESOR ---")
        cedula = input("Cédula: ").strip()
        if any(p.cedula == cedula for p in self.profesores):
            print(" Ya existe un profesor registrado con esa cédula.")
            return
        nombre = input("Nombre completo: ").strip()
        correo = input("Correo electrónico: ").strip()
        especialidad = input("Especialidad: ").strip()
        materia = input("Materia: ").strip()
        
        nuevo_profesor = Profesor(cedula, nombre, correo, especialidad, materia)
        self.profesores.append(nuevo_profesor)
        self.guardar_profesores()
        print(" Profesor registrado y guardado exitosamente en profesores.txt.")

    def registrar_nota(self):
        print("\n--- REGISTRAR NOTA A UN ALUMNO ---")
        cedula = input("Ingrese la Cédula del alumno: ").strip()
        alumno = next((a for a in self.alumnos if a.cedula == cedula), None)
        if not alumno:
            print(" Alumno no encontrado en el sistema.")
            return
        
        if len(alumno.notas) >= 3:
            print(" El alumno ya tiene el máximo de 3 notas permitidas.")
            return

        try:
            nota = float(input(f"Ingrese la calificación para {alumno.nombre} (0 a 20): "))
            if not (0 <= nota <= 20):
                print(" La nota debe estar entre 0 y 20.")
                return
        except ValueError:
            print(" Error: Por favor ingrese un valor numérico válido.")
            return

        # Añadir nota al alumno
        alumno.notas.append(nota)
        # Registrar acción en la Pila (LIFO)
        self.pila_notas.append((cedula, nota))
        # Guardar cambios actualizados
        self.guardar_alumnos()
        print(f" Nota de {nota} registrada con éxito para {alumno.nombre}.")

    def deshacer_ultimo_registro_nota(self):
        print("\n--- DESHACER ÚLTIMO REGISTRO DE NOTA ---")
        if not self.pila_notas:
            print(" No hay acciones de notas recientes para deshacer (Pila vacía).")
            return

        cedula, nota_removida = self.pila_notas.pop()
        alumno = next((a for a in self.alumnos if a.cedula == cedula), None)
        if alumno and nota_removida in alumno.notas:
            alumno.notas.remove(nota_removida)
            self.guardar_alumnos()
            print(f" Acción deshecha con éxito: Se removió la nota {nota_removida} del alumno {alumno.nombre}.")
        else:
            print(" No se pudo localizar el registro exacto en el alumno correspondiente.")

    def generar_cola_certificados(self):
        print("\n--- GENERAR COLA DE CERTIFICADOS ---")
        cola_certificados = deque()  # Cola FIFO
        
        for alumno in self.alumnos:
            if alumno.evaluar_aprobacion():
                cola_certificados.append(alumno)
        
        self.guardar_alumnos()

        if not cola_certificados:
            print(" No hay alumnos que cumplan con los criterios de aprobación actualmente.")
            return

        print(f"Procesando Cola de Certificados (Total candidatos: {len(cola_certificados)})...")
        try:
            with open(self.archivo_certificados, "w", encoding="utf-8") as f:
                f.write("=========================================\n")
                f.write("REPORTE DE CERTIFICADOS PENDIENTES\n")
                f.write("=========================================\n")
                f.write(f"Total de graduandos en cola: {len(cola_certificados)}\n")
                
                contador = 1
                while cola_certificados:
                    graduando = cola_certificados.popleft()  # FIFO
                    regla_extra = " (Cumple regla de ninguna nota < 14)" if graduando.tipo_programa == "Bootcamp" else ""
                    
                    f.write(f"{contador}. [{graduando.cedula}] {graduando.nombre}\n")
                    f.write(f"   - Programa: {graduando.tipo_programa}\n")
                    f.write(f"   - Promedio Final: {graduando.calcular_promedio():.1f}\n")
                    f.write(f"   - Estatus: APROBADO{regla_extra}\n")
                    
                    print(f" -> Procesado y agregado a cola: {graduando.nombre} ({graduando.tipo_programa})")
                    contador += 1
                
                f.write("=========================================\n")
                f.write("- Fin del reporte - Generado por SGA-DO *\n")
            print(f"Cola procesada con éxito. Archivo generado: '{self.archivo_certificados}'.")
        except Exception as e:
            print(f"Error al exportar certificados: {e}")

    def mostrar_reporte_general(self):
        print("\n" + "="*50)
        print("REPORTE GENERAL SISTEMA DIPLOMADOSONLINE")
        print("="*50)
        
        print("\n--- PROFESORES ACTIVOS ---")
        if not self.profesores:
            print("No hay profesores registrados.")
        else:
            for p in self.profesores:
                print(f"• Cédula: {p.cedula} | Nombre: {p.nombre} | Correo: {p.correo} | Especialidad: {p.especialidad} | Materia: {p.materia}")
        
        print("\n--- ALUMNOS REGISTRADOS ---")
        if not self.alumnos:
            print("No hay alumnos registrados.")
        else:
            for a in self.alumnos:
                a.evaluar_aprobacion() # Actualiza estatus basado en notas
                promedio = a.calcular_promedio()
                notas_str = ", ".join(map(str, a.notas)) if a.notas else "Sin notas"
                print(f"• Cédula: {a.cedula} | Nombre: {a.nombre} | Programa: {a.tipo_programa} | Notas: [{notas_str}] | Promedio: {promedio:.1f} | Estatus: {a.estatus}")
        print("="*50)

    def ejecutar(self):
        while True:
            print("\n" + "="*50)
            print("SGA-DO: SISTEMA DIPLOMADOSONLINE")
            print("="*50)
            print("1. Registrar Alumno")
            print("2. Registrar Profesor")
            print("3. Registrar Notas a un Alumno")
            print("4. Deshacer Último Registro de Nota")
            print("5. Generar Cola de Certificados")
            print("6. Mostrar Reporte General")
            print("7. Salir")
            print("="*50)
            
            opcion = input("Seleccione una opción (1-7): ").strip()
            
            if opcion == "1":
                self.registrar_alumno()
            elif opcion == "2":
                self.registrar_profesor()
            elif opcion == "3":
                self.registrar_nota()
            elif opcion == "4":
                self.deshacer_ultimo_registro_nota()
            elif opcion == "5":
                self.generar_cola_certificados()
            elif opcion == "6":
                self.mostrar_reporte_general()
            elif opcion == "7":
                print("\nGuardando cambios pendientes y cerrando la aplicación de forma segura...")
                self.guardar_alumnos()
                print("¡Hasta luego!")
                break
            else:
                print(" Opción inválida. Por favor, seleccione un número entre 1 y 7.")

if __name__ == "__main__":
    sistema = SistemaGestion()
    sistema.ejecutar()



