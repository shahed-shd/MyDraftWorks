import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.Semaphore;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReadWriteLock;
import java.util.concurrent.locks.ReentrantLock;
import java.util.concurrent.locks.ReentrantReadWriteLock;
import java.util.concurrent.locks.StampedLock;

public class SyncAndLocks {

    public static void main(final String args[]) {
        System.out.println("Sync and Lock demo");

        Counter counter = new Counter();
        ExecutorService executor = Executors.newFixedThreadPool(5);
        List<Future<?>> futures = new ArrayList<>();
        Future<?> future;

        System.out.println("---------- Execute the method without synchronization ----------");

        // The output is not sequential
        for (int i = 0; i < 10; ++i) {
            future = executor.submit(counter::increment);
            futures.add(future);
        }

        Utility.awaitForCompletion(futures);
        counter.print();

        System.out.println("---------- Execute the method with synchronization ----------");

        counter.reset();
        futures.clear();

        // The output is sequential
        for (int i = 0; i < 10; ++i) {
            future = executor.submit(counter::syncAndIncrement);
            futures.add(future);
        }

        Utility.awaitForCompletion(futures);
        counter.print();

        System.out.println("---------- Execute the method with ReentrantLock ----------");

        counter.reset();
        futures.clear();
        Lock lock = new ReentrantLock();

        for (int i = 0; i < 10; ++i) {
            Runnable task = () -> {
                lock.lock();

                try {
                    System.out.printf("Locked(inc) ");
                    counter.increment();
                } finally {
                    lock.unlock();
                }
            };

            future = executor.submit(task);
            futures.add(future);
        }

        Utility.awaitForCompletion(futures);
        counter.print();

        System.out.println("---------- Execute the methods with ReadWriteLock ----------");

        counter.reset();
        futures.clear();
        ReadWriteLock rwlock = new ReentrantReadWriteLock();
        Random random = new Random();

        for (int i = 0; i < 10; ++i) {
            if (random.nextBoolean()) {
                Callable<Integer> readTask = () -> {
                    rwlock.readLock().lock();
                    int c;

                    try {
                        System.out.printf("Locked(r) ");
                        c = counter.getCount();
                    } finally {
                        rwlock.readLock().unlock();
                    }

                    return c;
                };

                future = executor.submit(readTask);
            } else {
                Runnable writeTask = () -> {
                    rwlock.writeLock().lock();
                    try {
                        System.out.printf("Locked(w) ");
                        counter.increment();
                    } finally {
                        rwlock.writeLock().unlock();
                    }
                };

                future = executor.submit(writeTask);
            }

            futures.add(future);
        }

        Utility.awaitForCompletion(futures);
        counter.print();

        System.out.println("---------- Execute the methods with StampedLock ----------");
        // StampedLock doesn't implement reentrant characteristics.

        counter.reset();
        futures.clear();
        StampedLock stampedLock = new StampedLock();

        for (int i = 0; i < 10; ++i) {
            if (random.nextBoolean()) {
                Callable<Integer> readTask = () -> {
                    long stamp = stampedLock.readLock();
                    int c;

                    try {
                        System.out.printf("Locked(r) ");
                        c = counter.getCount();
                    } finally {
                        stampedLock.unlock(stamp);
                    }

                    return c;
                };

                future = executor.submit(readTask);
            } else {
                Runnable writeTask = () -> {
                    long stamp = stampedLock.writeLock();

                    try {
                        System.out.printf("Locked(w) ");
                        counter.increment();
                    } finally {
                        stampedLock.unlock(stamp);
                    }
                };

                future = executor.submit(writeTask);
            }

            futures.add(future);
        }

        Utility.awaitForCompletion(futures);
        counter.print();

        System.out.println("---------- Execute the methods with StampedLock (Optimistic) ----------");

        counter.reset();
        futures.clear();

        for (int i = 0; i < 10; ++i) {
            if (random.nextBoolean()) {
                Callable<Integer> readTask = () -> {
                    long stamp = stampedLock.tryOptimisticRead();
                    int c;

                    try {
                        retryHoldingLock: for (;; stamp = stampedLock.readLock()) {
                            if (stamp == 0L) {
                                continue retryHoldingLock;
                            } else {
                                System.out.printf("Locked(r) ");
                                c = counter.getCount();
                                break;
                            }
                        }
                    } finally {
                        if (StampedLock.isReadLockStamp(stamp)) {
                            stampedLock.unlockRead(stamp);
                        }
                    }

                    return c;
                };

                future = executor.submit(readTask);
            } else {
                Runnable writeTask = () -> {
                    long stamp = stampedLock.writeLock();

                    try {
                        System.out.printf("Locked(w) ");
                        counter.increment();
                    } finally {
                        stampedLock.unlock(stamp);
                    }
                };

                future = executor.submit(writeTask);
            }

            futures.add(future);
        }

        Utility.awaitForCompletion(futures);
        counter.print();

        System.out.println("---------- Execute the methods with StampedLock (tryConvertToWriteLock) ----------");

        counter.reset();
        futures.clear();

        for (int i = 0; i < 10; ++i) {
            Callable<Integer> task = () -> {
                long stamp = stampedLock.readLock();
                int c;

                try {
                    while (counter.getCount() == 0) {
                        long wStamp = stampedLock.tryConvertToWriteLock(stamp);

                        if (wStamp != 0L) {
                            stamp = wStamp;
                            counter.increment();
                        } else {
                            System.out.println("Couldn't convert to write lock");
                            stampedLock.unlockRead(stamp);
                            stamp = stampedLock.writeLock();
                        }
                    }

                    c = counter.getCount();
                } finally {
                    stampedLock.unlock(stamp);
                }

                return c;
            };

            future = executor.submit(task);
            futures.add(future);
        }

        Utility.awaitForCompletion(futures);
        counter.print();

        System.out.println("---------- Execute the methods with Semaphore ----------");

        counter.reset();
        futures.clear();
        Semaphore semaphore = new Semaphore(3, true);

        for (int i = 0; i < 10; ++i) {
            Runnable task = () -> {
                try {
                    semaphore.acquire();

                    try {
                        System.out.printf("Acquired, now available permits: %d, ", semaphore.availablePermits());
                        counter.increment();
                    } finally {
                        semaphore.release();
                    }
                } catch (InterruptedException e) {
                    System.out.println("Exception occures by semaphore while acquiring: " + e.getMessage());
                }
            };

            future = executor.submit(task);
            futures.add(future);
        }

        Utility.awaitForCompletion(futures);
        counter.print();

        executor.shutdown();
    }
}

class Counter {
    private int count = 0;

    private String threadToString(Thread thread) {
        return thread.getId() + ", " + thread.getName();
    }

    public void increment() {
        System.out.printf("count: %d incrementing... [%s]\n", count, threadToString(Thread.currentThread()));
        ++count;
    }

    public synchronized void syncAndIncrement() {
        System.out.printf("synchronously ");
        increment();
    }

    // The synchronized keyword is also available as a block statement.
    // public void incrementSync() {
    //     synchronized (this) {
    //         System.out.printf("synchronously ");
    //         increment();
    //     }
    // }

    public int getCount() {
        System.out.printf("getting... count: %d [%s]\n", count, threadToString(Thread.currentThread()));
        return count;
    }

    public void reset() {
        System.out.println("Counter reset");
        count = 0;
    }

    public void print() {
        System.out.printf("count: %d [%s]\n", count, threadToString(Thread.currentThread()));
    }
}
