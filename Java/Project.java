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


class SistemaSGA {
    private static final String ARCH_ALUMNOS = "alumnnos.txt";
    private static final String ARCH_PROFESORES = "profesores.txt";
    private static final String ARCH_CERTIFICADOS = "certificados_pendientes.txt";

    private List<Alumno> alumnos;
    private List<Profesor> profesores;
    private Stack<RegistroNota> pilaDEshacerNotas;
    private Scanner scanner;

    public SistemaSGA() {
        alumnos = new ArrayList<>();
        profesores = new ArrayList<>();
        pilaDeshacerNotas = new Stack<>();
        scanner = new Scanner(System.in);
        cargarDatos();
    }

    private ProgramaAcademico instanciarPrograma(String tipo) {
        tipo = tipo.trim().toLowerCase();
        if (tipo.equals("diplomado")) return new Diplomado();
        if (tipo.equals("bootcamp")) return new Bootcamp();
        return new Curso();
    }
    
    public void cargarDatos() {
        File FAlumnos = new File(ARCH_ALUMNOS);
        if (FAlumnos.exists()) {
            try (BufferedReader br = new BufferedReader(new FileReader(FAlumnos))) {
                String linea;
                while ((linea = br.readLine()) != null) {
                    linea = linea.trim();
                    if (linea.isEmpty()) continue;
                    String[] partes = linea.split(",");
                    if (partes.length >= 4) {
                        String cedula = partes[0].trim();
                        String nombre = partes[1].trim();
                        String correo = partes[2].trim();
                        String tipoProg = partes[3].trim();

                        ProgramaAcademico prog = instanciarPrograma(tipoProg);
                        Alumno alumno = new Alumno(cedula, nombre, correo, prog);

                        for (int i = 4; i < partes.length; i++) {
                            try {
                                double val = Double.parseDouble(partes[i].trim());
                                if (val > 0) {
                                    alumno.agregarNota(val);
                                }
                            } catch (NumberFormatException ignored) {}
                        }
                        alumnos.add(alumno);
                    }
                }
            } catch (IOException e) {
                System.out.println("Error al leer alumnos.txt: " + e.getMessage());
            }
        }

        File fProf = new File(ARCH_PROFESORES);
        if (fProf.exists()) {
            try (BufferedReader br = new BufferedReader(new FileReader(fProf))) {
                String linea;
                while ((linea = br.readLine()) != null) {
                    linea = linea.trim();
                    if (linea.isEmpty()) continue;
                    String[] partes = linea.split(",");
                    if (partes.length >= 5) {
                        String cedula = partes[0].trim();
                        String nombre = partes[1].trim();
                        String correo = partes[2].trim();
                        String especialidad = partes[3].trim();
                        StringBuilder materiaBuilder = new StringBuilder();
                        for (int i = 4; i < partes.length; i++) {
                            materiaBuilder.append(partes[i]);
                            if (i < partes.length - 1) materiaBuilder.append(",");
                        }
                        Profesor prof = new Profesor(cedula, nombre, correo, especialidad, materiaBuilder.toString().trim());
                        profesores.add(prof);
                    }
                }
            } catch (IOException e) {
                System.out.println("Error al leer profesores.txt: " + e.getMessage());
            }
        }
    }

    public void guardarTodo() {
        try (PrintWriter pw = new PrintWriter(new FileWriter(ARCH_ALUMNOS))) {
            for (Alumno a : alumnos) {
                List<Double> notasCompletas = new ArrayList<>(a.getNotas());
                while (notasCompletas.size() < 3) {
                    notasCompletas.add(0.0);
                }
                pw.print(a.getCedula() + "," + a.getNombre() + "," + a.getCorreo() + "," + a.getPrograma().getNombre());
                for (double n : notasCompletas) {
                    pw.print("," + (n == (int)n ? String.format("%d", (int)n) : String.valueOf(n)));
                }
                pw.println();
            }
        } catch (IOException e) {
            System.out.println("Error al guardar alumnos.txt: " + e.getMessage());
        }
