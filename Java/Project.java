import java.io.*;
import java.util.*;

class persona {
    private String cedula;
    private String nombre;
    private String correo;

    public Persona(String, cedula, String nombre, String correo) {
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

