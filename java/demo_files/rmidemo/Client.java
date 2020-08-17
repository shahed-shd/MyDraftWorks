import java.rmi.registry.LocateRegistry; 
import java.rmi.registry.Registry;  

public class Client {
    
    private Client() {}

    public static void main(final String[] args) {  
        try {  
            final String host = args[0];
            final int serverPort = Integer.parseInt(args[1]);

            Registry registry = LocateRegistry.getRegistry(host, serverPort); 

            System.out.println("Bound names in registry:");
            for(String s: registry.list()) {
                System.out.println(s);
            }

            Person stubAlice = (Person) registry.lookup("alice"); 
            System.out.println("Lookup done, stubAlice: " + stubAlice);

            Person stubBob = (Person) registry.lookup("bob"); 
            System.out.println("Lookup done, stubBob: " + stubBob);
 
            String greeting = stubAlice.greetingsTo(stubBob.getName(), "Good morning!"); 
            System.out.println("greeting: " + greeting);            

            System.out.println("Remote method invoked"); 
        } catch (Exception e) {
            System.err.println("Client exception: " + e.toString()); 
            e.printStackTrace(); 
        } 
    } 
}
