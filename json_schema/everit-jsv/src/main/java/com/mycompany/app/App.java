package com.mycompany.app;

import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.PrintStream;

import org.everit.json.schema.Schema;
import org.everit.json.schema.ValidationException;
import org.everit.json.schema.loader.SchemaLoader;
import org.json.JSONObject;
import org.json.JSONTokener;

public class App {
    static PrintStream printStream = System.out;

    public static void main(final String[] args) {
        // ToDo: Need to assign absolute path of the files.
        final String schemaPath = "absolute_path_of_the_demo_schema.json";
        final String instancePath = "absolute_path_of_the_demo_instance.json";

        validate(schemaPath, instancePath);
    }

    public static void validate(final String schemaPath, final String instancePath) {

        printStream.println("SCHEMA: " + schemaPath);
        printStream.println("INSTANCE: " + instancePath);
        printStream.println("Validating . . .");

        try (InputStream schemaStream = new FileInputStream(schemaPath);
                InputStream instanceStream = new FileInputStream(instancePath)) {

            JSONObject rawSchema = new JSONObject(new JSONTokener(schemaStream));
            Schema schema = SchemaLoader.load(rawSchema);

            JSONObject instance = new JSONObject(new JSONTokener(instanceStream));
            schema.validate(instance);
            printStream.println("Validation successful");
        } catch (IOException | ValidationException e) {
            e.printStackTrace(printStream);
        } finally {
            printStream.println("Done");
        }
    }
}
