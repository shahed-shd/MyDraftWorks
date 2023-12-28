package com.example;

import com.example.annotation.BuilderProperty;

public class Person {
    private String name;
    private int age;

    String getName() {
        return name;
    }

    @BuilderProperty
    void setName(String name) {
        this.name = name;
    }

    int getAge() {
        return age;
    }

    @BuilderProperty
    void setAge(int age) {
        this.age = age;
    }
}
