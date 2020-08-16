import java.util.LinkedList;
import java.util.Queue;
import java.util.concurrent.TimeUnit;

public class WaitNotifyDemo {
    public static void main(final String[] args) {
        Queue<Integer> queue = new LinkedList<>();
        final int MAX_CAPACITY = 5;

        Producer producer = new Producer(queue, MAX_CAPACITY);
        Consumer consumer = new Consumer(queue);

        Thread tProducer = new Thread(producer, "Thread-Producer");
        Thread tConsumer = new Thread(consumer, "Thread-Consumer");
        tConsumer.start();
        tProducer.start();
    }
}

class Producer implements Runnable {
    private final Queue<Integer> queue;
    private int maxCap;

    public Producer(Queue<Integer> sharedQueue, int maxCap) {
        this.queue = sharedQueue;
        this.maxCap = maxCap;
    }

    @Override
    public void run() {
        int loopCount = 0;

        while (loopCount < 100) {
            try {
                produce(++loopCount);
            } catch (InterruptedException e) {
                e.printStackTrace();
                Thread.currentThread().interrupt(); // Restore interrupted state.

            }
        }
    }

    private void produce(int value) throws InterruptedException {
        synchronized (queue) {
            while (queue.size() == maxCap) {
                System.out.println(
                        "Queue full, size: " + queue.size() + ", " + Thread.currentThread().getName() + " is waiting");
                queue.wait();
            }

            TimeUnit.SECONDS.sleep(1);
            queue.add(value);
            System.out.println("Produced: " + value);
            queue.notifyAll();
        }
    }
}

class Consumer implements Runnable {
    private final Queue<Integer> queue;

    Consumer(Queue<Integer> sharedQueue) {
        this.queue = sharedQueue;
    }

    @Override
    public void run() {
        int loopCount = 0;

        while (loopCount++ < 100) {
            try {
                consume();
            } catch (InterruptedException e) {
                e.printStackTrace();
                Thread.currentThread().interrupt(); // Restore interrupted state.
            }
        }
    }

    private void consume() throws InterruptedException {
        synchronized (queue) {
            while (queue.isEmpty()) {
                System.out.println(
                        "Queue empty, size: " + queue.size() + ", " + Thread.currentThread().getName() + " is waiting");
                queue.wait();
            }

            TimeUnit.SECONDS.sleep(1);
            int value = queue.remove();
            System.out.println("Consumed: " + value);
            queue.notifyAll();
        }
    }
}