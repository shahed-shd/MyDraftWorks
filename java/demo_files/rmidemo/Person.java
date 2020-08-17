import java.rmi.Remote; 
import java.rmi.RemoteException;  

public interface Person extends Remote {
    public String getName() throws RemoteException;
    public int getAge() throws RemoteException;
    public String greetingsTo(String otherPersonName, String greetingMessage) throws RemoteException;
    public void printInfo() throws RemoteException;
}
