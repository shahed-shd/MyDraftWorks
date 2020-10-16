import java.io.PrintStream;
import java.util.Objects;

public class PairDemo {
    public static final PrintStream printStream = System.out;

    public static void main(final String[] args) {
        Pair<Integer, Integer> p1 = Pair.of(11, 22);
        Pair<Integer, Integer> p2 = Pair.of(11, 22);
        Pair<Integer, Integer> p3 = Pair.of(11, 99);

        assert p1.compareTo(p2) == 0;
        assert p1.compareTo(p3) < 0;

        printStream.println(p1.hashCode());

        assert p1.equals(p2);
        assert !p1.equals(p3);

        printStream.println(p1.toString());
    }
}

class Pair<A extends Comparable<? super A>, B extends Comparable<? super B>> implements Comparable<Pair<A, B>> {
    public final A first;
    public final B second;

    private Pair(A first, B second) {
        this.first = first;
        this.second = second;
    }

    public static <A extends Comparable<? super A>, B extends Comparable<? super B>> Pair<A, B> of(A first, B second) {
        return new Pair<A, B>(first, second);
    }

    @Override
    public int compareTo(Pair<A, B> o) {
        int cmp = o == null ? 1 : (this.first).compareTo(o.first);
        return cmp == 0 ? (this.second).compareTo(o.second) : cmp;
    }

    @Override
    public int hashCode() {
        return (first == null ? 0 : first.hashCode()) ^ (second == null ? 0 : second.hashCode());
    }

    @Override
    public boolean equals(Object o) {
        if (!(o instanceof Pair)) {
            return false;
        }
        if (this == o) {
            return true;
        }

        Pair<?, ?> p = (Pair<?, ?>) o;
        return Objects.equals(p.first, first) && Objects.equals(p.second, second);
    }

    @Override
    public String toString() {
        return "(" + first + ", " + second + ')';
    }
}