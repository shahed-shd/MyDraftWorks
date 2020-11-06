import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.PrintStream;
import java.util.Map;
import java.util.concurrent.TimeUnit;

public class RuntimeAndProcessDemo {
    public static final PrintStream printStream = System.out;

    public static void main(final String[] args) throws IOException, InterruptedException {
        printStream.println("Runtime and Process Demo");

        // Runtime object associated with the current Java application.
        final Runtime r = Runtime.getRuntime();

        // Shutdown hooks
        Thread thread1 = new Thread(() -> printStream.println("Running shutdown hook 1"));
        Thread thread2 = new Thread(() -> printStream.println("Running shutdown hook 2"));
        Thread thread3 = new Thread(() -> printStream.println("Running shutdown hook 3"));
        Thread thread4 = new Thread(() -> printStream.println("Running shutdown hook 4"));

        r.addShutdownHook(thread1);
        r.addShutdownHook(thread2);
        r.addShutdownHook(thread3);
        r.addShutdownHook(thread4);

        r.removeShutdownHook(thread2);

        // Processors
        printStream.println("No of Processors: " + r.availableProcessors());

        // Memory status
        printStream.println("::Memory status::");
        printMemoryStatus(r);
        for (int i = 0; i <= 10000; i++) {
            new Object();
        }
        r.gc();
        printStream.println("After gc:");
        printMemoryStatus(r);

        // Subprocess using Runtime.exec()
        printStream.println("\n::Process::");
        String[] cmdArray = new String[] { "bash", "-c",
                "pwd ; echo \"count start: $countStart end: $countEnd interval: $countInterval\"; for count in $(seq $countStart $countInterval $countEnd); do sleep $countInterval && echo \"count: $count\" && date ; done ;" };
        String[] envp = new String[] { "countStart=1", "countEnd=10", "countInterval=3" };
        File dir = new File("../");
        Process proc = r.exec(cmdArray, envp, dir); // `envp` and `dir` are optional by `exec` overloaded methods.
        printFromInputStream(proc.getInputStream());
        terminateProcIfAlive(proc);

        // Subprocess using ProcessBuilder
        ProcessBuilder pb = new ProcessBuilder(cmdArray);
        Map<String, String> envMap = pb.environment();
        envMap.put("countStart", "1");
        envMap.put("countEnd", "5");
        envMap.put("countInterval", "1");
        pb.directory(dir);
        pb.inheritIO(); // Same I/O as current java process.
        proc = pb.start();
        proc.waitFor(10, TimeUnit.SECONDS);
        terminateProcIfAlive(proc);

        // Subprocess by modifying the previous ProcessBuilder instance
        envMap = pb.environment();
        envMap.put("countEnd", "5");
        envMap.put("countInterval", "1");
        String filename = "sample_log.txt";
        pb.redirectOutput(ProcessBuilder.Redirect.appendTo(new File(filename)));
        printStream.println("Starting process... appending output to file named " + filename);
        proc = pb.start();
        proc.waitFor(10, TimeUnit.SECONDS);
        terminateProcIfAlive(proc);

        // Terminate the currently running JVM by initiating its shutdown sequence. To terminate forcibly, invoke halt() method.
        // Registered shutdown hooks (if any) will run in some unspecified order concurrently.
        r.exit(0);
    }

    static void printMemoryStatus(final Runtime r) {
        printStream.println("Total memory: " + r.totalMemory());
        printStream.println("Free memory: " + r.freeMemory());
        printStream.println("Memory occupied: " + (r.totalMemory() - r.freeMemory()));
    }

    static void terminateProcIfAlive(Process proc) {
        printStream.print("Process (pid: " + proc.pid() + ") is ");
        if (proc.isAlive()) {
            printStream.println("still runnng. Terminating...");
            proc.destroy();
        } else {
            printStream.println("terminated normally");
        }
        printStream.println("Process's exit code: " + proc.exitValue());
    }

    static void printFromInputStream(InputStream inputStream) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(inputStream));
        String line;
        while ((line = br.readLine()) != null) {
            printStream.println(line);
        }
    }
}
