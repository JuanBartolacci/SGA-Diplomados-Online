#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <sstream>
#include <stack>
#include <queue>
#include <algorithm>
#include <iomanip>
#include <locale>

using namespace std;

// ==============================================================================
// CLASE BASE: Persona
// ==============================================================================
class Persona {
protected:
    string cedula;
    string nombre;
    string correo;

public:
    Persona(string cedula, string nombre, string correo)
        : cedula(cedula), nombre(nombre), correo(correo) {}

    virtual ~Persona() {}

    string getCedula() const { return cedula; }
    string getNombre() const { return nombre; }
    string getCorreo() const { return correo; }

    virtual string toString() const {
        return "ID: " + cedula + " | Nombre: " + nombre + " | Correo: " + correo;
    }
};

// ==============================================================================
// PATRÓN STRATEGY: ProgramaAcademico (Clase Abstracta con Polimorfismo Real)
// ==============================================================================
class ProgramaAcademico {
protected:
    string nombre;

public:
    ProgramaAcademico(string nombre) : nombre(nombre) {}
    virtual ~ProgramaAcademico() {}

    string getNombre() const { return nombre; }
    virtual bool evaluarAprobacion(const vector<double>& notas) const = 0;
};

class Curso : public ProgramaAcademico {
public:
    Curso() : ProgramaAcademico("Curso") {}

    bool evaluarAprobacion(const vector<double>& notas) const override {
        vector<double> notasCompletas = notas;
        while (notasCompletas.size() < 3) {
            notasCompletas.push_back(0.0);
        }
        double suma = 0;
        for (double n : notasCompletas) suma += n;
        return (suma / 3.0) >= 10.0;
    }
};

class Diplomado : public ProgramaAcademico {
public:
    Diplomado() : ProgramaAcademico("Diplomado") {}

    bool evaluarAprobacion(const vector<double>& notas) const override {
        vector<double> notasCompletas = notas;
        while (notasCompletas.size() < 3) {
            notasCompletas.push_back(0.0);
        }
        double suma = 0;
        for (double n : notasCompletas) suma += n;
        return (suma / 3.0) >= 14.0;
    }
};

class Bootcamp : public ProgramaAcademico {
public:
    Bootcamp() : ProgramaAcademico("Bootcamp") {}

    bool evaluarAprobacion(const vector<double>& notas) const override {
        vector<double> notasCompletas = notas;
        while (notasCompletas.size() < 3) {
            notasCompletas.push_back(0.0);
        }
        for (double n : notasCompletas) {
            if (n < 14.0) return false;
        }
        return true;
    }
};

// ==============================================================================
// CLASE: Alumno
// ==============================================================================
class Alumno : public Persona {
private:
    ProgramaAcademico* programa;
    vector<double> notas;

public:
    Alumno(string cedula, string nombre, string correo, ProgramaAcademico* programa)
        : Persona(cedula, nombre, correo), programa(programa) {}

    ~Alumno() {
        delete programa; // Liberar memoria
    }

    ProgramaAcademico* getPrograma() const { return programa; }
    const vector<double>& getNotas() const { return notas; }

    bool agregarNota(double nota) {
        if (notas.size() < 3) {
            notas.push_back(nota);
            return true;
        }
        return false;
    }

    bool eliminarUltimaNota(double& notaRemovida) {
        if (!notas.empty()) {
            notaRemovida = notas.back();
            notas.pop_back();
            return true;
        }
        return false;
    }

    bool estaAprobado() const {
        return programa->evaluarAprobacion(notas);
    }

    string toString() const {
        vector<double> notasCompletas = notas;
        while (notasCompletas.size() < 3) {
            notasCompletas.push_back(0.0);
        }
        stringstream ss;
        for (size_t i = 0; i < notasCompletas.size(); i++) {
            double n = notasCompletas[i];
            if (n == (int)n) {
                ss << (int)n;
            } else {
                ss << fixed << setprecision(1) << n;
            }
            if (i < notasCompletas.size() - 1) ss << ",";
        }
        string estado = estaAprobado() ? "APROBADO" : "EN PROCESO / REPROBADO";
        return "[Alumno] " + Persona::toString() + " | Programa: " + programa->getNombre() +
               " | Notas: [" + ss.str() + "] | Estatus: " + estado;
    }
};

// ==============================================================================
// CLASE: Profesor
// ==============================================================================
class Profesor : public Persona {
private:
    string especialidad;
    string materia;

public:
    Profesor(string cedula, string nombre, string correo, string especialidad, string materia)
        : Persona(cedula, nombre, correo), especialidad(especialidad), materia(materia) {}

