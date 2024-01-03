import java.nio.file.Path;

public class Main {
    static {
        System.load(Path.of("libsharedutils.so").toAbsolutePath().toString()); 
        // System.loadLibrary("sharedutils");  // Doesn't work, don't know why.
    }
 
    private native int add(int a, int b);
    private native int multiply(int a, int b);
 
    public static void main(String[] args) {
        int a = 2, b = 3;
        Main main = new Main();

        int sum = main.add(a, b);
        int product = main.multiply(a, b);

        System.out.println("sum: " + sum + "\nproduct: " + product);
    }
 }
 