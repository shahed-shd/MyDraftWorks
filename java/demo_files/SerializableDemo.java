import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.PrintStream;
import java.io.Serializable;

public class SerializableDemo {
    static PrintStream printStream = System.out;

    static class Person implements Serializable {
        private static final long serialVersionUID = 382682708032729996L;

        static String scientificName = "Homo sapiens";
        String name;
        int age;
        transient String secretToken;

        Person(String name, int age, String secretToken) {
            this.name = name;
            this.age = age;
            this.secretToken = secretToken;
        }

        // Classes that require special handling during the serialization and deserialization process must implement special methods with some given exact signatures.
        // writeObject(), readObject() are some of special methods and can be omitted to have default behavior.

        private void writeObject(java.io.ObjectOutputStream out) throws IOException {
            printStream.println("Person.writeObject() invoked");
            out.defaultWriteObject();
        }

        private void readObject(java.io.ObjectInputStream in) throws IOException, ClassNotFoundException {
            printStream.println("Person.readObject() invoked");
            in.defaultReadObject();
        }
    }

    public static void main(final String[] args) {
        printStream.printf("Demo java.io.Serializable%n%n");

        Person bob = new Person("Mr. Bob", 23, "JustSimpleSecretToken");
        printPersonInfo(bob);

        String filename = "person.ser";

        try (FileOutputStream file = new FileOutputStream(filename);
                ObjectOutputStream out = new ObjectOutputStream(file)) {
            out.writeObject(bob);
            printStream.println("Serialization done");
        } catch (IOException ex) {
            printStream.println("IOException caught: " + ex.getMessage());
        }

        printStream.printf("File created: %s%n%n", filename);

        try (FileInputStream file = new FileInputStream(filename); ObjectInputStream in = new ObjectInputStream(file)) {
            Person bob2 = (Person) in.readObject();
            printStream.println("Deserialization done");
            printPersonInfo(bob2);
        } catch (IOException ex) {
            printStream.println("IOException caught: " + ex.getMessage());
        } catch (ClassNotFoundException ex) {
            printStream.println("ClassNotFoundException caught: " + ex.getMessage());
        }
    }

    public static void printPersonInfo(Person p) {
        printStream.printf("name: %s, age: %d, secretToken: %s, scientificName: %s%n", p.name, p.age, p.secretToken,
                p.scientificName);
    }
}