    string getEspecialidad() const { return especialidad; }
    string getMateria() const { return materia; }

    string toString() const override {
        return "[Profesor] " + Persona::toString() + " | Especialidad: " + especialidad + " | Materia: " + materia;
    }
};

// ==============================================================================
// ESTRUCTURA PARA LA PILA DE DESHACER (LIFO)
// ==============================================================================
struct RegistroNota {
    string cedulaAlumno;
    double nota;
};

// ==============================================================================
// MOTOR DEL SISTEMA: SistemaSGA
// ==============================================================================
class SistemaSGA {
private:
    const string ARCH_ALUMNOS = "alumnos.txt";
    const string ARCH_PROFESORES = "profesores.txt";
    const string ARCH_CERTIFICADOS = "certificados_pendientes.txt";

    vector<Alumno*> alumnos;
    vector<Profesor*> profesores;
    stack<RegistroNota> pilaDeshacerNotas;

    ProgramaAcademico* instanciarPrograma(string tipo) {
        for (char& c : tipo) c = tolower(c);
        if (tipo.find("diplomado") != string::npos) return new Diplomado();
        if (tipo.find("bootcamp") != string::npos) return new Bootcamp();
        return new Curso();
    }

public:
    SistemaSGA() {
        cargarDatos();
    }

    ~SistemaSGA() {
        // Limpieza de memoria dinámica para evitar fugas
        for (auto a : alumnos) delete a;
        for (auto p : profesores) delete p;
    }

    void cargarDatos() {
        ifstream fAlumnos(ARCH_ALUMNOS);
        if (fAlumnos.is_open()) {
            string linea;
            while (getline(fAlumnos, linea)) {
                if (linea.empty()) continue;
                stringstream ss(linea);
                string cedula, nombre, correo, tipoProg;

                if (getline(ss, cedula, ',') && getline(ss, nombre, ',') &&
                    getline(ss, correo, ',') && getline(ss, tipoProg, ',')) {

                    ProgramaAcademico* prog = instanciarPrograma(tipoProg);
                    Alumno* alumno = new Alumno(cedula, nombre, correo, prog);

                    string notaStr;
                    while (getline(ss, notaStr, ',')) {
                        try {
                            double val = stod(notaStr);
                            if (val > 0) {
                                alumno->agregarNota(val);
                            }
                        } catch (...) {}
                    }
                    alumnos.push_back(alumno);
                }
            }
            fAlumnos.close();
        }

        ifstream fProf(ARCH_PROFESORES);
        if (fProf.is_open()) {
            string linea;
            while (getline(fProf, linea)) {
                if (linea.empty()) continue;
                stringstream ss(linea);
                string cedula, nombre, correo, especialidad, materia;

                if (getline(ss, cedula, ',') && getline(ss, nombre, ',') &&
                    getline(ss, correo, ',') && getline(ss, especialidad, ',') &&
                    getline(ss, materia)) {

                    Profesor* prof = new Profesor(cedula, nombre, correo, especialidad, materia);
                    profesores.push_back(prof);
                }
            }
            fProf.close();
        }
    }

    void guardarTodo() {
        // Persistencia para Alumnos (escribe exactamente las 3 notas rellenando con ceros si faltan)
        ofstream fAlumnos(ARCH_ALUMNOS);
        if (fAlumnos.is_open()) {
            for (const auto& a : alumnos) {
                vector<double> notasCompletas = a->getNotas();
                while (notasCompletas.size() < 3) {
                    notasCompletas.push_back(0.0);
                }
                fAlumnos << a->getCedula() << "," << a->getNombre() << ","
                         << a->getCorreo() << "," << a->getPrograma()->getNombre();
                for (double n : notasCompletas) {
                    fAlumnos << ",";
                    if (n == (int)n) fAlumnos << (int)n;
                    else fAlumnos << n;
                }
                fAlumnos << "\n";
            }
            fAlumnos.close();
        }

        // Persistencia para Profesores
        ofstream fProf(ARCH_PROFESORES);
        if (fProf.is_open()) {
            for (const auto& p : profesores) {
                fProf << p->getCedula() << "," << p->getNombre() << ","
                      << p->getCorreo() << "," << p->getEspecialidad() << ","
                      << p->getMateria() << "\n";
            }
            fProf.close();
        }
    }

