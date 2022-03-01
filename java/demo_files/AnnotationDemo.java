import java.lang.annotation.Annotation;
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;
import java.lang.reflect.Method;

public class AnnotationDemo {
    public static void main(final String args[]) throws NoSuchMethodException, SecurityException {
        System.out.println("Demo java annotations");

        Hello hello = new Hello();
        Method sayHelloMethod = hello.getClass().getMethod("sayHello");

        System.out.println("\nAnnotations:");
        Annotation[] annotations = sayHelloMethod.getAnnotations();

        for (Annotation annotation : annotations) {
            System.out.println(annotation.toString());
        }

        MyAnnotation myAnnotation = sayHelloMethod.getAnnotation(MyAnnotation.class);
        System.out.println("\nMyAnnotation values:");
        System.out.println("intValue: " + myAnnotation.intValue());
        System.out.println("strValue: " + myAnnotation.strValue());
    }
}

@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
@interface MyMarkerAnnotation {
}

@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
@interface MyAnnotation {
    int intValue() default 0;

    String strValue() default "DEFAULT";
}

class Hello {
    @MyMarkerAnnotation
    @MyAnnotation(intValue = 123)
    public void sayHello() {
        System.out.println("Hello");
    }
}