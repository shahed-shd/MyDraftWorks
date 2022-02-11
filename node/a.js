var m = require('./m')

m.fn(123)

console.log(m)

class Animal {
    constructor(name) {
        console.log('Animal.constructor() called')
        this.name = name
    }

    speak() {
        console.log(`${this.name} makes a noise.`)
    }
}

class Dog extends Animal {
    constructor(name) {
        super(name)
        console.log('Dog.constructor() called')
    }
    
    speak() {
        console.log(`${this.name} barks.`)
    }
}

dog = new Dog('Tomy')
dog.speak()