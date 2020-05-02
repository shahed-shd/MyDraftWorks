import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.TimeUnit;

public class RunnableDemo {
    public static void main(final String args[]) {
        System.out.println("Hello Java");

        Runnable task = () -> {
            Thread currThread = Thread.currentThread();
            System.out.println("Thread name: " + currThread.getName() + " and ID: " + currThread.getId());
            Utility.trySleep(2);
        };

        System.out.println("---------- Execute the runnable using executor ----------");
        List<Future<?>> futures = new ArrayList<>();
        ExecutorService executor = Executors.newFixedThreadPool(3);

        futures.add(executor.submit(task));
        futures.add(executor.submit(task));
        futures.add(executor.submit(task));
        futures.add(executor.submit(task));
        futures.add(executor.submit(task));

        Utility.awaitForCompletion(futures);
        Utility.shutdownExecutor(executor, 4);

        System.out.println("---------- Execute the runnable in another thread ----------");
        Thread thread = new Thread(task);
        thread.start();

        System.out.println("---------- Execute the runnable directly (in main thread) ----------");
        task.run();

        System.out.println("Done");
    }
}
