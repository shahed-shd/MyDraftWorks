import java.io.Externalizable;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectInput;
import java.io.ObjectInputStream;
import java.io.ObjectOutput;
import java.io.ObjectOutputStream;
import java.io.PrintStream;

public class ExternalizableDemo {
    static PrintStream printStream = System.out;

    public static class Person implements Externalizable {
        static String scientificName = "Homo sapiens";
        String name;
        int age;

        public Person() {
            printStream.println("Person no-arg constructor called");
        }

        public Person(String name, int age) {
            printStream.println("Person parameterized constructor called");
            this.name = name;
            this.age = age;
        }

        @Override
        public void writeExternal(ObjectOutput out) throws IOException {
            out.writeObject(name);
            out.writeInt(age);
            out.writeObject(scientificName);
        }

        @Override
        public void readExternal(ObjectInput in) throws IOException, ClassNotFoundException {
            name = (String) in.readObject();
            age = in.readInt();
            scientificName = (String) in.readObject();
        }
    }

    public static void main(final String[] args) {
        printStream.printf("Demo java.io.Externalizable%n%n");

        Person bob = new Person("Mr. Bob", 23);
        printPersonInfo(bob);

        String filename = "person.txt";

        try (FileOutputStream file = new FileOutputStream(filename);
                ObjectOutputStream out = new ObjectOutputStream(file)) {
            out.writeObject(bob);
            out.flush();
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
        printStream.printf("name: %s, age: %d, scientificName: %s%n", p.name, p.age, p.scientificName);
    }
}