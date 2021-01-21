import java.io.*;
import java.util.*;

public class ProcessRunner {
    public static final PrintStream printStream = System.out;

    public static void main(final String[] args) throws InterruptedException, IOException {
        printStream.println("args: " + Arrays.toString(args));

        ProcessBuilder pb = new ProcessBuilder(args);
        pb.inheritIO();
        printStream.println("----------------------------------------");
        Process proc = pb.start();
        proc.waitFor();
        printStream.println("----------------------------------------");
        printStream.println("Process's exit code: " + proc.exitValue());
        
        // printStream.println("----------------------------------------");
        // Process proc = Runtime.getRuntime().exec(args);
        // proc.waitFor();
        // printFromInputStream(proc.getInputStream());
        // printStream.println("----------------------------------------");
        // printStream.println("Process's exit code: " + proc.exitValue());
    }

    static void printFromInputStream(InputStream inputStream) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(inputStream));
        String line;
        while ((line = br.readLine()) != null) {
            printStream.println(line);
        }
    }
}