    void registrarAlumno() {
        cout << "\n--- Registrar Alumno ---\n";
        string cedula, nombre, correo;
        cout << "Cédula / ID: ";
        getline(cin, cedula);

        for (const auto& a : alumnos) {
            if (a->getCedula() == cedula) {
                cout << "Error: Ya existe un alumno con esa cédula.\n";
                return;
            }
        }

        cout << "Nombre Completo: ";
        getline(cin, nombre);
        cout << "Correo Electrónico: ";
        getline(cin, correo);

        ProgramaAcademico* prog = nullptr;
        while (true) {
            cout << "Tipo de Programa (1. Curso, 2. Diplomado, 3. Bootcamp): ";
            string opc;
            getline(cin, opc);
            if (opc == "1") {
                prog = new Curso();
                break;
            } else if (opc == "2") {
                prog = new Diplomado();
                break;
            } else if (opc == "3") {
                prog = new Bootcamp();
                break;
            } else {
                cout << "Error: Opción no válida. Debe ingresar 1, 2 o 3.\n";
            }
        }

        Alumno* nuevo = new Alumno(cedula, nombre, correo, prog);
        alumnos.push_back(nuevo);
        guardarTodo();
        cout << "Alumno registrado exitosamente.\n";
    }

    void registrarProfesor() {
        cout << "\n--- Registrar Profesor ---\n";
        string cedula, nombre, correo, especialidad, materia;
        cout << "Cédula / ID: ";
        getline(cin, cedula);

        for (const auto& p : profesores) {
            if (p->getCedula() == cedula) {
                cout << "Error: Ya existe un profesor con esa cédula.\n";
                return;
            }
        }

        cout << "Nombre Completo: ";
        getline(cin, nombre);
        cout << "Correo Electrónico: ";
        getline(cin, correo);
        cout << "Especialidad: ";
        getline(cin, especialidad);
        cout << "Materia Asignada: ";
        getline(cin, materia);

        Profesor* nuevo = new Profesor(cedula, nombre, correo, especialidad, materia);
        profesores.push_back(nuevo);
        guardarTodo();
        cout << "Profesor registrado exitosamente.\n";
    }

    void registrarNota() {
        cout << "\n--- Registrar Notas ---\n";
        cout << "Ingrese la Cédula del Alumno: ";
        string cedula;
        getline(cin, cedula);

        Alumno* alumno = nullptr;
        for (auto a : alumnos) {
            if (a->getCedula() == cedula) {
                alumno = a;
                break;
            }
        }

        if (!alumno) {
            cout << "Error: Alumno no encontrado.\n";
            return;
        }

        if (alumno->getNotas().size() >= 3) {
            cout << "Error: El alumno ya tiene sus 3 notas registradas.\n";
            return;
        }

        cout << "Ingrese calificación (0-20) para " << alumno->getNombre() << ": ";
        string notaStr;
        getline(cin, notaStr);
        try {
            double nota = stod(notaStr);
            if (nota < 0 || nota > 20) {
                cout << "Error: La nota debe estar entre 0 y 20.\n";
                return;
            }

            if (alumno->agregarNota(nota)) {
                pilaDeshacerNotas.push({alumno->getCedula(), nota});
                guardarTodo();
                cout << "Nota " << nota << " guardada correctamente.\n";
            }
        } catch (...) {
            cout << "Error: Ingrese un valor numérico válido.\n";
        }
    }

    void deshacerUltimaNota() {
        cout << "\n--- Deshacer Último Registro ---\n";
        if (pilaDeshacerNotas.empty()) {
            cout << "No hay acciones de notas recientes para deshacer en esta sesión.\n";
            return;
        }

        RegistroNota ultimo = pilaDeshacerNotas.top();
        pilaDeshacerNotas.pop();

        Alumno* alumno = nullptr;
        for (auto a : alumnos) {
            if (a->getCedula() == ultimo.cedulaAlumno) {
                alumno = a;
                break;
            }
        }

        double notaRemovida = 0;
        if (alumno && alumno->eliminarUltimaNota(notaRemovida)) {
            guardarTodo();
            cout << "Se ha removido la última nota (" << notaRemovida << ") del alumno " << alumno->getNombre() << ".\n";
        } else {
            cout << "No se pudo completar la operación.\n";
        }
    }

