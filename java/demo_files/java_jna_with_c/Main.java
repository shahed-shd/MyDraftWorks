
public class Main {
    public static void main(String[] args) {
        int a = 2, b = 3;
    
        int sum = LibSharedUtils.INSTANCE.add(a, b);
        int product = LibSharedUtils.INSTANCE.multiply(a, b);

        System.out.println("sum: " + sum);
        System.out.println("product: " + product);
    }
 }
