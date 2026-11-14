import java.io.*;
import java.util.*;

class Persona {
    private String cedula;
    private String nombre;
    private String correo;

    public Persona(String cedula, String nombre, String correo) {
        this.cedula = cedula;
        this.nombre = nombre;
        this.correo = correo;

    }

    public String getCedula() { return cedula; }
    public String getNombre() { return nombre; }
    public String getCorreo() {return correo; }

    @Override
    public String toString() {
        return "ID: " + cedula + " | Nombre: " + nombre + " | Correo: " + correo;
    }    
    
}

abstract class ProgramaAcademico {
    private String nombre;

    public ProgramaAcademico(String nombre) {
        this.nombre = nombre;
    }
    public String getNombre() { return nombre; }

    // metodo evaluado por las sublases3
    public abstract boolean evaluarAprobacion(List<Double> notas);     
}

class Curso extends ProgramaAcademico {
        public Curso() { super("Curso"); }

        @Override
        public boolean evaluarAprobacion(List<Double> notas) {
            if (notas.size() < 3) return false;
            double suma = 0;
            for (double n : notas) suma += n;
            return (suma / notas.size()) >= 10.0;   
        }
}

class Diplomado extends ProgramaAcademico {
   public Diplomado() { super("Diplomado"); }
   
   @Override
   public boolean evaluarAprobacion(List<Double> notas) {
    if (notas.size() < 3) return false;
    double suma = 0;
    for (double n : notas) suma += n;
    return (suma / notas.size()) >=14.0;
   }
}

class Bootcamp extends ProgramaAcademico {
    public Bootcamp() {super("Bootcamp"); }
    @Override
    public boolean evaluarAprobacion(List<Double> notas) {
        if (notas.size() < 3) return false;
        for (double n : notas) {
            if (n < 14.0) return false;
        } 
        return true;
    }
}

class Alumno extends Persona {
    private ProgramaAcademico programa;
    private List<Double> notas;
    
    public Alumno(String cedula, String nombre, String correo, ProgramaAcademico programa) {
        super(cedula, nombre, correo);
        this.programa = programa;
        this.notas = new ArrayList<>();
    }
    public ProgramaAcademico getPrograma() { return programa; }
    public List<Double> getNotas() {return notas; }

    public boolean agregarNota(double nota) {
        if (notas.size() < 3) {
            notas.add(nota);
            return true;

        }
        return false;

    }

    public Double eliminarUltimaNota() {
        if(!notas.isEmpty()) {
            return notas.remove(notas.size() - 1);
        }
        return null;
    }

    public boolean estaAprobado() {
        return programa.evaluarAprobacion(notas);    
    }

    @Override
    public String toString() {
        List<Double> notasCompletas = new ArrayList<>(notas);
        while (notasCompletas.size() < 3) {
            notasCompletas.add(0.0);
        }
        StringBuilder sb = new StringBuilder();
        for (int i=0; i < notasCompletas.size(); i++) {
            double n = notasCompletas.get(i);
            sb.append(n == (int)n ? String.format("%d", (int)n) : String.format("%.1f" , n));
            if (i < notasCompletas.size() -1) sb.append(", ");    
        }
       String estado = estaAprobado() ? "APROBADO" : "EN PROCESO / REPROBADO";
        return "[Alumno] " + super.toString() + " | Programa: " + programa.getNombre() +
               " | Notas: [" + sb.toString() + "] | Estatus: " + estado;
    }
}

class Profesor extends Persona {
    private String especialidad;
    private String materia;

    public Profesor(String cedula, String nombre, String correo, String especialidad, String materia) {
    super(cedula,nombre, correo);
    this.especialidad = especialidad;
    this.materia = materia;    
    }

    public String getEspecialidad() {return especialidad;}
    public String getMateria() {return materia; }

    @Override
    public String toString() {
        return "[Profesor] " + super.toString() + " | Especialidad: " + especialidad + " | Materia: " + materia;

    }

}

//Comtrol pila last in first out
class RegistroNota {
    private String cedulaAlumno;
    private double nota;

    public RegistroNota(String cedulaAlumno, double nota) {
        this.cedulaAlumno = cedulaAlumno;
        this.nota = nota;
    }

    public String getCedulaAlumno() { return cedulaAlumno; }
    public double getNota() {return nota; }
}

// ==============================================================================
// MOTOR DEL SISTEMA SGA-DO Y GESTIÓN DE FLUJOS
// ==============================================================================



    