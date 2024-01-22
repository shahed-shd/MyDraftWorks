
/* java version: 21
 * 
 */
import java.io.PrintStream;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import java.util.function.BiConsumer;
import java.util.function.Supplier;

public class CompletableFutureDemo {
    private static PrintStream printStream = System.out;

    public static void main(String[] args) {
        printStream.println("CompletableFuture demo");

        Supplier<String> currentThreadToString = () -> {
            Thread currentThread = Thread.currentThread();
            return String.format("Thread(name: %s, id: %s)", currentThread.getName(), currentThread.getId());
        };

        printStream.println(String.format("In main method, thread: %s", currentThreadToString.get()));
        

        BiConsumer<Integer, String> sleepTask = (Integer second, String reference) -> {
            try {
                TimeUnit.SECONDS.sleep(second);
                printStream.println(String.format("Ref: %s, thread: %s", reference, currentThreadToString.get()));
            } catch (InterruptedException e) {
                throw new IllegalStateException(e);
            }
        };

        // ========== supplyAsync and chain ==========
        {
            CompletableFuture<String> completableFuture = CompletableFuture.supplyAsync(() -> {
                sleepTask.accept(1, "supplyAsync");
                return "Initial";
            });

            ExecutorService executorService = Executors.newFixedThreadPool(3);

            CompletableFuture<Void> completableFutureChained = completableFuture.thenApply(value -> {
                printStream.println("In thenApply");
                return value + " -> thenApply";
            }).thenApplyAsync(value -> {
                printStream.println("In thenApplyAsync");
                return value + " -> thenApplyAsync";
            }).thenApplyAsync(value -> {
                printStream.println("In thenApplyAsync with executor");
                return value + " -> thenApplyAsync-with-executor";
            }, executorService).exceptionally(ex -> {
                printStream.println("In exceptionally");
                ex.printStackTrace();
                return " -> exceptional";
            }).thenCompose(value -> {
                printStream.println("In thenCompose");
                return CompletableFuture.completedFuture(value + " -> thenCompose");
            }).thenCombine(CompletableFuture.completedStage("CompletedStageValue"), (a, b) -> {
                printStream.println("In thenCombine, params: " + a + ", " + b);
                return a + " -> thenCombine";
            }).handle((value, throwable) -> {
                printStream.println("In handle, params: " + value + ", " + throwable);
                if (throwable == null) {
                    printStream.println("Completed normally");
                    return value + " -> handle";
                } else {
                    printStream.println("Completed exceptionally");
                    return "Re-initited-from-handle";
                }
            }).exceptionally(ex -> {
                printStream.println("In exceptionally after handle");
                ex.printStackTrace();
                return " -> exceptional-after-handle";
            }).thenAccept(value -> {
                printStream.println("In thenAccept");
                System.out.println(value);
            }).thenRun(() -> {
                printStream.println("In thenRun");
                executorService.shutdown();
            });

            printStream.println("is done: " + completableFutureChained.isDone());
            printStream.println("In main method, before join");
            completableFutureChained.join();
        }

        // ========== runAsync ==========
        {
            CompletableFuture<Void> completableFutureFromRunAsync = CompletableFuture.runAsync(() -> {
                sleepTask.accept(1, "runAsync");
            }).thenAccept(value -> {
                printStream.println("Now in thenAccept, value is null: " + (value == null));
            });

            completableFutureFromRunAsync.join();

        }

        // ========== allOf ==========
        {
            CompletableFuture<Void> completableFutureAllOf = CompletableFuture.allOf(
                    CompletableFuture.supplyAsync(() -> {
                        sleepTask.accept(2, "allOf-1");
                        return "allOf-1";
                    }),
                    CompletableFuture.supplyAsync(() -> {
                        sleepTask.accept(5, "allOf-2");
                        return "allOf-2";
                    }),
                    CompletableFuture.supplyAsync(() -> {
                        sleepTask.accept(2, "allOf-3");
                        return "allOf-3";
                    }));

            printStream.println("In main method, before joining `allOf`");

            completableFutureAllOf.join();
        }

        // ========== anyOf ==========
        {

            CompletableFuture<Object> completableFutureAnyOf = CompletableFuture.anyOf(
                    CompletableFuture.supplyAsync(() -> {
                        sleepTask.accept(2, "anyOf-1");
                        return "anyOf-1";
                    }),
                    CompletableFuture.supplyAsync(() -> {
                        sleepTask.accept(5, "anyOf-2");
                        return "anyOf-2";
                    }),
                    CompletableFuture.supplyAsync(() -> {
                        sleepTask.accept(2, "anyOf-3");
                        return "anyOf-3";
                    }));

            printStream.println("In main method, before joining `anyOf`");
            Object res = completableFutureAnyOf.join();
            printStream.println("In main method, after joining `anyOf`, result: " + res);
        }
    }
}

/*
 * Notes on some key points:
 * 
 * The computation performed by a stage may be expressed as:
 * - Function
 * - Consumer
 * - Runnable
 * 
 * using methods with names including the followings
 * depending on whether it requires arguments and/or produces results:
 * - apply
 * - accept
 * - run
 * 
 * `compose` for computation pipelines.
 * `combine` to combine resultsor effects of two stages.
 * 
 * Any argument to a stage's computation is the outcome of a triggering stage's
 * computation.
 * One stage's execution may be triggered by completion of a
 * - single stage (methods with prefix `then`)
 * - or both of two stages (methods with prefix `both`)
 * - or either of two stages (methods with prefix `either`)
 * 
 */