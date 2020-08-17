class PersonImpl implements Person {
    protected String name;
    protected int age;

    protected PersonImpl() {}

    public PersonImpl(String name, int age) {
    	this.name = name;
	this.age = age;
    }

    public String getName() {
    	return name;
    }

    public int getAge() {
    	return age;
    }

    public String greetingsTo(String otherPersonName, String greetingMessage) {
    	return "Hello, " + otherPersonName + ". " + greetingMessage;
    }

    public String toString() {
    	return "Person(name: " + name + ", age: " + age + ")";
    }

    public void printInfo() {
    	System.out.println(toString());
    }
}
