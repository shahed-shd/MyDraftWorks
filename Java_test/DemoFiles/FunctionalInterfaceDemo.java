
public class FunctionalInterfaceDemo {
    public static void main(final String args[]) {
        System.out.println("Demo FunctionalInterface");

        A a = (int x) -> {
            System.out.println("In lambda: " + x);
            return x + 1;
        };

        int y = a.fn(123);
        assert y == 124;
        System.out.println("y: " + y);

        B b = new B();
        int z = b.fn(5);
        assert z == 50;
        System.out.println("z: " + z);

    }

}

@FunctionalInterface
interface A {
    public abstract int fn(int k);
}

class B implements A {
    public int fn(int value) {
        System.out.println("In B::fn(): " + value);
        return value * 10;
    }
}