package com.example;

public class Main {

    public static void main(String[] args) {
        Person p = new PersonBuilder().setName("Alice")
                .setAge(21)
                .build();

        System.out.println("name: " + p.getName() + ", age: " + p.getAge());
    }
}
