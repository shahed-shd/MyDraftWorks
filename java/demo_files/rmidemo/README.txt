Simple example of Java Remote Method Invocation (RMI)
-----------------------------------------------------

In server PC:
    - Keep all files except Client.java
    - In Server.java, RMI registry has been started programmatically using LocateRegistry.createRegistry(port) method
      Or, it can be done by command before running Server program. Example: rmiregistry 1099
    - Compile Server.java program. Command: javac Server.java
    - Execute Server program with host and port. Example: java -ea -Djava.rmi.server.hostname=192.168.0.8 Server 1099

In client PC:
    - Keep all files except Server.java
    - Compile Client.java program. Command: javac Client.java
    - Execute Client program with host and port. Example: java -ea Client 192.168.0.8 1099
