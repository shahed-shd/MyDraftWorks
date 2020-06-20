import java.lang.reflect.Constructor;
import java.lang.reflect.Field;
import java.lang.reflect.Method;

public class ClassDemo {
    public static void main(final String args[]) {
        System.out.println("Demo java.lang.Class");

        Person bob = new Person("Bob", 28);
        ServiceMan alice = new ServiceMan("Alice", 26, "Teacher");
        ServiceMan[] serviceManArray = { new ServiceMan("Colin", 29, "Doctor"), alice };

        Class<Person> classPerson = Person.class;
        Class<?> classBob = bob.getClass();
        Class classServiceMan = ServiceMan.class;
        Class classAlice = alice.getClass();

        assert classPerson == classBob;
        assert classPerson != classServiceMan;
        assert classServiceMan == classAlice;

        // public static Class<?> forName(String className) throws
        // ClassNotFoundException
        try {
            assert Class.forName("Person") == Person.class;
        } catch (Exception e) {
            System.out.println(e);
        }

        // Class<? super T> getSuperclass()
        assert ServiceMan.class.getSuperclass() == Person.class;

        // AnnotatedType getAnnotatedSuperclass()
        System.out.println("Object.class.getAnnotatedSuperclass(): " + Object.class.getAnnotatedSuperclass());
        System.out.println("Person.class.getAnnotatedSuperclass(): " + Person.class.getAnnotatedSuperclass());
        System.out.println("ServiceMan.class.getAnnotatedSuperclass(): " + ServiceMan.class.getAnnotatedSuperclass());

        // Type getGenericSuperclass()
        assert ServiceMan.class.getGenericSuperclass() == Person.class;

        // String getName()
        assert ServiceMan.class.getName().equals("ServiceMan");

        // String getSimpleName()
        assert ServiceMan.class.getSimpleName().equals("ServiceMan");

        // String getCanonicalName()
        assert ServiceMan.class.getCanonicalName().equals("ServiceMan");

        // String getTypeName()
        assert ServiceMan.class.getTypeName().equals("ServiceMan");

        // String toGenericString()
        assert ServiceMan.class.toGenericString().equals("class ServiceMan");

        // String toString()
        assert ServiceMan.class.toString().equals("class ServiceMan");

        // Class<?> getComponentType()
        assert serviceManArray.getClass().componentType() == classServiceMan;

        // Constructor<?>[] getConstructors() [returns public constructors only]
        System.out.println("ServiceMan.class.getConstructors():");
        for (Constructor<?> x : ServiceMan.class.getConstructors()) {
            System.out.println("\t" + x);
        }

        // Constructor<?>[] getDeclaredConstructors()
        System.out.println("ServiceMan.class.getDeclaredConstructors():");
        for (Constructor<?> x : ServiceMan.class.getDeclaredConstructors()) {
            System.out.println("\t" + x);
        }

        // Class<?>[] getDeclaredClasses()
        System.out.println("ServiceMan.class.getDeclaredClasses():");
        for (Class<?> x : ServiceMan.class.getDeclaredClasses()) {
            System.out.println("\t" + x);
        }

        // Field[] getFields()
        System.out.println("ServiceMan.class.getFields():");
        for (Field x : ServiceMan.class.getFields()) {
            System.out.println("\t" + x);
        }

        // Field[] getDeclaredFields()
        System.out.println("ServiceMan.class.getDeclaredFields():");
        for (Field x : ServiceMan.class.getDeclaredFields()) {
            System.out.println("\t" + x);
        }

        // Method[] getMethods()
        System.out.println("ServiceMan.class.getMethods():");
        for (Method x : ServiceMan.class.getMethods()) {
            System.out.println("\t" + x);
        }

        // Method[] getDeclaredMethods()
        System.out.println("ServiceMan.class.getDeclaredMethods():");
        for (Method x : ServiceMan.class.getDeclaredMethods()) {
            System.out.println("\t" + x);
        }

        // Class<?> getDeclaringClass()
        assert ServiceMan.NestedClassA.class.getDeclaringClass() == ServiceMan.class;

        // Class<?> getEnclosingClass()
        assert ServiceMan.NestedClassA.class.getEnclosingClass() == ServiceMan.class;

        // T[] getEnumConstants()
        System.out.println("ServiceMan.SampleEnum.class.getEnumConstants():");
        for (var x : ServiceMan.SampleEnum.class.getEnumConstants()) {
            System.out.println("\t" + x);
        }

        // boolean isAnnotation()
        assert ServiceMan.class.isAnnotation() == false;

        // boolean isAnonymousClass()
        assert ServiceMan.class.isAnonymousClass() == false;

        // boolean isArray()
        assert serviceManArray.getClass().isArray() == true;
        assert ServiceMan.class.isArray() == false;

        // boolean isEnum()
        assert ServiceMan.SampleEnum.class.isEnum() == true;
        assert ServiceMan.class.isEnum() == false;

        // boolean isInstance(Object obj)
        assert ServiceMan.class.isInstance(alice) == true;

        // boolean isInterface()
        assert ServiceMan.class.isInterface() == false;

        // boolean isLocalClass()
        assert ServiceMan.class.isLocalClass() == false;
        Object sampleLocal = alice.buildLocalClass();
        assert sampleLocal.getClass().isLocalClass() == true;

        // boolean isMemberClass()
        assert ServiceMan.class.isMemberClass() == false;
        assert ServiceMan.NestedClassA.class.isMemberClass() == true;

        // boolean isPrimitive()
        assert int.class.isPrimitive() == true;
        Integer integer = 123;
        assert integer.getClass().isPrimitive() == false;
        assert ServiceMan.class.isPrimitive() == false;

        // T newInstance() method is deprecated, it can be replaced with
        // getDeclaredConstructor().newInstance() method
        try {
            ServiceMan dan = new ServiceMan("Dan", 30, "Businessman");

            Constructor serviceManConstructor = ServiceMan.class.getDeclaredConstructor(String.class, int.class,
                    String.class);
            ServiceMan danNewInstance = (ServiceMan) serviceManConstructor.newInstance("Dan", 30, "Businessman");

            System.out.println("New instance of ServiceMan:\n\t" + danNewInstance.toInfoString());

            assert dan.name.equals(danNewInstance.name) && dan.age == danNewInstance.age
                    && dan.occupation.equals(danNewInstance.occupation);
        } catch (Exception e) {
            System.out.println(e);
        }

        System.out.println("OK");
    }
}

class Person {
    public String name;
    int age;

    public Person() {
        System.out.println("Person class's Empty constructor called");
    }

    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    public String toInfoString() {
        return "name: " + name + ", age: " + age;
    }
}

class ServiceMan extends Person {
    enum SampleEnum {
        SampleEnumValueA, SampleEnumValueB
    };

    public String occupation;

    class NestedClassA {
    }

    class NestedClassB {
    }

    public ServiceMan(String name, int age, String occupation) {
        super(name, age);
        this.occupation = occupation;
    }

    ServiceMan() {
        System.out.println("ServiceMan class's Empty constructor called");
    }

    @Override
    public String toInfoString() {
        return super.toInfoString() + ", occupation: " + occupation;
    }

    Object buildLocalClass() {
        class SampleLocal {
        }

        return new SampleLocal();
    }
}
