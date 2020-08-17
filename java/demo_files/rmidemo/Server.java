import java.rmi.registry.Registry; 
import java.rmi.registry.LocateRegistry; 
import java.rmi.RemoteException; 
import java.rmi.server.UnicastRemoteObject; 

public class Server extends PersonImpl { 

    public static void main(final String[] args) {
        try {
	    final int serverPort = Integer.parseInt(args[0]);

            PersonImpl alice = new PersonImpl("Alice", 23); 
            PersonImpl bob  = new PersonImpl("Bob", 25); 
    
            Person stubAlice = (Person) UnicastRemoteObject.exportObject(alice, 0);
            Person stubBob = (Person) UnicastRemoteObject.exportObject(bob, 0);

	    Registry registry = LocateRegistry.createRegistry(serverPort);
            // Or, run command "rmiregistry" with port to create RMI registry and get the registry by the following commented statement.
	    // Registry registry = LocateRegistry.getRegistry(serverPort);  

            registry.rebind("alice", stubAlice);  
            registry.rebind("bob", stubBob);  
            
            System.err.println("Server ready"); 
        } catch (Exception e) { 
            System.err.println("Server exception: " + e.toString()); 
            e.printStackTrace(); 
        } 
    } 
} 
