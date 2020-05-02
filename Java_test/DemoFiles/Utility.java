import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Future;
import java.util.concurrent.TimeUnit;

public class Utility {

    public static void main(final String args[]) {
        System.out.println("Utility class having some necessary methods");
    }

    public static void trySleep(int seconds) {
        try {
            TimeUnit.SECONDS.sleep(seconds);
        } catch (InterruptedException e) {
            System.out.println("Exception occurs in trySleep: " + e);
            Thread.currentThread().interrupt(); // set interrupt flag
            throw new RuntimeException(e);
        }
    }

    public static void awaitForCompletion(List<Future<?>> futures) {
        for (Future<?> future : futures) {
            try {
                future.get();
            } catch (Exception e) {
                System.out.println("Exception occurs in future get");
                e.printStackTrace();
            }
        }
    }

    public static void shutdownExecutor(ExecutorService executor, int awaitSeconds) {
        try {
            System.out.println("Executor shutting down...");
            executor.shutdown();
            System.out.println("Executor shutdown done, awaiting " + awaitSeconds + " seconds to terminate...");
            executor.awaitTermination(awaitSeconds, TimeUnit.SECONDS);
        } catch (InterruptedException e) {
            System.out.println("Exection occurs while executor shutdown: " + e);
        } finally {
            if (!executor.isTerminated()) {
                System.out.println("Executor not terminated, terminating...");
                List<Runnable> nonFinishedTasks = executor.shutdownNow();
                int nonFinishedTaskCount = nonFinishedTasks.size();

                if (nonFinishedTaskCount > 0) {
                    System.out.println(nonFinishedTaskCount + " tasks couldn't be finished");
                    for (int i = 0; i < nonFinishedTaskCount; ++i) {
                        System.out.println("Non finished task (" + (i + 1) + "): " + nonFinishedTasks.get(i));
                    }
                }
            }

            System.out.println("Executor finally terminated");
        }
    }
}