    void generarColaCertificados() {
        cout << "\n--- Generar Cola de Certificados ---\n";
        queue<Alumno*> colaGraduandos;

        for (auto a : alumnos) {
            if (a->estaAprobado()) {
                colaGraduandos.push(a);
            }
        }

        if (colaGraduandos.empty()) {
            cout << "No hay alumnos aprobados actualmente.\n";
            return;
        }

        ofstream pw(ARCH_CERTIFICADOS);
        if (pw.is_open()) {
            pw << "=========================================\n";
            pw << "REPORTE DE CERTIFICADOS PENDIENTES\n";
            pw << "=========================================\n";
            pw << "Total de graduandos en cola: " << colaGraduandos.size() << "\n";

            int contador = 1;
            while (!colaGraduandos.empty()) {
                Alumno* g = colaGraduandos.front();
                colaGraduandos.pop(); // Procesamiento FIFO

                vector<double> notasCompletas = g->getNotas();
                while (notasCompletas.size() < 3) {
                    notasCompletas.push_back(0.0);
                }
                double suma = 0;
                for (double n : notasCompletas) suma += n;
                double promedio = suma / 3.0;

                pw << contador << ". [" << g->getCedula() << "] " << g->getNombre() << "\n";
                pw << "- Programa: " << g->getPrograma()->getNombre() << "\n";
                pw << fixed << setprecision(1) << "- Promedio Final: " << promedio << "\n";

                string estatus = "APROBADO";
                if (dynamic_cast<Bootcamp*>(g->getPrograma())) {
                    estatus = "APROBADO (Cumple regla de ninguna nota < 14)";
                }
                pw << "- Estatus: " << estatus << "\n";
                contador++;
            }
            pw << "=========================================\n";
            pw << "- Fin del reporte - Generado por SGA-DO *\n";
            pw.close();
            cout << "Reporte generado exitosamente en '" << ARCH_CERTIFICADOS << "'.\n";
        } else {
            cout << "Error al escribir el archivo de certificados.\n";
        }
    }

    void mostrarReporteGeneral() {
        cout << "\n" << string(50, '=') << "\n";
        cout << "Reporte General - Diplomados Online\n";
        cout << string(50, '=') << "\n";

        cout << "\n[PROFESORES]\n";
        if (profesores.empty()) {
            cout << "Sin registros.\n";
        }
        for (const auto& p : profesores) {
            cout << "- " << p->getCedula() << "," << p->getNombre() << ","
                 << p->getCorreo() << "," << p->getEspecialidad() << "," << p->getMateria() << "\n";
        }

        cout << "\n[ALUMNOS]\n";
        if (alumnos.empty()) {
            cout << "Sin registros.\n";
        }
        for (const auto& a : alumnos) {
            vector<double> notasCompletas = a->getNotas();
            while (notasCompletas.size() < 3) {
                notasCompletas.push_back(0.0);
            }
            stringstream sb;
            for (size_t i = 0; i < notasCompletas.size(); i++) {
                double n = notasCompletas[i];
                if (n == (int)n) sb << (int)n;
                else sb << fixed << setprecision(1) << n;
                if (i < notasCompletas.size() - 1) sb << ",";
            }
            cout << "- " << a->getCedula() << "," << a->getNombre() << ","
                 << a->getCorreo() << "," << a->getPrograma()->getNombre() << "," << sb.str() << "\n";
        }
        cout << string(50, '=') << "\n";
    }

    void iniciar() {
        while (true) {
            cout << "\n" << string(50, '=') << "\n";
            cout << "SGA-DO: SISTEMA DIPLOMADOSONLINE\n";
            cout << string(50, '=') << "\n";
            cout << "1. Registrar Alumno\n";
            cout << "2. Registrar Profesor\n";
            cout << "3. Registrar Notas a un Alumno\n";
            cout << "4. Deshacer Último Registro de Nota\n";
            cout << "5. Generar Cola de Certificados\n";
            cout << "6. Mostrar Reporte General\n";
            cout << "7. Salir\n";
            cout << string(50, '=') << "\n";
            cout << "Seleccione una opción (1-7): ";

            string opcion;
            getline(cin, opcion);

            if (opcion == "1") {
                registrarAlumno();
            } else if (opcion == "2") {
                registrarProfesor();
            } else if (opcion == "3") {
                registrarNota();
            } else if (opcion == "4") {
                deshacerUltimaNota();
            } else if (opcion == "5") {
                generarColaCertificados();
            } else if (opcion == "6") {
                mostrarReporteGeneral();
            } else if (opcion == "7") {
                guardarTodo();
                cout << "\nGuardando y saliendo de forma segura. ¡Hasta pronto!\n";
                return;
            } else {
                cout << "Opción inválida. Intente de nuevo.\n";
            }
        }
    }
};

// ==============================================================================
// FUNCIÓN PRINCIPAL MAIN
// ==============================================================================
int main() {
    SistemaSGA sistema;
    sistema.iniciar();
    return 0;
}