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
    public String getCorreo() { return correo; }

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

    public abstract boolean evaluarAprobacion(List<Double> notas);    
}

class Curso extends ProgramaAcademico {
    public Curso() { super("Curso"); }

    @Override
    public boolean evaluarAprobacion(List<Double> notas) {
        List<Double> notasCompletas = new ArrayList<>(notas);
        while (notasCompletas.size() < 3) {
            notasCompletas.add(0.0);
        }
        double suma = 0;
        for (double n : notasCompletas) suma += n;
        return (suma / notasCompletas.size()) >= 10.0;   
    }
}

class Diplomado extends ProgramaAcademico {
   public Diplomado() { super("Diplomado"); }
   
   @Override
   public boolean evaluarAprobacion(List<Double> notas) {
       List<Double> notasCompletas = new ArrayList<>(notas);
       while (notasCompletas.size() < 3) {
           notasCompletas.add(0.0);
       }
       double suma = 0;
       for (double n : notasCompletas) suma += n;
       return (suma / notasCompletas.size()) >= 14.0;
   }
}

class Bootcamp extends ProgramaAcademico {
    public Bootcamp() { super("Bootcamp"); }
    
    @Override
    public boolean evaluarAprobacion(List<Double> notas) {
        List<Double> notasCompletas = new ArrayList<>(notas);
        while (notasCompletas.size() < 3) {
            notasCompletas.add(0.0);
        }
        for (double n : notasCompletas) {
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
    public List<Double> getNotas() { return notas; }

    public boolean agregarNota(double nota) {
        if (notas.size() < 3) {
            notas.add(nota);
            return true;
        }
        return false;
    }

    public Double eliminarUltimaNota() {
        if (!notas.isEmpty()) {
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
        for (int i = 0; i < notasCompletas.size(); i++) {
            double n = notasCompletas.get(i);
            sb.append(n == (int)n ? String.format("%d", (int)n) : String.format("%.1f" , n));
            if (i < notasCompletas.size() - 1) sb.append(", ");    
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
        super(cedula, nombre, correo);
        this.especialidad = especialidad;
        this.materia = materia;    
    }

    public String getEspecialidad() { return especialidad; }
    public String getMateria() { return materia; }

    @Override
    public String toString() {
        return "[Profesor] " + super.toString() + " | Especialidad: " + especialidad + " | Materia: " + materia;
    }
}

class RegistroNota {
    private String cedulaAlumno;
    private double nota;

    public RegistroNota(String cedulaAlumno, double nota) {
        this.cedulaAlumno = cedulaAlumno;
        this.nota = nota;
    }

    public String getCedulaAlumno() { return cedulaAlumno; }
    public double getNota() { return nota; }
}

class SistemaSGA {
    private static final String ARCH_ALUMNOS = "alumnos.txt";
    private static final String ARCH_PROFESORES = "profesores.txt";
    private static final String ARCH_CERTIFICADOS = "certificados_pendientes.txt";

    private List<Alumno> alumnos;
    private List<Profesor> profesores;
    private Stack<RegistroNota> pilaDeshacerNotas;
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

        try (PrintWriter pw = new PrintWriter(new FileWriter(ARCH_PROFESORES))) {
            for (Profesor p : profesores) {
                pw.println(p.getCedula() + "," + p.getNombre() + "," + p.getCorreo() + "," + p.getEspecialidad() + "," + p.getMateria());
            }
        } catch (IOException e) {
            System.out.println("Error al guardar profesores.txt: " + e.getMessage());
        }
    }
    
    public void registrarAlumno() {
        System.out.println("\n--- Registrar Alumno ---");
        System.out.print("Cédula / ID: ");
        String cedula = scanner.nextLine().trim();

        for (Alumno a : alumnos) {
            if (a.getCedula().equalsIgnoreCase(cedula)) {
                System.out.println("Error: Ya existe un alumno con esa cédula.");
                return;
            }
        }

        System.out.print("Nombre Completo: ");
        String nombre = scanner.nextLine().trim();
        System.out.print("Correo Electrónico: ");
        String correo = scanner.nextLine().trim();

        ProgramaAcademico prog;
        while (true) {
            System.out.println("Tipo de Programa (1. Curso, 2. Diplomado, 3. Bootcamp): ");
            String opc = scanner.nextLine().trim();
            if (opc.equals("1")) {
                prog = new Curso();
                break;
            } else if (opc.equals("2")) {
                prog = new Diplomado();
                break;
            } else if (opc.equals("3")) {
                prog = new Bootcamp();
                break;
            } else {
                System.out.println("Error: Opción no válida. Debe ingresar 1, 2 o 3.");
            }
        }

        Alumno nuevo = new Alumno(cedula, nombre, correo, prog);
        alumnos.add(nuevo);
        guardarTodo();
        System.out.println("Alumno registrado exitosamente.");
    }

    public void registrarProfesor() {
        System.out.println("\n--- Registrar Profesor ---");
        System.out.print("Cédula / ID: ");
        String cedula = scanner.nextLine().trim();

        for (Profesor p : profesores) {
            if (p.getCedula().equalsIgnoreCase(cedula)) {
                System.out.println("Error: Ya existe un profesor con esa cédula.");
                return;
            }
        }

        System.out.print("Nombre Completo: ");
        String nombre = scanner.nextLine().trim();
        System.out.print("Correo Electrónico: ");
        String correo = scanner.nextLine().trim();
        System.out.print("Especialidad (ej. Backend, Frontend): ");
        String especialidad = scanner.nextLine().trim();
        System.out.print("Materia Asignada: ");
        String materia = scanner.nextLine().trim();

        Profesor nuevo = new Profesor(cedula, nombre, correo, especialidad, materia);
        profesores.add(nuevo);
        guardarTodo();
        System.out.println(" Profesor registrado exitosamente.");
    }

    public void registrarNota() {
        System.out.println("\n--- Registrar Notas ---");
        System.out.print("Ingrese la Cédula del Alumno: ");
        String cedula = scanner.nextLine().trim();

        Alumno alumno = null;
        for (Alumno a : alumnos) {
            if (a.getCedula().equalsIgnoreCase(cedula)) {
                alumno = a;
                break;
            }
        }

        if (alumno == null) {
            System.out.println("Error: Alumno no encontrado.");
            return;
        }

        if (alumno.getNotas().size() >= 3) {
            System.out.println("Error: El alumno ya tiene sus 3 notas registradas.");
            return;
        }
        
        try {
            System.out.print("Ingrese calificación (0-20) para " + alumno.getNombre() + ": ");
            double nota = Double.parseDouble(scanner.nextLine().trim());
            if (nota < 0 || nota > 20) {
                System.out.println("Error: La nota debe estar entre 0 y 20.");
                return;
            }

            if (alumno.agregarNota(nota)) {
                pilaDeshacerNotas.push(new RegistroNota(alumno.getCedula(), nota));
                guardarTodo();
                System.out.println("Nota " + nota + " guardada correctamente.");                
            }            
        } catch (NumberFormatException e) {
            System.out.println("Error: Ingrese un valor numérico válido.");
        }
    }

    public void deshacerUltimaNota() {
        System.out.println("\n--- Deshacer Último Registro ---");
        if (pilaDeshacerNotas.isEmpty()) {
            System.out.println("No hay acciones de notas recientes para deshacer en esta sesión.");
            return;
        }

        RegistroNota ultimo = pilaDeshacerNotas.pop();
        Alumno alumno = null;
        for (Alumno a : alumnos) {
            if (a.getCedula().equalsIgnoreCase(ultimo.getCedulaAlumno())) {
                alumno = a;
                break;
            }
        }

        if (alumno != null && !alumno.getNotas().isEmpty()) {
            Double notaRemovida = alumno.eliminarUltimaNota();
            guardarTodo();
            System.out.println("Se ha removido la última nota (" + notaRemovida + ") del alumno " + alumno.getNombre() + ".");
        } else {
            System.out.println("No se pudo completar la operación.");
        }
    }

    public void generarColaCertificados() {
        System.out.println("\n--- Generar Cola de Certificados ---");
        Queue<Alumno> colaGraduandos = new LinkedList<>();
        
        for (Alumno a : alumnos) {
            if (a.estaAprobado()) {
                colaGraduandos.add(a);
            }
        }
        
        if (colaGraduandos.isEmpty()) {
            System.out.println("No hay alumnos aprobados actualmente.");
            return;            
        }

        try (PrintWriter pw = new PrintWriter(new FileWriter(ARCH_CERTIFICADOS))) {
            pw.println("=========================================");
            pw.println("Reporte de Certificados Pendientes");
            pw.println("=========================================");
            pw.println("Total de Graduandos en Cola: " + colaGraduandos.size());

            int contador = 1;
            while (!colaGraduandos.isEmpty()) {
                Alumno g = colaGraduandos.poll(); // FIFO
                List<Double> notasCompletas = new ArrayList<>(g.getNotas());
                while (notasCompletas.size() < 3) {
                    notasCompletas.add(0.0);
                }
                double suma = 0;
                for (double n : notasCompletas) suma += n;
                double promedio = suma / notasCompletas.size();

                pw.println(contador + ". [" + g.getCedula() + "] " + g.getNombre());
                pw.println("- Programa: " + g.getPrograma().getNombre());
                pw.println(String.format(Locale.US, "- Promedio Final: %.1f", promedio));

                String estatus = "Aprobado";
                if (g.getPrograma() instanceof Bootcamp) {
                    estatus = "Aprobado (Cumple regla de ninguna nota < 14)";
                }
                pw.println("- Estatus: " + estatus);
                contador++;
            }
            pw.println("=========================================");
            pw.println("- Fin del reporte - Generado por SGA-DO *");
            System.out.println("✓ Reporte generado exitosamente en '" + ARCH_CERTIFICADOS + "'.");
        } catch (IOException e) {
            System.out.println("Error al escribir el archivo de certificados: " + e.getMessage());
        }
    }

    public void mostrarReporteGeneral() {
        System.out.println("\n" + "=".repeat(50));
        System.out.println("Reporte General - Diplomados Online");
        System.out.println("=".repeat(50));
        System.out.println("\n[PROFESORES]");
        if (profesores.isEmpty()) {
            System.out.println("Sin registros.");
        }
        for (Profesor p : profesores) {
            System.out.println("- " + p.getCedula() + "," + p.getNombre() + "," + p.getCorreo() + "," + p.getEspecialidad() + "," + p.getMateria());
        }
        System.out.println("\n[ALUMNOS]");
        if (alumnos.isEmpty()) {
            System.out.println("Sin registros.");
        }
        for (Alumno a : alumnos) {
            List<Double> notasCompletas = new ArrayList<>(a.getNotas());
            while (notasCompletas.size() < 3) {
                notasCompletas.add(0.0);
            }
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < notasCompletas.size(); i++) {
                double n = notasCompletas.get(i);
                sb.append(n == (int)n ? (int)n : n);
                if (i < notasCompletas.size() - 1) sb.append(",");
            }
            System.out.println("- " + a.getCedula() + "," + a.getNombre() + "," + a.getCorreo() + "," + a.getPrograma().getNombre() + "," + sb.toString());
        }
        System.out.println("=".repeat(50));
    }

    public void iniciar() {
        while (true) {
            System.out.println("\n" + "=".repeat(50));
            System.out.println("SGA-DO: SISTEMA DIPLOMADOSONLINE");
            System.out.println("=".repeat(50));
            System.out.println("1. Registrar Alumno");
            System.out.println("2. Registrar Profesor");
            System.out.println("3. Registrar Notas a un Alumno");
            System.out.println("4. Deshacer Último Registro de Nota");
            System.out.println("5. Generar Cola de Certificados");
            System.out.println("6. Mostrar Reporte General");
            System.out.println("7. Salir");
            System.out.println("=".repeat(50));
            System.out.print("Seleccione una opción (1-7): ");

            String opcion = scanner.nextLine().trim();

            switch (opcion) {
                case "1":
                    registrarAlumno();
                    break;
                case "2":
                    registrarProfesor();
                    break;
                case "3":
                    registrarNota();
                    break;
                case "4":
                    deshacerUltimaNota();
                    break;
                case "5":
                    generarColaCertificados();
                    break;
                case "6":
                    mostrarReporteGeneral();
                    break;
                case "7":
                    guardarTodo();
                    System.out.println("\nGuardando y saliendo de forma segura. ¡Hasta pronto!");
                    return;
                default:
                    System.out.println("Opción inválida. Intente de nuevo.");
            }
        }
    }
}

public class MainSGA {
    public static void main(String[] args) {
        SistemaSGA sistema = new SistemaSGA();
        sistema.iniciar();
    }
}