import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.PrintStream;
import java.nio.file.Path;
import protogen.models.PersonOuterClass.Person;
import protogen.models.AddressOuterClass.Address;
import protogen.enums.StatusOuterClass.Status;

public class Main {

    private static PrintStream printStream = System.out;

    public static void serializeToFile(File file) throws Exception {
        printStream.println("Java: serializing");

        Address address = Address.newBuilder()
                .setStreet("456 Elm St")
                .setCity("JavaTown")
                .setZip("99999")
                .build();

        Person person = Person.newBuilder()
                .setName("Bob")
                .setId(2)
                .setEmail("bob@example.com")
                .addPhoneNumbers("789")
                .addPhoneNumbers("101")
                .setAddress(address)
                .setStatus(Status.INACTIVE)
                .build();

        try (FileOutputStream fos = new FileOutputStream(file)) {
            person.writeTo(fos);
        }
    }

    public static void deserializeFromFile(File file) throws Exception {
        printStream.println("Java: deserializing");

        try (FileInputStream fis = new FileInputStream(file)) {
            Person person = Person.parseFrom(fis);
            printStream.println("----- Deserialized instance output -----");
            printStream.println(person);
            printStream.println("---------- Done ----------");
        }
    }

    public static void main(String[] args) throws Exception {
        String command = args[0];
        String filePathArg = args[1];
        
        File outputFile = new File(filePathArg);

        if (command.equals("serialize")) {
            serializeToFile(outputFile);
        } else if (command.equals("deserialize")) {
            deserializeFromFile(outputFile);
        } else if (command.equals("demo")) {
            serializeToFile(outputFile);
            deserializeFromFile(outputFile);
        } else {
            throw new IllegalArgumentException("Invalid commad " + command);
        }
    }
}
